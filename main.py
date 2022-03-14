import tkinter as tk
from tkinter.filedialog import askopenfile
import csv
import PyPDF2


# GUI setup
root = tk.Tk()
canvas = tk.Canvas(root, height=400, width=400)
canvas.grid(columnspan=3, rowspan=3)

#class setup
class Reference():
    def __init__(self, type, author, pubDate):
        self.type = type
        self.author = author
        self.pubDate = pubDate





def getType(ref_list):
    for index in range(1, len(ref_list)):
        type = ref_list[index][0]

    return type


def printType(type):
    print(type)





# Open Csv & extract entries
def open_csv_file():
    file = askopenfile(parent=root, mode="r", title="Choose a file", filetypes=[("Csv file", "*.csv")])
    reference_list = []
    if file:
        reader = csv.reader(file)
        for row in reader:
            reference_list.append(row)
        result = getType(reference_list)
        print(reference_list)
        printType(result)
        return reference_list


# Open pdf & extract text
def open_pdf_file():
    file = askopenfile(parent=root, mode="rb", title="Choose a file", filetypes=[("Pdf file", "*.pdf")])
    if file:
        read_pdf = PyPDF2.PdfFileReader(file)
        page = read_pdf.getPage(2)
        page_content = page.extractText()
        print(page_content)


# CSV Button


choose_csv_text = tk.StringVar()
choose_csv_btn = tk.Button(root, textvariable=choose_csv_text, command=lambda: open_csv_file(), bg="blue", fg="white",
                        height=2, width=15)
choose_csv_text.set("Choose Csv")
choose_csv_btn.grid(column=2, row=2)

# Pdf Button
choose_pdf_text = tk.StringVar()
choose_pdf_btn = tk.Button(root, textvariable=choose_pdf_text, command=lambda: open_pdf_file(), bg="red", fg="white",
                        height=2, width=15)
choose_pdf_text.set("Choose Pdf")
choose_pdf_btn.grid(column=1, row=2)


root.mainloop()
