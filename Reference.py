import re
"""
Use keyword arguments when creating instances / objects:
newReference = Reference(type= "shitpost", name= "Keyword arguments rule", year_published= 1337)

NOTE: Any of the arguments can be left out
"""

class Reference:
    
    # can't be next to a year notation in a reference text,
    #   only applies if looking for just a year by itself
    ref_text_year_disqualifiers = "\\/:+-*1234567890"
    
    # some fields / variables can be left as None
    def __init__(self,
            name: str = None,
            type = None,
            author: str = None,
            publisher: str = None,
            year_published = None,
            reference_url: str = None
            ):
        
        self.name = name
        self.type = type
        self.author = author
        self.publisher = publisher
        self.year_published = year_published
        self.reference_url = reference_url
    
    def get_as_string(self):
        return  \
            (("Name: " + str(self.name) + " ; ") if (self.name != None) else "") + \
            (("Type: " + str(self.type) + " ; ") if (self.type != None) else "") + \
            (("Author: " + str(self.author) + " ; ") if (self.author != None) else "") + \
            (("Publisher: " + str(self.publisher) + " ; ") if (self.publisher != None) else "") + \
            (("Year of publication: " + str(self.year_published) + " ;") if (self.year_published != None) else "") +\
            (("Reference URL: " + str(self.reference_url) + " ;") if (self.reference_url != None) else "")

    # try to just get the year and the potential URL for now, expand later
    @classmethod
    def reference_from_string(cls, ref_text: str):
        year = None
        ref_url = None

        url_match = re.search("http", ref_text)
        if url_match:
            url_span = url_match.span()
            search_index = url_span[1]
            while (search_index < len(ref_text)) and (ref_text[search_index] != ' '):
                search_index += 1
            url_span = (url_span[0], search_index)
            ref_url = ref_text[url_span[0]:url_span[1]]

            # cuts out the URL from string variable, 
            # only affects string in this function
            ref_text = ref_text[0:url_span[0]] + ref_text[url_span[1]:]
        
        # find the first 4-digit number that is not next to
        # characters that imply that it's not a year:
        str_iterator = re.finditer("[0-9]{4}", ref_text)
        while True:
            try:
                span = next(str_iterator).span()
                if span[0] > 0:
                    if (ref_text[span[0] - 1] in cls.ref_text_year_disqualifiers):
                        continue
                if span[1] < len(ref_text):
                    if (ref_text[span[1]] in cls.ref_text_year_disqualifiers):
                        continue
                
                # can un-comment for debugging:
                #print(ref_text[span[0]:span[1]], " at: ", span)
                year = int(ref_text[span[0]:span[1]])
                break
    
            except StopIteration:
                break
            except ValueError:
                break
        
        return Reference(year_published= year, reference_url= ref_url)

class ReferenceList:
    def __init__(self):
        self.references = []

    def add_reference(self, new_reference: Reference):
        for ref in self.references:
            if ref == new_reference:
                print("Reference is already in the list")
                return
        self.references.append(new_reference)

    def reference_string_at_index(self, index):
        return self.references[index].get_as_string()
    
    def debug_printout(self):
        for ref in self.references:
            print(ref.get_as_string())

    def construct(self, refinstance):
        pass
        #target_class = getattr(Reference, refinstance)
        #instance = target_class()
        #self.references.append(instance)

# for testing, only if file is run on it's own:
def local_testing():
    newReference = Reference.reference_from_string("Bolland, J., Wilson, J. (1994). \
Three faces of integrative coordination: A model\
of interorganizational relations in community-based health and human services.\
Health Service Research. Luettavissa:\
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1070009/ Luettu 1.11.2021")
    
    print(newReference.get_as_string())

    # keyword arguments:
    """
    newReference = Reference(type= "shitpost", name= "Keyword arguments rule", year_published= 1337)
    print(newReference.type)
    print(newReference.name)
    print(newReference.year_published)
    ref_list = ReferenceList()
    ref_list.add_reference(newReference)
    ref_list.add_reference(newReference)
    ref_list.debug_printout()
    newReference.author = "anonymous"
    ref_list.debug_printout()
    """

if __name__ == "__main__":
    local_testing()

"""
# class setup
class Reference:
    def __init__(self, attr):
        self.attr = attr

class ReferenceList:
    def __init__(self):
        self.allClasses = []

    def construct(self, refinstance):
        target_class = getattr(Reference, refinstance)
        instance = target_class()
        self.allClasses.append(instance)
"""