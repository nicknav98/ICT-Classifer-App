import requests as req
import TextContentAnalysis as Analysis
import re

def get_source(ref_link: str, \
        look_for_file_link: bool = False, \
        required_link_parts: list = [], \
        preferred_link_parts: list = [], \
        forbidden_link_parts: list = []):
    
    page: req.Response = req.get(ref_link)

    try:
        page.json()
        print("Response was a json script")
    except:
        print("Response was NOT a json script")
    
    content = page.text
    
    content = Analysis.TextContainer(content)
    
    if look_for_file_link:
        print("Getting link...")
        links = Analysis.find_links(content, required_link_parts, preferred_link_parts, forbidden_link_parts, 1)
        print("Trying link: ", links[0])
        get_source(links[0], look_for_file_link= False)
    
    return content
    

def local_testing():
    test_container = get_source("https://www.theseus.fi/handle/10024/342934",\
        True, \
        required_link_parts= [".pdf"], \
        preferred_link_parts= ["Alhola", "Juho"], \
        forbidden_link_parts= [".jpg", ".jpeg", ".png", ".webm"])   # ignore images
    # WARNING! This prints out A LOT.
    # Seems to get link to file, but doesn't seem to properly read it, 
    # need to handle it better.
    print(test_container.text)

if __name__ == "__main__":
    local_testing()