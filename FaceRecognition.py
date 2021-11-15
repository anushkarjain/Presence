import tkinter
from tkinter import *
from tkinter import messagebox as mess
from tkinter import ttk
import tkinter.simpledialog as tsd
import os
import cv2
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time

#contact
def contact():
    mess._show(title="Contact Me",message="If you find anything weird or you need any help contact me on anushka.rjain@gmail.com")


#clearbutton
def clear():
    txt.delete(0, 'end')
    txt2.delete(0, 'end')

#Check for correct Path
def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

#check for haarcascade file
def check_haarcascadefile():
    exists = os.path.isfile("AttendanceFaceRecognition\haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Haarcascade file missing', message='some file is missing.')
        window.destroy()

#check the password for change the password
def save_pass():
    assure_path_exists("AttendanceFaceRecognition\Password/")
    exists1 = os.path.isfile("AttendanceFaceRecognition\Password\password.txt")
    if exists1:
        tf = open("AttendanceFaceRecognition\Password\password.txt", "r")
        str = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Password not set', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='Null Password Entered', message='Password not set.Please try again!')
        else:
            tf = open("AttendanceFaceRecognition\Password\password.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered!', message='New password was registered successfully!')
            return
    op = (old.get())
    newp= (new.get())
    nnewp = (nnew.get())
    if (op == str):
        if(newp == nnewp):
            txf = open("AttendanceFaceRecognition\Password\password.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error', message='Confirm new password again!!!')
            return
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')
        return
    mess._show(title='Password Changed', message='Password changed successfully!!')
    master.destroy()

#change password
def change_pass():
    global master
    master = tkinter.Tk()
    master.geometry("400x160")
    master.resizable(False,False)
    master.title("Change Admin Password")
    master.configure(background="white")
    lbl4 = tkinter.Label(master,text='    Enter Old Password',bg='white',font=('times', 12, ' bold '))
    lbl4.place(x=10,y=10)
    global old
    old=tkinter.Entry(master,width=25 ,fg="black",relief='solid',font=('times', 12, ' bold '),show='*')
    old.place(x=180,y=10)
    lbl5 = tkinter.Label(master, text='   Enter New Password', bg='white', font=('times', 12, ' bold '))
    lbl5.place(x=10, y=45)
    global new
    new = tkinter.Entry(master, width=25, fg="black",relief='solid', font=('times', 12, ' bold '),show='*')
    new.place(x=180, y=45)
    lbl6 = tkinter.Label(master, text='Confirm New Password', bg='white', font=('times', 12, ' bold '))
    lbl6.place(x=10, y=80)
    global nnew
    nnew = tkinter.Entry(master, width=25, fg="black", relief='solid',font=('times', 12, ' bold '),show='*')
    nnew.place(x=180, y=80)
    cancel=tkinter.Button(master,text="Cancel", command=master.destroy, fg="white" , bg="#13059c", height=1,width=25 , activebackground = "white" ,font=('times', 10, ' bold '))
    cancel.place(x=200, y=120)
    save1 = tkinter.Button(master, text="Save", command=save_pass, fg="black", bg="#00aeff", height = 1,width=25, activebackground="white", font=('times', 10, ' bold '))
    save1.place(x=10, y=120)
    master.mainloop()

#ask for password
def psw():
    assure_path_exists("AttendanceFaceRecognition\Password/")
    exists1 = os.path.isfile("AttendanceFaceRecognition\Password\password.txt")
    if exists1:
        tf = open("AttendanceFaceRecognition\Password\password.txt", "r")
        str_pass = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("AttendanceFaceRecognition\Password\password.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if (password == str_pass):
        TrainImages()

    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')


#$$$$$$$$$$$$$
def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', 'ID', 'NAME']
    assure_path_exists("AttendanceFaceRecognition/StudentDetails/")
    assure_path_exists("AttendanceFaceRecognition/TrainingImage/")
    serial = 0
    exists = os.path.isfile("AttendanceFaceRecognition\StudentDetails\StudentDetails.csv")
    if exists:
        with open("AttendanceFaceRecognition\StudentDetails\StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open("AttendanceFaceRecognition\StudentDetails\StudentDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()
    Id = (txt.get())
    name = (txt2.get())
    if ((name.isalpha()) or (' ' in name)):
        cam = cv2.VideoCapture(0)
        harcascadePath = "AttendanceFaceRecognition\haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.05, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # incrementing sample number
                sampleNum = sampleNum + 1
                # saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("AttendanceFaceRecognition\TrainingImage\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                            gray[y:y + h, x:x + w])
                # display the frame
                cv2.imshow('Taking Images', img)
            # wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Taken for ID : " + Id
        row = [serial, '', Id, '', name]
        with open('AttendanceFaceRecognition\StudentDetails\StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
    else:
        if (name.isalpha() == False):
            res = "Enter Correct name"
            message.configure(text=res)

def TrainImages():
    check_haarcascadefile()
    assure_path_exists("AttendanceFaceRecognition\Password/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "AttendanceFaceRecognition\haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("AttendanceFaceRecognition\TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!')
        return
    recognizer.save("AttendanceFaceRecognition\Password\Trainner.yml")
    mess.showinfo("Popup","Your Profile Is Saved Successfully")

def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empty face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

def TrackImages():
    check_haarcascadefile()
    assure_path_exists("AttendanceFaceRecognition/")
    assure_path_exists("AttendanceFaceRecognition\StudentDetails/")
    msg = ''
    i = 0
    j = 0
    recognizer =cv2.face.LBPHFaceRecognizer_create() 
    exists3 = os.path.isfile("AttendanceFaceRecognition\Password\Trainner.yml")
    if exists3:
        recognizer.read("AttendanceFaceRecognition\Password\Trainner.yml")
    else:
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return
    harcascadePath = "AttendanceFaceRecognition\haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['ID', 'Name', 'Date', 'Time']
    exists1 = os.path.isfile("AttendanceFaceRecognition\StudentDetails\StudentDetails.csv")
    if exists1:
        df = pd.read_csv("AttendanceFaceRecognition\StudentDetails\StudentDetails.csv")
    else:
        mess._show(title='Details Missing', message='Students details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID = str(ID)
                ID = ID[1:-1]
                ID = ID.replace("'", "")
                bb = str(aa)
                bb = bb[2:-2]
                attendance = [str(ID), bb, str(date), str(timeStamp)]

            else:
                Id = 'Unknown'
                bb = str(Id)
            cv2.putText(im, str(bb), (x, y + h), font, 1, (0, 251, 255), 2)
        cv2.imshow('Taking Attendance', im)
        if (cv2.waitKey(1) == ord('q')):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile("AttendanceFaceRecognition\Attendance_" + str(datetime.date.today()) + ".csv")
    if exists:
        with open("AttendanceFaceRecognition\Attendance_" + str(datetime.date.today()) + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(attendance)
        csvFile1.close()
    else:
        with open("AttendanceFaceRecognition\Attendance_" + str(datetime.date.today()) + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            writer.writerow(attendance)
        csvFile1.close()
    csvFile1.close()
    cam.release()
    cv2.destroyAllWindows()
    mess.showinfo("Attendance", "Attendance Marked Successfully")

#Front End===========================================================

window = tkinter.Tk()
window.title("Face Recognition Based Attendance System")
window.geometry("1480x879")
window.resizable(True,True)
window.configure(background='#355454')
                 
background= ImageTk.PhotoImage(file="Path to background image file")
canvas= tkinter.Canvas(window, width=400, height= 200)
canvas.pack(expand=True, fill= "both")
canvas.create_image(0,0,image=background, anchor="nw")

#Help menubar----------------------------------------------
menubar=Menu(window)
help=Menu(menubar,tearoff=0)
help.add_command(label="Change Password!",command=change_pass)
help.add_command(label="Contact Us",command=contact)
help.add_separator()
menubar.add_cascade(label="Help",menu=help)

#This line will attach our menu to window
window.config(menu=menubar)

#main window------------------------------------------------

#registration frame
txt = tkinter.Entry(window,width=22 ,fg="black",highlightcolor="white",font=('IBM Plex Sans', 18, ' bold '), borderwidth = 0)
txt.place(x=1051, y=279)

txt2 = tkinter.Entry(window,width=22 ,fg="black",highlightcolor="white",font=('IBM Plex Sans', 18, ' bold '), borderwidth = 0)
txt2.place(x=1051, y=359)

message = tkinter.Label(window, text="" ,bg="#90BE6D" ,fg="#37371F"  ,width=2, height=1, activebackground = "yellow" ,font=('IBM Plex Sans', 20, ' bold '))
message.place(x=1190, y=750)

#Display total registration----------
res=0
exists = os.path.isfile("AttendanceFaceRecognition\StudentDetails\StudentDetails.csv")
if exists:
    with open("AttendanceFaceRecognition\StudentDetails\StudentDetails.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res = res + 1
    res = (res // 2) - 1
    csvFile1.close()
else:
    res = 0
message.configure(text=str(res))

#BUTTONS----------------------------------------------

clearButton = tkinter.Button(window, text="Clear", command=clear, fg="#37371F", bg="#EAEFBD", width=10, activebackground = "#EAEFBD", font=('IBM Plex Sans', 12, ' bold '), borderwidth = 0)
clearButton.place(x=1311, y=428)

takeImg = tkinter.Button(window, text="Take Images", command=TakeImages, fg="#37371F", bg="#EAEFBD", height=1, activebackground = "#EAEFBD", font=('IBM Plex Sans', 16, ' bold '), borderwidth = 0)
takeImg.place(x=788, y=610)

trainImg = tkinter.Button(window, text="Save Profile", command=psw, fg="#37371F", bg="#EAEFBD", height=1, activebackground = "#EAEFBD", font=('IBM Plex Sans', 17, ' bold '), borderwidth = 0)
trainImg.place(x=1175, y=600)

trackImg = tkinter.Button(window, text="Take Attendance", command=TrackImages, fg="#37371F", bg="#EAEFBD", height=1, activebackground = "#EAEFBD" ,font=('IBM Plex Sans', 16, ' bold '), borderwidth = 0)
trackImg.place(x=956,y=687)

window.mainloop()
