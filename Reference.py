"""
Use keyword arguments when creating instances / objects:
newReference = Reference(type= "shitpost", name= "Keyword arguments rule", year_published= 1337)

NOTE: Any of the arguments can be left out
"""

class Reference:
    # \ allows splitting an expression between multiple rows:
    # some fields / variables can be left as None
    def __init__(self,                     \
            name: str = None,              \
            type = None,                   \
            author: str = None,            \
            publisher: str = None,         \
            year_published = None,         \
            ):
        
        self.name = name
        self.type = type
        self.author = author
        self.publisher = publisher
        self.year_published = year_published
    
    def get_as_string(self):
        return  \
            (("Name: " + str(self.name) + " ; ") if (self.name != None) else "") + \
            (("Type: " + str(self.type) + " ; ") if (self.type != None) else "") + \
            (("Author: " + str(self.author) + " ; ") if (self.author != None) else "") + \
            (("Publisher: " + str(self.publisher) + " ; ") if (self.publisher != None) else "") + \
            (("Year of publication: " + str(self.year_published) + " ;") if (self.year_published != None) else "")

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