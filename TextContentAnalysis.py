import string
import re

"""
Storing a string inside an object allows it to be passed by reference, 
instead of copying the string
"""
class TextContainer:
    def __init__(self, text: str) -> None:
        self.__text = text
        self.__text_string_length = len(self.__text)
        self.__line_breaks_list: list = self.__get_newline_chars_indices()
        self.__line_breaks_count = len(self.__line_breaks_list)
    
    @property
    def text(self):
        return self.__text
    
    @text.setter
    def text(self, value):
        #reset:
        self.__init__(value)

    @property
    def text_string_length(self):
        return self.__text_string_length
    
    @property
    def line_breaks_list(self):
        return self.__line_breaks_list
    
    @property
    def line_breaks_count(self):
        return self.__line_breaks_count

    """
    finds all line breaks
    """
    def __get_newline_chars_indices(self) -> list:
        newlines = list()
        substring_iterator = re.finditer("\n", self.__text)
        while True:
            try:
                position = next(substring_iterator).span()
                newlines.append(position[0])
            except StopIteration:
                break
        return newlines

    """
    Takes an index of character in the text and returns number of the line and number of the word 
    that contains that index. If the index corresponds to a whitespace after a word, it's counted
    as a part of that word. (This rule might be changed in the future)
    """
    def get_line_and_char_index(self, index: int, get_word_number: bool = True) -> tuple:
        if (index > -1) and (index < self.__text_string_length):
            #l = 0
            for l in range(self.__line_breaks_count):
                if self.__line_breaks_list[l] > index:
                    break
            if self.__line_breaks_list[l] < index:
                l += 1
            
            previous_break_index = l - 1
            if previous_break_index < 0:
                start_index = 0
            else:
                start_index = self.__line_breaks_list[previous_break_index]

            snippet = self.__text[start_index: index + 1]
            #print("snippet is: ", snippet)
            words = snippet.split()
            #print("words on the line are: ", words)
            w = len(words)
            #print("number of words calculated to be: ", w)
            return (l + 1, w)
        else:
            return (-1,-1)


"""
Checks if the given index in the given TextContainer's text is a dash and 
next to a newline character. Use in checking if a word was split between lines.
"""
def is_newline_with_dash(index: int, container: TextContainer) -> bool:
    if index > 0 and index < len(container.text) - 1:
        if container.text[index] == "\n":
            if container.text[index - 1] == "-":
                return True
            elif container.text[index + 1] == "-":
                return True

    return False

"""
Returns a tuple that represents the whole word that contains
he given subsection of the text as denoted by given tuple.
    (start_index, stop_index)
    start_index is the first letter 
    stop_index is AFTER the last letter
"""
def get_whole_word_span(span: tuple, container: TextContainer) -> tuple:
    if len(span) != 2:
        return span

    #ELSE:
    start_index = span[0]
    stop_index = span[1]
    search_index: int = start_index
    # iterate backwards
    while search_index > -1:
        if container.text[search_index] in string.whitespace:
            if not is_newline_with_dash(search_index, container):
                start_index = search_index + 1
                break
        #ELSE:
        search_index -= 1
    if search_index < 0:
        start_index = 0

    # iterate forward
    search_index = stop_index - 1
    while search_index < len(container.text):
        if container.text[search_index] in string.whitespace:
            if not is_newline_with_dash(search_index, container):
                stop_index = search_index
                break
        #ELSE:
        search_index += 1
    if search_index > len(container.text):
        stop_index = len(container.text)
    return (start_index, stop_index)


"""
Searches for all occurences of a given string in the given text (in the form of TextContainer)
and returns a dictionary with found words and their positions in the text. Positions are in a
form of tuple that indicates the line and the position of the first letter on that line.
"""
def find_word(word: str, container: TextContainer, get_whole_words: bool = True) -> dict:
    found_words = dict()
    #words = list()
    #substringStartPoints = []#self._find_all_substrings(text_container, word)
    substring_iterator = re.finditer(word, container.text, re.IGNORECASE)
    while True:
        try:
            wordspan = next(substring_iterator).span()
            if get_whole_words:
                wordspan = get_whole_word_span(wordspan, container)
            position = container.get_line_and_char_index(wordspan[0])
            found_words[position] = container.text[wordspan[0]:wordspan[1]]

        except StopIteration:
            break
    return found_words



#Testing goes here:
if __name__ == "__main__":
    testContainer = TextContainer("--")
    # text can be changed, which resets other attributes
    testContainer.text = "The first line of text\nis followed by another,\nand yet another after that."
    indices = [5, 15, 21, 32, 41, 51, 63, 70]
    for index in indices:
        word_position_at_index = testContainer.get_line_and_char_index(index)
        print("Index\t", index, "\tis a letter ", testContainer.text[index], "\tand corresponds to line", \
            word_position_at_index[0], " and word", word_position_at_index[1])