import string
import re

"""
Storing a string inside an object allows it to be passed by reference, 
instead of copying the string
"""
class TextContainer:
    def __init__(self, val: str) -> None:
        self.text = val

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
and returns a dictionary with found words and their positions in the text.
"""
def find_word(word: str, container: TextContainer, get_whole_words: bool = True) -> dict:
    found_words = dict()
    #words = list()
    substringStartPoints = []#self._find_all_substrings(text_container, word)
    substring_iterator = re.finditer(word, container.text, re.IGNORECASE)
    while True:
        try:
            wordspan = next(substring_iterator).span()
            if get_whole_words:
                wordspan = get_whole_word_span(wordspan, container)
            found_words[wordspan[0]] = container.text[wordspan[0]:wordspan[1]]

        except StopIteration:
            break
    return found_words
