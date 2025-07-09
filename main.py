import os
import pandas as pd
import numpy as np
from tkinter import *
from tkinter import filedialog
import tkinter.font as font
from functools import partial
from sklearn import datasets, linear_model 
import spacy
from PyPDF2 import PdfReader
import docx

nlp = spacy.load("en_core_web_sm")

class train_model:
    def train(self):
        data = pd.read_csv('training_dataset.csv')
        array = data.values

        for i in range(len(array)):
            if array[i][0] == "Male":
                array[i][0] = 1
            else:
                array[i][0] = 0

        df = pd.DataFrame(array)
        maindf = df[[0,1,2,3,4,5,6]]
        mainarray = maindf.values
        temp = df[7]
        train_y = temp.values

        self.mul_lr = linear_model.LogisticRegression(multi_class='multinomial', solver='newton-cg', max_iter=1000)
        self.mul_lr.fit(mainarray, train_y)

    def test(self, test_data):
        try:
            test_predict = list(map(int, test_data))
            y_pred = self.mul_lr.predict([test_predict])
            return y_pred[0]
        except Exception as e:
            print("Error in prediction:", e)


def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except:
        return ""

def extract_text_from_docx(docx_path):
    try:
        doc = docx.Document(docx_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except:
        return ""

def parse_resume(path):
    if path.endswith('.pdf'):
        text = extract_text_from_pdf(path)
    elif path.endswith('.docx'):
        text = extract_text_from_docx(path)
    else:
        text = ""

    doc = nlp(text)
    skills_keywords = ['python', 'java', 'sql', 'excel', 'machine learning', 'data analysis', 'communication']
    skills_found = set()

    for token in doc:
        if token.text.lower() in skills_keywords:
            skills_found.add(token.text.lower())

    entities = {ent.label_: ent.text for ent in doc.ents}

    parsed_data = {
        "Email": entities.get("EMAIL", "Not found"),
        "Phone Number": entities.get("PHONE", "Not found"),
        "Skills": ", ".join(skills_found) if skills_found else "Not found",
        "Education": entities.get("EDUCATION", "Not parsed") if "EDUCATION" in entities else "Not parsed"
    }

    return parsed_data

def check_type(data):
    if isinstance(data, (str, int)):
        return str(data).title()
    elif isinstance(data, (list, tuple)):
        return ", ".join(data)
    return str(data)

def prediction_result(top, aplcnt_name, cv_path, personality_values):
    top.withdraw()
    print("\n############# Candidate Entered Data #############\n")
    print(aplcnt_name.get(), cv_path, personality_values)

    personality = model.test(personality_values)
    data = parse_resume(cv_path)

    print("\n############# Parsed Resume Data #############\n")
    for key, val in data.items():
        print(f"{key} : {val}")

    result = Tk()
    result.geometry("{0}x{1}+0+0".format(result.winfo_screenwidth(), result.winfo_screenheight()))
    result.configure(background='White')
    result.title("Predicted Personality")

    titleFont = font.Font(family='Arial', size=40, weight='bold')
    Label(result, text="Result - Personality Prediction", foreground='green', bg='white', font=titleFont).pack(fill=BOTH)

    Label(result, text=f"Name: {aplcnt_name.get()}", bg='white').pack(fill=BOTH)
    Label(result, text=f"Age: {personality_values[1]}", bg='white').pack(fill=BOTH)
    for key, value in data.items():
        Label(result, text=f"{key}: {value}", bg='white').pack(fill=BOTH)
    Label(result, text=f"Predicted Personality: {personality}", bg='white').pack(fill=BOTH)

    Button(result, text="Exit", command=result.destroy).pack()
    result.mainloop()

def perdict_person():
    root.withdraw()
    top = Toplevel()
    top.geometry('700x500')
    top.configure(background='black')
    top.title("Apply For A Job")

    titleFont = font.Font(family='Helvetica', size=20, weight='bold')
    Label(top, text="Personality Prediction", foreground='red', bg='black', font=titleFont, pady=10).pack()

    Label(top, text="Applicant Name", bg='black', fg='white').place(x=70, y=130)
    Label(top, text="Age", bg='black', fg='white').place(x=70, y=160)
    Label(top, text="Gender", bg='black', fg='white').place(x=70, y=190)
    Label(top, text="Upload Resume", bg='black', fg='white').place(x=70, y=220)
    Label(top, text="Openness (1-10)", bg='black', fg='white').place(x=70, y=250)
    Label(top, text="Neuroticism (1-10)", bg='black', fg='white').place(x=70, y=280)
    Label(top, text="Conscientiousness (1-10)", bg='black', fg='white').place(x=70, y=310)
    Label(top, text="Agreeableness (1-10)", bg='black', fg='white').place(x=70, y=340)
    Label(top, text="Extraversion (1-10)", bg='black', fg='white').place(x=70, y=370)

    sName = Entry(top)
    sName.place(x=450, y=130, width=160)
    age = Entry(top)
    age.place(x=450, y=160, width=160)
    gender = IntVar()
    Radiobutton(top, text="Male", variable=gender, value=1).place(x=450, y=190)
    Radiobutton(top, text="Female", variable=gender, value=0).place(x=540, y=190)
    cv = Button(top, text="Select File", command=lambda: OpenFile(cv))
    cv.place(x=450, y=220, width=160)

    openness = Entry(top); openness.insert(0,'1-10'); openness.place(x=450, y=250, width=160)
    neuroticism = Entry(top); neuroticism.insert(0,'1-10'); neuroticism.place(x=450, y=280, width=160)
    conscientiousness = Entry(top); conscientiousness.insert(0,'1-10'); conscientiousness.place(x=450, y=310, width=160)
    agreeableness = Entry(top); agreeableness.insert(0,'1-10'); agreeableness.place(x=450, y=340, width=160)
    extraversion = Entry(top); extraversion.insert(0,'1-10'); extraversion.place(x=450, y=370, width=160)

    Button(top, text="Submit", bg='red', fg='white', command=lambda: prediction_result(top, sName, loc, (gender.get(), age.get(), openness.get(), neuroticism.get(), conscientiousness.get(), agreeableness.get(), extraversion.get()))).place(x=350, y=420, width=200)
    top.mainloop()

def OpenFile(button):
    global loc
    name = filedialog.askopenfilename(filetypes=(('Document', '*.docx'), ('PDF', '*.pdf'), ('All files', '*')))
    filename = os.path.basename(name)
    loc = name
    button.config(text=filename)
    return

if __name__ == "__main__":
    model = train_model()
    model.train()

    root = Tk()
    root.geometry('700x500')
    root.configure(background='white')
    root.title("Personality Prediction System")
    titleFont = font.Font(family='Helvetica', size=25, weight='bold')
    Label(root, text="Personality Prediction System", bg='white', font=titleFont, pady=30).pack()
    Button(root, text="Predict Personality", bg='black', fg='white', command=perdict_person).place(relx=0.5, rely=0.5, anchor=CENTER)
    root.mainloop()
