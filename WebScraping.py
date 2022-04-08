from enum import Enum
import requests
import TextContentAnalysis as Analysis
import re
import PyPDF2
import io
from bs4 import BeautifulSoup

"""
"""
class SourceType(Enum):
    WEBSITE = 0
    PDF = 1


def local_testing():
    resp = requests.get("https://en.wikipedia.org/wiki/Main_Page")
    #TODO:
    # 1. get response html
    # 2. extract visible text
    # 3. save as TextContainer
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