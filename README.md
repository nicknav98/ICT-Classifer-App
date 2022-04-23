# ICT-Classifer-App

====== Classes ======

 Reference

Reference class is for storing information about individual references. This class has not been developed very extensively, as getting information from references has been tricky and we haven't managed to do it reliably.

Developer opinions:
- Ideally each field should have a default value that represents lack of (parsed) information. That way constructor can be used with keyword arguments, to only set the fields for which the data is found.
- Use separate static method or class method that takes a string as an argument, extracts information that it can, and uses the constructor to create and return a new instance / object.

Currently each instance of Reference can hold:
 - name of the referenced material, such as a title; consider changing variable name to "title" if that is more appropriate
    - data type: string
 - type of material, e.g. research paper or blog post
    - data type: any, consider using enums
 - author(s) of the material
    - data type: string
    - change name to "authors", need to change in other parts of code
 - publisher(s) of the material
    - data type: string
    - change name to "publishers", need to change in other parts of code
 - year of publication
    - data type: any, use int or string, or possibly specially defined class
    - consider changing to a more precise date representation, if there's a way to get it from text
 - URL, if there is one
    - data type: string
    - probably easiest part to get from text, but can be mangled in text by the text editor carrying it over to next line

=== TextContainer ===

TextContainer class is for passing strings by reference and analyzing contents of text, especially for evaluating relevance of referenced text material, by looking for specific words and sentences that contain those words. Several of the functions are not meant to be used directly by the end user, but rather are utilities for other functions of the class.

An instance of TextContainer can hold:
- text
    - data type: string
    OR
- response object from Requests module
    - data type: Response, see requests module
    - probably not needed and can be removed, along with parts of constructor and properties that accomodate it
NOTE: TextContainer can only hold ONE of these: if one is assigned, the other is set to None
    If both are given to constructor, text string is ignored

The following values are derived:
- text_string_length
    - data type: int
    - just the length of the text, calculated when text is assigned
- word_start_indices
    - data type: list, should contain only int values
    - each integer represents an index of the first letter of a word
    - optional: values are not always calculated, but can be useful, and are also used by the function that calculates the ordinal number of a word that occupies a specific index, and by extension the find_word( ... ), see below
- word_count
    - just the number of words in the contained, calculated when words are indexed, if they are indexed

Arguably the two important functions are find_word( ... ) and find_sentences_with_words( ... )

find_word(self, word: str,
        as_dictionary: bool = False,
        all_partial_matches: bool = False,
        word_affix_char: str = '*',
        return_word_indices: bool = False)

searches through the contained text string for occurences of given word / substring. Can optionally only get exact matches, all partial matches or words that start or end with given set of characters.

Returns a list or a dictionary, containing tuples that denote word's first letter's index and the index AFTER the last letter, OR can return ordinal numbers of words if the optional return_word_indices is set to True.

word_affix_char, * by default, is a character that when found on either end of the word given as the argument, tells the function to also match larger words that contain the searched word.
For example:
"by*" will also match words like "byproduct" and "bygone"
"*word" will also match words like "crossword" and "keyword"
"*arch*" will also match words like "searched" and "parched"

If optional argument all_partial_matches is set as True, all words that contain the given word are included.


find_sentences_with_words(self,
        must_contain_all: list = list(),
        must_contain_some: list = list(),
        better_if_has_more: list = list(),
        cannot_contain_any: list = list(),
        prioritize_by_must_contain_some: bool = True,
        ignore_case: bool = True,
        max_sentences_returned = 0):

looks for sentences that contain and/or don't contain specific words.

All arguments are optional, uses find_word( ... ), so lists can contain, for example strings like "key*" to match words that start with letters "key"

- must_contain_all: list = list()
    - a sentence must contain all of these words
- must_contain_some: list = list()
    - a sentence must contain at least one of these words
- better_if_has_more: list = list()
    - prefers sentences with more of these appearing at least once
- cannot_contain_any: list = list()
    - a sentence can not contain any of these
- prioritize_by_must_contain_some: bool = True
    - if True, having more of these appear at least once is preferred
- ignore_case: bool = True
    - ignores letter case for ALL matches
    - there might be a good way to specify whether letter case should be ignored for specific words
- max_sentences_returned = 0
    - if greater than 0, returns only a number of best matches, based on "better_if_has_more" and if "prioritize_by_must_contain_some" is True, also by "must_contain_some"

Should be extended to be able to use optional arguments of find_word( ... )