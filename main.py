import tkinter as tk
from tkinter.filedialog import askopenfile
import csv
import PyPDF2
from Reference import Reference, ReferenceList
"""
tkinter toolkit used for quick GUI setup. Documentation available at https://docs.python.org/3/library/tk.html
Csv files were used for testing working with references before extracting them directly from pdf files becomes
possible. Documentation: https://docs.python.org/3/library/csv.html
PyPDF2 allows for reading and extracting text from pdf files, user guide: https://pypdf2.readthedocs.io/en/latest/
"""

# GUI setup
# tkinter works using a canvas separated into a grid of columns and rows
# use .grid to attach widgets to canvas
root = tk.Tk()
canvas = tk.Canvas(root, height=700, width=800)
canvas.grid(columnspan=6, rowspan=12)

# Header
header = tk.Label(root, text="ICT Thesis Classifier App Prototype", font="Raleway")
header.grid(columnspan=3, column=1, row=0)

# Mid Label
mid_label = tk.Label(root, text="Input reference index", font="Raleway")
mid_label.grid(columnspan=3, column=1, row=4)

# Bottom Label
mid_label = tk.Label(root, text="Enter word to search", font="Raleway")
mid_label.grid(columnspan=3, column=1, row=6)

# Textbox
text_box = tk.Text(root, height=14, width=75, padx=15, pady=15)
text_box.grid(row=8, columnspan=6)
text_box.tag_configure("left", justify="left")

reference_container = ReferenceList()
ref_list = []
# firstReference = ReferenceList()


# Removes stored elements from list, used when switching to a different file
def reset_reference_list():
    reference_container.references.clear()
    text_box.delete("1.0", "end")
    ref_list.clear()


def get_one_ref(ref_list):
    for index in range(1, len(ref_list)):
        type = ref_list[index][0]

    return type


def csv_row_to_reference(row) -> Reference:
    # bandaid solution, csv reader returns the first row as a list of 3, others as list of 1
    if len(row) == 1:
        row = str(row[0]).split(',')
    return Reference(type= row[0], author= row[1], year_published= row[2])


# Open Csv file & extract rows into a list.
# List used for ease of testing basic functionality, splitting the row elements into class attributes
# a work in progress
def open_csv_file():
    file = askopenfile(parent=root, mode="r", title="Choose a file", filetypes=[("Csv file", "*.csv")])
    if file:
        reader = csv.reader(file)
        for row in reader:
            reference_container.add_reference(csv_row_to_reference(row))
            ref_list.append(row)
        text_box.insert(tk.END,"File Loaded" + '\n' + "References found: " + str(len(ref_list)))
        # change index to 0 in the following after implementing a way to ignore title row
        result = reference_container.reference_string_at_index(1)

        # just for testing ReferenceList
        reference_container.debug_printout()
        return ref_list

    # return reference_list


# Open pdf & extract text
# Testing basic text extraction functionality from pdf files
# Should have logic to extract only the reference list of a thesis in the future, and then
# removing the need for csv files
def open_pdf_file():
    file = askopenfile(parent=root, mode="rb", title="Choose a file", filetypes=[("Pdf file", "*.pdf")])
    if file:
        read_pdf = PyPDF2.PdfFileReader(file)
        page = read_pdf.getPage(0)
        page_content = page.extractText()
        text_box.insert(1.0, page_content)
        text_box.tag_configure("left", justify="left")


def display_type(type):
    print("Type is: ", type)
    return type


# Displays all rows extracted with the open_csv_file function in the GUI text field
def display_all_references():
    text_box.delete("1.0", "end")
    for row in ref_list:
        text_box.insert(tk.END, str(row) + '\n')


# Displays a row of specified index in the GUI text field
def display_ref_index():
    text_box.delete("1.0", "end")
    input1 = int(input_box1.get())
    try:
        text_box.insert(tk.END, ref_list[input1])
    except IndexError:
        text_box.insert(tk.END, "Invalid Choice")


# Takes input to search extracted rows for keywords
# Function and search logic currently incomplete
def display_search_result():
    text_box.delete("1.0", "end")
    input2 = input_box2.get()


# Interactive tkinter widgets

# Input Box
input_box1 = tk.Entry(root)
input_box1.grid(column=2, row=5)

input_box2 = tk.Entry(root)
input_box2.grid(column=2, row=7)

# Display Selected Index Button
selected_text = tk.StringVar()
selected_btn = tk.Button(root, textvariable=selected_text, command=lambda: display_ref_index(), font="Raleway",
                         bg="white",fg="black", height=1, width=8)
selected_text.set("Select")
selected_btn.grid(column=3, row=5)

# Display Selected Search
searched_text = tk.StringVar()
searched_btn = tk.Button(root, textvariable=searched_text, command=lambda: display_search_result(), font="Raleway",
                         bg="white",fg="black", height=1, width=8)
searched_text.set("Select")
searched_btn.grid(column=3, row=7)

# CSV Button
choose_csv_text = tk.StringVar()
choose_csv_btn = tk.Button(root, textvariable=choose_csv_text, command=lambda: open_csv_file(), font="Raleway",
                           bg="green", fg="white", height=2, width=10)
choose_csv_text.set("Csv File")
choose_csv_btn.grid(column=2, row=2)

# Pdf Button
choose_pdf_text = tk.StringVar()
choose_pdf_btn = tk.Button(root, textvariable=choose_pdf_text, command=lambda: open_pdf_file(), font="Raleway",
                           bg="red", fg="white", height=2, width=10)
choose_pdf_text.set("Pdf File")
choose_pdf_btn.grid(column=0, row=2)

# Display All References
display_all_text = tk.StringVar()
display_all_btn = tk.Button(root, textvariable=display_all_text, command=lambda: display_all_references(), font="Raleway",
                            bg ="white", fg="black", height=2, width=10)
display_all_text.set("All Ref.")
display_all_btn.grid(column=0, row=6)

# Reset Button
reset_btn_text = tk.StringVar()
reset_btn = tk.Button(root, textvariable=reset_btn_text, command=lambda: reset_reference_list(), font="Raleway",
                      bg="gray", fg="black", height=2, width=10)
reset_btn_text.set("Clear")
reset_btn.grid(column=4, row=2)

root.mainloop()
