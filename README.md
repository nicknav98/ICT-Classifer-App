# ICT-Classifer-App

##### Some important notations, mentioning just in case:

- `variable_name: datatype`
    - for example: `text: str` means that variable `text` should contain text data of type `str`, or string

- Double underscore in front of a variable name, like `__variable`, means that the variable is meant to be internal / private to the class, and should not be accessed or manipulated outside of the class functions

- Also, files have `local_testing()` functions that can be used to test code in that file, with code segments commented out with `""" """` ; feel free to uncomment parts to see how different parts of code work, like demos of sorts.


## Files / Modules

### main.py

Contains main loop and interface implementation. Should probably keep user interface implementation in this file.

Does not contain class definitions.


### Reference.py

Contains classes for storing reference data:

#### Classes

##### `Reference`

`Reference` class is for storing information about individual references. This class has not been developed very extensively, as getting information from references has been tricky and we haven't managed to do it reliably.

Developer opinions:
- Ideally each field should have a default value that represents lack of (parsed) information. That way constructor can be used with keyword arguments, to only set the fields for which the data is found.
- Use separate static method or class method that takes a string as an argument, extracts information that it can, and uses the constructor to create and return a new instance / object.

When constructing a `Reference` instance, use keyword arguments to only set fields for which there are values.
For example:

```
new_reference = Reference(type= ReferenceType.BLOG_POST, name= "Keyword arguments rule", year_published= 2022)
```

Currently each instance of Reference has the following fields:

- `name: str`
    - The name / title of the referenced material; consider changing variable name to "title" if that is more appropriate
- `type`
    - Type of the material, e.g. research paper or blog post
    - Holds any data type, consider using enums, see below
- `author: str`
    - Author(s) of the material
    - Change name to "authors", need to change in other parts of code
- `publisher: str`
    - Publisher(s) of the material
    - Change name to "publishers", need to change in other parts of code
- `year_published`
    - Year of publication
    - Holds any data type, could use `int` or `string`, or possibly a specially defined class
    - Consider changing to a more precise date representation, if there's a way to get it from text
- `reference_url: str`
    - URL, if there is one
    - Probably easiest part to get from text, but URLs can be mangled in text by the text editor carrying it over to next line, sometimes with a dash, '-'


This class currently has the following methods:

- `get_as_string(self) -> str`
    - Returns a string that represents fields / variables of the instance / object that have been set.
    - The string should probably follow a specific reference style, possibly based on an argument given to the method.

- `reference_from_string(cls, ref_text: str)`
    - A `@classmethod`, called with class name, rather than instance / object name
    - Takes a written reference as a string and tries to construct a `Reference` object from it.
        - Currently can only parse a URL and (possibly) a year
    - Needs to be expanded to ideally process the whole string, and maybe show what parts could not be parsed.


##### `ReferenceList`

Contains a `list` of `Reference` instances / objects and a few simple methods. Might be useful if there is a need to have some functionality specifically for a list of references of one thesis. Feel free to completely remake this.

- `add_reference(self, new_reference: Reference)` adds a `Reference` to the list 

- `reference_string_at_index(self, index)` uses `Reference` class method to get a string with information of a specific reference
    
- `debug_printout(self)` prints out all contained `Reference` objects as strings


##### `ReferenceType`

Enumeration class (inherits `Enum`) used to define reference type enumerations. Having defined variables with string values can be used to avoid typos for Reference's type field.

For examlpe:

```
RESEARCH_PAPER__PEER_REVIEWED = "Research paper, peer reviewed"
```


### TextContentAnalysis.py

Contains `TextContainer` class and a few other functions for analyzing text strings. Most functions are not yet used by anything else.

#### Classes

##### `TextContainer`

`TextContainer` class is for passing strings by reference and analyzing contents of text, especially for evaluating relevance of referenced text material, by looking for specific words and sentences that contain those words. Several of the functions are not meant to be used directly by the end user, but rather are utilities for other functions of the class.

An instance of `TextContainer` can hold:
- `__text: str`
    - Normal way of storing text

