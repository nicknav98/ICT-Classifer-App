import requests as req
import TextContentAnalysis as Analysis
import re

def get_source(ref_link: str,                       \
        look_for_file_link: bool = False,           \
        required_substrings_all: list = [],         \
        required_substrings_some: list = list(),    \
        preferred_substrings: list = [],            \
        forbidden_substrings: list = []):
    
    page: req.Response = req.get(ref_link)

    try:
        page.json()
        print("Response was a json script")
    except:
        print("Response was not a json script, likely http / https")
    
    content = page.text
    
    content = Analysis.TextContainer(content)
    
    if look_for_file_link:
        print("Getting link...")
        links = Analysis.find_links(content, \
            required_substrings_all, \
            required_substrings_some, \
            preferred_substrings, \
            forbidden_substrings, \
            1)
        
        print("Trying link: ", links[0])
        get_source(links[0], look_for_file_link= False)
    
    return content
    

def local_testing():
    test_container = get_source("https://www.theseus.fi/handle/10024/342934",\
        True, \
        required_substrings_all= ["https"], \
        required_substrings_some= [".pdf"], \
        preferred_substrings= ["Alhola", "Juho"], \
        forbidden_substrings= [".jpg", ".jpeg", ".png", ".webm"])   # ignore images
    # WARNING! This prints out A LOT.
    # Seems to get link to file, but doesn't seem to properly read it, 
    # need to handle it better.
    print(test_container.text)

if __name__ == "__main__":
    local_testing()