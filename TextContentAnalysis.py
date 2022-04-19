import string
import re
import requests

"""
Characters between words in html code text
"""
html_non_word_chars = string.whitespace + "<=>[/]{*}.,;:" + '"'

"""
Storing a string inside an object allows it to be passed by reference, 
instead of copying the string. Can store response object instead, 
in which case there is no separate string and text property returns
response object's text property
"""
class TextContainer:
    def __init__(self, text: str, response_object: requests.Response = None, index_words = False) -> None:
        self.__text = text if response_object == None else None
        self.__response_object = response_object
        self.__text_string_length = len(self.__text) if self.__text else len(response_object.text)
        self.__line_breaks_list: list = self.__get_newline_chars_indices()
        self.__line_breaks_count = len(self.__line_breaks_list)
        self.__word_start_indices = list()
        self.__word_count = None
        if index_words:
            self.index_text_words()

    
    @property
    def text(self):
        return self.__text if self.__text else self.__response_object.text
    
    @text.setter
    def text(self, value):
        #reset:
        self.__init__(text= value)
    
    @property
    def response_object(self):
        return self.__response_object
    
    @response_object.setter
    def response_object(self, value):
        self.__init__(text= None, response_object= value)

    @property
    def text_string_length(self):
        return self.__text_string_length
    
    @property
    def line_breaks_list(self):
        return self.__line_breaks_list
    
    @property
    def line_breaks_count(self):
        return self.__line_breaks_count
    
    @property
    def word_indices(self):
        return self.__word_start_indices

    @property
    def word_count(self):
        return self.__word_count

    """
    <OBSOLETE>
    finds all line breaks
    """
    def __get_newline_chars_indices(self) -> list:
        newlines = list()
        if self.__response_object:
            substring_iterator = re.finditer("\n", self.__response_object.text)
        else:
            substring_iterator = re.finditer("\n", self.__text)
        while True:
            try:
                position = next(substring_iterator).span()
                newlines.append(position[0])
            except StopIteration:
                break
        return newlines

    """
    Searches for all occurences of a given string in the TextContainer's text
    and returns found words and their positions in the text, as a list or a dictionary with
    of positions. Positions are represented by a tuple that consists of:
    - index of the first character
    - index after the last character
    e.g. word_string = text_container.text[span[0]:span[1]], where:
    - 'text_container' is a TextContainer object
    - 'span' is a single tuple representing word position
        'word_string' would be assigned the word as a string
    """
    def find_word(self, word: str,
            as_dictionary: bool = False,
            all_partial_matches: bool = False,  # returns all substring matches if true
            word_affix_char: str = '*'):

        found_words_dict = dict()
        found_words_list = list()

        check_prefix = word[0] == word_affix_char
        if check_prefix:
            word = word[1:]

        check_suffix = word[len(word) - 1] == word_affix_char
        if check_suffix:
            word = word[:-1]

        substring_iterator = re.finditer(word, self.text, re.IGNORECASE)
        while True:
            try:
                match_span = next(substring_iterator).span()
                match_span = self.get_word_span(match_span, include_prefix= check_prefix, include_suffix= check_suffix)
                wordspan = self.get_word_span(match_span)

                # how to return only proper matches
                if ((match_span[0] == wordspan[0]) and (match_span[1] == wordspan[1])) or all_partial_matches:
                    word_position = self.get_word_index(match_span[0])
                    if as_dictionary:
                        found_words_dict[word_position] = self.text[wordspan[0]:wordspan[1]]
                    else:
                        found_words_list.append(self.text[wordspan[0]:wordspan[1]])

            except StopIteration:
                break
        if as_dictionary:
            return found_words_dict
        else:
            return found_words_list


    """
    FOR OPTIONAL LIST PROPERTY, DO NOT USE IF MEMORY IS LIMITED!
    finds starting index for each word in the string
    -> use this to help quickly calculating the ordinal number
    of a word based on the index of it's first letter
    """
    def index_text_words(self):
        self.__word_count = 0
        looking_for_word_start = True
        for i in range(self.__text_string_length):
            if looking_for_word_start:
                if (not (self.text[i] in html_non_word_chars)) and (self.text[i] in string.printable):
                    self.__word_start_indices.append(int(i))
                    self.__word_count += 1
                    looking_for_word_start = False
            elif self.text[i] in html_non_word_chars:
                looking_for_word_start = True

    
    """
    Returns the index of the word that starts on given character index
    TODO: implement a *good* search algorithm
    """
    def get_word_index(self, index: int):
        if len(self.__word_start_indices) > 0:
            for i in range(self.__word_count):
                if index < self.__word_start_indices[i]:
                    if i == 0:
                        return self.__word_start_indices[0]
                    else:
                        return self.__word_start_indices[i - 1]
                
                return self.__word_start_indices[i]
        else:
            word_count = 0
            looking_for_word_start = True
            for i in range(index + 1):
                if looking_for_word_start:
                    if (not (self.text[i] in html_non_word_chars)) and (self.text[i] in string.printable):
                        word_count += 1
                        looking_for_word_start = False
                elif self.text[i] in html_non_word_chars:
                    looking_for_word_start = True
            return word_count


    """
    Finds sentences that:
        - contain all of the must_contain_all
        - contain at least one of must_contain_some
            - *can* prefer more over less
        - do NOT contain any forbidden substrings
    and returns them in order from having most preferred substrings
    to least.
    """
    def find_sentences_with_words(self,            \
            must_contain_all: list = list(),     \
            must_contain_some: list = list(),    \
            better_if_has_more: list = list(),        \
            cannot_contain_any: list = list(),   \
            prioritize_by_must_contain_some: bool = True,    \
            ignore_case: bool = True,   \
            max_sentences_returned = 0):
        
        # find all occurences of first word
        word_results = self.find_word(must_contain_all[0])
        untested_sentences = list()
        ranked_sentences = list()
        found_sentence = (-1,-1)
        for i in range(len(word_results)):
            found_sentence = self.get_whole_sentence(word_results[i][0])
            if not (found_sentence in untested_sentences):
                untested_sentences.append(found_sentence)
        # look for the rest of required words; each must be found in each of the sentences

        for i in range(len(untested_sentences)):
            # test each sentence for substring ratios
            ratio_required_all = found_substring_ratio(
                untested_sentences[i], 
                must_contain_all, 
                ignore_case
                )
            ratio_required_some = found_substring_ratio(
                untested_sentences[i], 
                must_contain_some, 
                ignore_case
                )
            ratio_priority = found_substring_ratio(
                untested_sentences[i],
                (better_if_has_more + must_contain_some) if prioritize_by_must_contain_some else better_if_has_more,
                ignore_case
                )
            ratio_forbidden = found_substring_ratio(
                untested_sentences[i], 
                cannot_contain_any, 
                ignore_case
                )

            if (ratio_required_all == 1) \
            and (ratio_required_some > 0) \
            and (ratio_forbidden == 0):
                orderly_tuple_insert((untested_sentences[i], ratio_priority), ranked_sentences)
        
        print(ranked_sentences)
        # clean up the list by removing the rank number:
        for i in range(len(ranked_sentences)):
            ranked_sentences[i] = ranked_sentences[i][0]
        
        return ranked_sentences[0:max_sentences_returned]
        


    """
    TODO: made this part of the class, TEST!!
    Checks if the given index in the given TextContainer's text is a dash and 
    next to a newline character. Use in checking if a word was split between lines.
    """
    def is_newline_with_dash(self, index: int) -> bool:
        if index > 0 and index < len(self.text) - 1:
            if self.text[index] == "\n":
                if self.text[index - 1] == "-":
                    return True
                elif self.text[index + 1] == "-":
                    return True

        return False

    """
    TODO: made this part of the class, TEST!!
    Returns a tuple that represents the larger word that contains
    he given subsection of the text as denoted by given tuple.
    By default returns the whole word, but can ignore:
    - character before given span (prefix), OR
    - characters after given span (suffix)
        (start_index, stop_index)
        start_index is the first letter 
        stop_index is AFTER the last letter
    """
    def get_word_span(self, \
            span: tuple, \
            include_prefix: bool = True, \
            include_suffix: bool = True \
            ) -> tuple:
            
        if len(span) != 2:
            return span

        #ELSE:
        start_index = span[0]
        stop_index = span[1]
        search_index: int = start_index

        # iterate backwards
        if include_prefix:
            while search_index > -1:
                if self.text[search_index] in html_non_word_chars:
                    if not self.is_newline_with_dash(search_index):
                        start_index = search_index + 1
                        break
                #ELSE:
                search_index -= 1
            if search_index < 0:
                start_index = 0

        # iterate forward
        if include_suffix:
            search_index = stop_index - 1
            while search_index < len(self.text):
                if self.text[search_index] in html_non_word_chars:
                    if not self.is_newline_with_dash(search_index):
                        stop_index = search_index
                        break
                #ELSE:
                search_index += 1
            if search_index > len(self.text):
                stop_index = len(self.text)
        
        return (start_index, stop_index)

    """
    TODO: made this part of the class, TEST!!
    Returns the span of the whole sentence around the specified index as a tuple
    denoting start and end indices.
    ISSUES:
    - a "sentence" can start after index, if the index is the whitespace after the period
        - this should not be a problem if index of a found word is used
    """
    def get_whole_sentence(self, index: int) -> tuple:
        if index < 0:
            index = 0
        if index >= self.text_string_length:
            index = self.text_string_length - 1

        start_index = index
        stop_index = index

        # iterate backwards
        search_index: int = start_index
        if self.text[search_index] == '.':
            search_index -= 1
        while search_index > -1:
            if self.text[search_index] == '.':
                start_index = search_index + 1
                if self.text[start_index] in string.whitespace:
                    start_index += 1
                break
            #ELSE:
            search_index -= 1
        if search_index < 0:
            start_index = 0
        if start_index >= self.text_string_length:
            start_index = self.text_string_length - 1

        # iterate forward
        search_index = stop_index
        while search_index < len(self.text):
            if self.text[search_index] == '.':
                stop_index = search_index + 1
                break
            #ELSE:
            search_index += 1
        if search_index > len(self.text):
            stop_index = len(self.text)
        return (start_index, stop_index)


    """
    Finds links in "" -marks, starting with http, that:
        - contain all of the required_substrings_all
        - contain at least one of required_substrings_some
            - does not prefer more over less
        - do NOT contain any forbidden substrings
    and returns them in order from having most preferred substrings
    to least.
    """
    def find_links(self,            \
            required_substrings_all: list = list(),     \
            required_substrings_some: list = list(),    \
            preferred_substrings: list = list(),        \
            forbidden_substrings: list = list(),   \
            max_links_returned = 1):
        links = list()
        substring_iterator = re.finditer("http", self.text, re.IGNORECASE)
        while True:
            try:
                wordspan = next(substring_iterator).span()
                searchindex = wordspan[1]
                while (self.text[searchindex] != '"') and (searchindex < self.text_string_length):
                    searchindex += 1
                link_string = self.text[wordspan[0]:searchindex]# one link as a string
                if found_substring_ratio(link_string, required_substrings_all) == 1 \
                        and found_substring_ratio(link_string, required_substrings_some) > 0 \
                        and found_substring_ratio(link_string, forbidden_substrings) == 0:
                    link_rating = found_substring_ratio(link_string, preferred_substrings)
                    orderly_tuple_insert((self.text[wordspan[0]:searchindex], link_rating), links)

            except StopIteration:
                break
        
        links = links[0:max_links_returned]
        for i in range(len(links)):
            links[i] = links[i][0]
        return links


