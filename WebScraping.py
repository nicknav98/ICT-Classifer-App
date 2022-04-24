from enum import Enum
import requests
import TextContentAnalysis as Analysis
import re
import PyPDF2
import io
from bs4 import BeautifulSoup

"""
JUST DELETE THIS FILE IF IT'S NOT USED FOR FETCHING DATA FROM WEB
"""

#TODO:
# 1. extract visible text / save a section of visible text as a string
# 2. print visible text string
def local_testing():
    resp = requests.get("https://en.wikipedia.org/wiki/Main_Page")
    html_text = resp.text
    print(html_text)


    """
    # remote pdf testing:
    resp = \
        requests.get("https://www.theseus.fi/bitstream/handle/10024/342934/Alhola_Juho.pdf?sequence=2&isAllowed=y")
    pdf_bytes = io.BytesIO(resp.content)
    pdf_reader = PyPDF2.PdfFileReader(pdf_bytes)
    for i in range(pdf_reader.getNumPages()):
        print(pdf_reader.getPage(i).extractText())
        usr_input = input("Continue? (- / n)")
        if usr_input.lower() == "n":
            break
        else:
            continue
    """

if __name__ == "__main__":
    local_testing()