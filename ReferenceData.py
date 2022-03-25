# alternative implementation(s):
"""
ReferenceData is an alternative to Reference
    - use keyword arguments when creating instances / objects:
    newReference = ReferenceData(type= "shitpost", name= "Keyword arguments rule", year_published= 1337)

    NOTE: Any of the arguments can be left out
"""
class ReferenceData:
    # \ allows splitting an expression between multiple rows:
    # some fields / variables can be left as None
    def __init__(self,                     \
            name: str = None,              \
            type = None,                   \
            author: str = None,            \
            publisher: str = None,         \
            year_published: int = None,    \
            ):
        
        self.name = name
        self.type = type
        self.author = author
        self.publisher = publisher
        self.year_published = year_published

# for testing, only if file is run on it's own:
if __name__ == "__main__":
    newReference = ReferenceData(type= "shitpost", name= "Keyword arguments rule", year_published= 1337)
    print(newReference.type)
    print(newReference.name)
    print(newReference.year_published)