"""
Returns individual numbers found in a string. Can start and/or end at specified indices 
and limit the number of numbers searched for. Returns either list of tuples denoting character 
spans (like with words), or optionally a dictionary of span tuples and numbers themselves.
NOTE: Numbers are returned as strings to preserve exact way they are typed in text.
"""
def find_number_spans_in_text(text: str, 
        decimal_delimeter: str = ',',
        start_index: int = 0, 
        end_index: int = -1, 
        max_numbers_returned: int = 0, 
        as_dictionary: bool = False
        ) -> list:
    
    list_of_numbers = list()
    dict_of_numbers = dict()
    substring_iterator = re.finditer(
        "-{0,1}[0-9]{1,}" + 
        decimal_delimeter + 
        "{0,1}[0-9]{0,}", 
        text[start_index: end_index if (end_index > 0) else len(text)]
        )
    
    numbers_found = 0
    while (max_numbers_returned < 1) or (numbers_found < max_numbers_returned):
        try:
            span = next(substring_iterator).span()
            if as_dictionary:
                dict_of_numbers[span] = text[span[0]:span[1]]
            else:
                list_of_numbers.append(span)
            
            numbers_found += 1

        except StopIteration:
            break
    
    if as_dictionary:
        return dict_of_numbers
    else:
        return list_of_numbers