OR
- `__response_object: Response`
    - An object containing response data from a web page, see `requests` module
    - Probably not needed and can be removed, along with parts of constructor and properties that accomodate it
NOTE: `TextContainer` can only hold ONE of these: if one is assigned, the other is set to None
    If both are given to constructor, text string is ignored

Properties `text` and `response_object` should be used when retrieving or assigning values to a `TextContainer`.

The following values are derived:
- `text_string_length: int`
    - Just the length of the text, calculated when text is assigned
- `word_start_indices: list`
    - List should contain only `int` values
    - Each integer represents an index of the first letter of a word
    - NOTE: values are not always calculated, but can be useful, and are also used by the function that calculates the ordinal number of a word that occupies a specific index, and by extension the `find_word( ... )`, see below
        - Word ordinals / indices can be calculated by the constructor if `index_words` argument is `True`, or later by calling the function `index_text_words`
- `word_count`
    - Just the number of words in the contained, calculated when words are indexed, if they are indexed

Arguably the two important functions are `find_word( ... )` and `find_sentences_with_words( ... )`

```
find_word(self, word: str,
        as_dictionary: bool = False,
        all_partial_matches: bool = False,
        word_affix_char: str = '*',
        return_word_indices: bool = False)
```

searches through the contained text string for occurences of given word / substring. Can optionally only get exact matches, all partial matches or words that start or end with given set of characters.

Returns a list or a dictionary, containing tuples that denote word's first letter's index and the index AFTER the last letter, OR can return ordinal numbers of words if the optional `return_word_indices` is set to `True`.

`word_affix_char`, * by default, is a character that when found on either end of the word given as the argument, tells the function to also match larger words that contain the searched word.
For example:
`"by*"` will also match words like `"byproduct"` and `"bygone"`
`"*word"` will also match words like `"crossword"` and `"keyword"`
`"*arch*"` will also match words like `"searched"` and `"parched"`

If optional argument `all_partial_matches` is set as `True`, all words that contain the given word are included.

```
find_sentences_with_words(self,
        must_contain_all: list = list(),
        must_contain_some: list = list(),
        better_if_has_more: list = list(),
        cannot_contain_any: list = list(),
        prioritize_by_must_contain_some: bool = True,
        ignore_case: bool = True,
        max_sentences_returned = 0):
```

looks for sentences that contain and/or don't contain specific words.

All arguments are optional, uses `find_word( ... )`, so lists can contain, for example strings like `"key*"` to match words that start with letters `"key"`

- `must_contain_all: list = list()`
    - a sentence must contain all of these words
- `must_contain_some: list = list()`
    - a sentence must contain at least one of these words
- `better_if_has_more: list = list()`
    - prefers sentences with more of these appearing at least once
- `cannot_contain_any: list = list()`
    - a sentence can not contain any of these
- `prioritize_by_must_contain_some: bool = True`
    - if `True`, having more of these appear at least once is preferred
- `ignore_case: bool = True`
    - ignores letter case for ALL matches
    - there might be a good way to specify whether letter case should be ignored for specific words
- `max_sentences_returned = 0`
    - if greater than 0, returns only a number of best matches, based on `better_if_has_more`, and if `prioritize_by_must_contain_some` is `True`, also by `must_contain_some`

Should be extended to be able to use optional arguments of `find_word( ... )`


### External modules used:

- `PyPDF2`
    - Used for handling pdf files
- `requests`
    - Used for getting data from websites
- `re`
    - Regular expression module for finding patterns in strings
    - TextContentAnalysis module is essentially an extension of this, with more specialized functions
- `string`
    - Primarily for identifying string characters by their type, like whitespaces and printable characters
- `tkinter`
    - Current graphical user interface is made using this
- `csv`
    - For handling csv files, probably won't be needed

#### Other recommended external modules, libraries and classes:

- "Beautiful Soup" library / `BeautifulSoup` class, for easier manipulation of html code
    - https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- `io` for stream handling, especially if accessing remote pdf files


