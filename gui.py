import tkinter as tk
import json
import os

# -----------------------GLOBAL DATA---------------------
students={}

# -----------------------GUI SETUP---------------------------
root=tk.Tk()
root.title('Students MarkSheet')
root.geometry('500x600')

#----------------------FONT STYLES---------------------
FONT_LABEL = ("Arial", 11)
FONT_ENTRY = ("Arial", 11)
FONT_TEXT  = ("Consolas", 11)
FONT_BTN   = ("Arial", 10, "bold")

#Labels and Entries
studentID=tk.Label(root,text='Student ID',font=FONT_LABEL)
studentID.grid(row=0,column=0,padx=10, pady=5)
input_ID=tk.Entry(root,font=FONT_ENTRY)
input_ID.grid(row=0,column=1)

name=tk.Label(root,text='Name',font=FONT_LABEL)
name.grid(row=1 ,column= 0,padx=10, pady=5)
input_name=tk.Entry(root,font=FONT_ENTRY)
input_name.grid(row=1 ,column=1)

subject=tk.Label(root,text='Subject',font=FONT_LABEL)
subject.grid(row=2,column=0,padx=10, pady=5)
input_subject=tk.Entry(root,font=FONT_ENTRY)
input_subject.grid(row=2,column=1)

marks=tk.Label(root,text='Marks',font=FONT_LABEL)
marks.grid(row= 4,column=0 ,padx=10, pady=5)
input_marks=tk.Entry(root,font=FONT_ENTRY)
input_marks.grid(row=4 ,column=1 )

output_text=tk.Text(root,height=10, width=40,font=FONT_TEXT)
output_text.grid(row=5,column=2, padx=20, pady=10)

# -----------------------FUNCTIONS---------------
#Displays all students and their marks

def display_students():
    output_text.delete("1.0",tk.END)
    
    if not students:
        output_text.insert(tk.END, "No students available\n")
        return
    
    for student_id,details in students.items():
        output_text.insert(tk.END,f"studentID:{student_id} added successfully\n")
        output_text.insert(tk.END,f"Name:{details['name']}\n")
        if not details["marks"]:
            output_text.insert(tk.END,"marks not added\n")
        else:  
            output_text.insert(tk.END,"marks\n")  
            for subject, mark in details["marks"].items():
                output_text.insert(tk.END,f"{subject}:{mark}")

    output_text.insert(tk.END,"-" * 30 + "\n")

# Adds a new student    
def add_student():
    stu_id=input_ID.get()
    name=input_name.get()

    if stu_id == "" or name == "":
        output_text.insert(tk.END,"All fields are required\n")
        return
    
    if not stu_id.isdigit():
        output_text.insert(tk.END,"Student ID must be a number\n")
        return

    student_id=int(stu_id)

    if student_id in students:
        output_text.insert(tk.END,"Student already exists\n")
        return
    
    students[student_id]={"name":name,"marks":{}}
    save_to_file()
    display_students() 
    clear_entries()

#update subject and its marks for a student
def update_marks():
    stu_id = input_ID.get()
    subject = input_subject.get()
    marks_str = input_marks.get()

    if stu_id == "" or subject == "" or marks_str== "":
        output_text.insert(tk.END, "All fields are required\n")
        return

    if not stu_id.isdigit() or not marks_str.isdigit():
        output_text.insert(tk.END, "Student ID and Marks must be numbers\n")
        return

    student_id = int(stu_id)
    mark = int(marks_str)

    if student_id not in students:
        output_text.insert(tk.END, "Student not found\n")
        return

    students[student_id]["marks"][subject] = mark
    save_to_file()
    display_students()
    clear_entries()

def save_to_file():
    with open("students.json", "w") as f:
        json.dump(students, f)

def load_from_file():
    global students
    if os.path.exists("students.json"):
        with open("students.json", "r") as f:
            data = json.load(f)
            students = {int(k): v for k, v in data.items()}

def clear_entries():
    input_ID.delete(0, tk.END)
    input_name.delete(0, tk.END)
    input_subject.delete(0, tk.END)
    input_marks.delete(0, tk.END)

"shows student with highest marks"
def best_performer():
    output_text.delete("1.0", tk.END)

    best_id = None
    best_total = 0

    for sid, details in students.items():
        total = sum(details["marks"].values())
        if total > best_total:
            best_total = total
            best_id = sid

    if best_id is None:
        output_text.insert(tk.END, "No marks added yet\n")
        return

    output_text.insert(
        tk.END,
        f"Best Performer:\nID: {best_id}\nName: {students[best_id]['name']}\nTotal Marks: {best_total}\n"
    )
# best_performer()

"displays failed students"
def failed_students():
    output_text.delete("1.0", tk.END)

    failed = False

    for sid, details in students.items():
        for marks in details["marks"].values():
            if marks < 35:
                output_text.insert(tk.END, f"ID: {sid}, Name: {details['name']}\n")
                failed = True
                break

    if not failed:
        output_text.insert(tk.END, "No failed students\n")
# failed_students()        

# ----------------------------BUTTONS---------------------
add_button=tk.Button(root,text='Add',font=FONT_BTN, width=12, command=add_student).grid(row=6 ,column=1,pady=5 )
update_button=tk.Button(root,text='Update',font=FONT_BTN, width=12, command=update_marks).grid(row=6,column= 2,pady=5)
performer_button=tk.Button(root,text='BestPerformer',font=FONT_BTN, width=12, command=best_performer).grid(row= 7,column=1,pady=5)
fail_button=tk.Button(root,text='FailedStudents',font=FONT_BTN, width=12, command=failed_students).grid(row= 7,column= 2,pady=5)
clear_button=tk.Button(root,text='clear',font=FONT_BTN, width=12, command=clear_entries).grid(row= 7,column= 3,pady=5)

load_from_file()
display_students()

root.mainloop()