"""
Returns a fraction of how many of the given substrings are present in the main string
If substrings list is empty, returns 1
"""
def found_substring_ratio(main_string: str, substrings: list, ignore_case: bool = True):
    all = len(substrings)
    if all == 0:
        return 1.0
    else:
        found = 0
        for s in substrings:
            if type(s) == str:
                if ignore_case:
                    if re.search(s, main_string, re.IGNORECASE):
                        found += 1
                else:
                    if re.search(s, main_string):
                        found += 1
        return found / all

"""
Inserts a tuple into a list of tuples based on the second value.
This a utility function for other functions in this module.
"""
def orderly_tuple_insert(new_tuple: tuple, t_list: list):
    for i in range(len(t_list)):
        if t_list[i][1] < new_tuple[1]:
            t_list.insert(i, new_tuple)
            return
    # this is executed ONLY if no other slot is acceptable:
    t_list.insert(len(t_list), new_tuple)


"""
Use this for local testing of module's functions:
1. Write content of your choosing in local_testing -function
2. Run the script by itself
"""
def local_testing():
    # finding numbers:

    test_text = "1234 sfdg 1234 awe3ws8eyhg8qwgdse 24q3"
    list_of_numbers = find_number_spans_in_text(test_text)
    print(list_of_numbers)
    list_of_numbers = find_number_spans_in_text(test_text, max_numbers_returned= 3)
    print(list_of_numbers)
    list_of_numbers = find_number_spans_in_text(test_text, start_index= len(test_text) // 2)
    print(list_of_numbers)
    print("dictionary:")
    list_of_numbers = find_number_spans_in_text(test_text, as_dictionary= True)
    print(list_of_numbers)

    # finding words:
    """
    test_text = "To address the uncertainty of data parameters including those\n" +\
        "in the technology, market, and society ﬁeld, a stochastic optimi-\n" +\
        "zation model is developed to estimate the arbitrage proﬁt of PHEV\n" +\
        "under three scenarios of electricity market and buyer behavior.\n" +\
        "The arbitrage proﬁt is measured as the difference between the\n" +\
        "baseline case and the arbitrage case. The cost in the arbitrage case\n" +\
        "is the sum of charging cost and battery degradation cost, minuses\n" +\
        "the revenue from V2G discharging. In the baseline case, PHEV does\n" +\
        "not participate in arbitrage. The cost in this case consists of only\n" +\
        "charging cost and degradation cost from PHEV driving."
    testContainer = TextContainer(test_text)
    words_to_find = ["case", "The", "base*"]
    for word in words_to_find:
        w_list = testContainer.find_word(word)
        w_dict = testContainer.find_word(word, as_dictionary= True)
        print(w_list)
        print(w_dict)
    """

    # getting whole sentence:
    """
    test_text = "To address the uncertainty of data parameters including those\n" +\
        "in the technology, market, and society ﬁeld, a stochastic optimi-\n" +\
        "zation model is developed to estimate the arbitrage proﬁt of PHEV\n" +\
        "under three scenarios of electricity market and buyer behavior.\n" +\
        "The arbitrage proﬁt is measured as the difference between the\n" +\
        "baseline case and the arbitrage case. The cost in the arbitrage case\n" +\
        "is the sum of charging cost and battery degradation cost, minuses\n" +\
        "the revenue from V2G discharging. In the baseline case, PHEV does\n" +\
        "not participate in arbitrage. The cost in this case consists of only\n" +\
        "charging cost and degradation cost from PHEV driving."
    testContainer = TextContainer(test_text)
    print(len(test_text))
    indices = [12, 20, 92, 102, 130, 257, 258, 280, 305, 444, 519, 641]
    for index in indices:
        span = testContainer.get_whole_sentence(index)
        print(index, testContainer.text[index], span, testContainer.text[span[0]:span[1]])
        print("\n")
    """

    # substring ratio test:
    #   need to use find word instead? use * to denote that the word continues forward or back
    #                                                           "the*" can be "there"
    """
    test_text = "The first line of text\nis followed by another,\nand yet another after that."
    ratio_ignore_case = found_substring_ratio(test_text, ["first", "the ", "By"])
    ratio_match_case = found_substring_ratio(test_text, ["first", "the ", "By"], False)
    print(ratio_ignore_case, ratio_match_case)
    """
    # html analysis:
    """
    html_text = TextContainer(requests.get("https://www.wikipedia.org/").text)
    str_english = html_text.find_word("english")
    with open('results.txt', 'w') as file:
        for r in str_english:
            file.write(str(r))
            file.write(" ")
        file.write("\n\n=======\n\n")
        file.write(html_text.text)
    """

    """
    # Index testing:
    testContainer = TextContainer("The<first*line.of:text\nis>followed*by<another,\nand<yet<another,after<that.")
    #testContainer.index_text_words()   # <- optional
    indices = [5, 15, 21, 32, 41, 51, 63, 70]
    for index in indices:
        print("Index\t", index, "\tis a letter ", testContainer.text[index], "\tand part of word number", \
            testContainer.get_word_index(index))
    """


#Testing goes here:
if __name__ == "__main__":
    local_testing()