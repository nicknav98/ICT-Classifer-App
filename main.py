import tkinter as tk
from tkinter.filedialog import askopenfile
import csv
import PyPDF2
from Reference import Reference, ReferenceList

# GUI setup
root = tk.Tk()
canvas = tk.Canvas(root, height=300, width=800)
canvas.grid(columnspan=3, rowspan=3)

# Header
header = tk.Label(root, text="ICT Thesis Classifier App Prototype", font="Raleway")
header.grid(columnspan=3, column=0, row=0)

reference_container = ReferenceList()

#firstReference = ReferenceList()

def reset_reference_list():
    reference_container.references.clear()

def get_one_ref(ref_list):
    for index in range(1, len(ref_list)):
        type = ref_list[index][0]

    return type

def csv_row_to_reference(row) -> Reference:
    # bandaid solution, csv reader returns the first row as a list of 3, others as list of 1
    if len(row) == 1:
        row = str(row[0]).split(',')
    return Reference(type= row[0], author= row[1], year_published= row[2])

# Open Csv & extract entries
def open_csv_file():
    file = askopenfile(parent=root, mode="r", title="Choose a file", filetypes=[("Csv file", "*.csv")])
    #reference_list = []
    #length = len(reference_list)

    if file:
        text_box = tk.Text(root, height=10, width=60, padx=15, pady=15)
        text_box.grid(row=4, columnspan=3)
        reader = csv.reader(file)
        for row in reader:
            reference_container.add_reference(csv_row_to_reference(row))
            #reference_list.append(row)
            text_box.insert(tk.END, str(row) + '\n')
        text_box.tag_configure("left", justify="left")
        # change index to 0 in the following after implementing a way to ignore title row
        result = reference_container.reference_string_at_index(1)
        #result = get_one_ref(reference_list)
        text_box.insert(tk.END, 'The first reference is:' + result + '\n')
        #firstReference.construct(result)

        # just for testing ReferenceList
        reference_container.debug_printout()

    #return reference_list


# Open pdf & extract text
def open_pdf_file():
    file = askopenfile(parent=root, mode="rb", title="Choose a file", filetypes=[("Pdf file", "*.pdf")])
    if file:
        read_pdf = PyPDF2.PdfFileReader(file)
        page = read_pdf.getPage(0)
        page_content = page.extractText()
        text_box = tk.Text(root, height=10, width=60, padx=15, pady=15)
        text_box.grid(row=4, columnspan=3)
        text_box.insert(1.0, page_content)
        text_box.tag_configure("left", justify="left")


def displayType(type):
    print("Type is: ", type)
    return type


# CSV Button


choose_csv_text = tk.StringVar()
choose_csv_btn = tk.Button(root, textvariable=choose_csv_text, command=lambda: open_csv_file(), font="Raleway",
                           bg="blue", fg="white", height=3, width=15)
choose_csv_text.set("Csv File")
choose_csv_btn.grid(column=2, row=2)

# Pdf Button
choose_pdf_text = tk.StringVar()
choose_pdf_btn = tk.Button(root, textvariable=choose_pdf_text, command=lambda: open_pdf_file(), font="Raleway",
                           bg="red", fg="white", height=3, width=15)
choose_pdf_text.set("Pdf File")
choose_pdf_btn.grid(column=0, row=2)

canvas = tk.Canvas(root, width=800, height=300)
canvas.grid(columnspan=3, rowspan=3)

#print(firstReference.reference_list)
root.mainloop()
