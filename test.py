import os
import tkinter
from tkinter.ttk import *
from tkinter import messagebox
from PIL import ImageTk, Image
import pandas as pd
from datetime import date

def compare():
    speaker = pd.read_csv("AttendanceSpeakerIdentification\attendance_"+str(date.today())+".csv")
    face = pd.read_csv("AttendanceFaceRecognition\attendance_"+str(date.today())+".csv")
    output = pd.merge(face, speaker, on='ID', how='left', indicator=True)
    output1 = output.drop(['Time_x', '_merge'], axis = 1)
    output1.to_csv("path to csv file where you want to store final attendance information.")


top = tkinter.Tk()
top.resizable(width=False, height=False)
top.title("Attendance System using Facial and speaker Recognition")

def run_si():
    os.system('SpeakerIdentification.py')

def run_rd():
    os.system('FaceRecognition.py')
    
def openCSV():
    compare()
    os.system('start "excel" "enter the path of file where final attendance is stored"')
    

def about_us():
    messagebox.showinfo("About Us", "Developed By: \n Anushka Jain\n Anushka Lalwani \n Apoorva Rathore :)")

top.geometry("1480x879")

bg1= ImageTk.PhotoImage(file="path to background image file")
canvas= tkinter.Canvas(top, width=400, height= 200)
canvas.pack(expand=True, fill= "both")
canvas.create_image(0,0,image=bg1, anchor="nw")

s = tkinter.Button(top,bg="#ea9010", fg="white", text="Face Recognition", command=run_rd,width=18,height=1, activebackground = "#ea9010", font=('IBM Plex Sans',15,'normal'), borderwidth=0)
s.place(x=1188,y=447)
x = tkinter.Button(top,bg="#ea9010", fg="white",text="speaker Recognition", command=run_si,width=18,height=1,activebackground = "#ea9010", font=('IBM Plex Sans',15,'normal'), borderwidth=0)
x.place(x=1188,y=522)
z = tkinter.Button(top, bg="#ea9010",fg="white",text="Show Attendance", command=openCSV,width=18,height=1,activebackground = "#ea9010", font=('IBM Plex Sans',15,'normal'), borderwidth=0)
z.place(x=1188,y=595)
quitWindow = tkinter.Button(top, text="Quit", command=top.destroy, fg="white", bg="#D22B2B", width=7, height=1, activebackground = "#D2042D", font=('IBM Plex Sans', 15, ' bold '), borderwidth=0)
quitWindow.place(x=6, y=820)
aboutus = tkinter.Button(top, text="About Us", command=about_us, fg="white", bg="#D22B2B", width=8, height=1, activebackground = "#D2042D", font=('IBM Plex Sans', 15, ' bold '), borderwidth=0)
aboutus.place(x=112, y=820)

top.mainloop()