import os
import wave
import time
import pickle
import pyaudio
import warnings
import numpy as np
import pandas as pd
from sklearn import preprocessing
from scipy.io.wavfile import read
import python_speech_features as mfcc
from sklearn.mixture import GaussianMixture
from datetime import datetime
from datetime import date
import tkinter
from tkinter.ttk import *
from tkinter import Toplevel, messagebox
from PIL import ImageTk, Image
import csv
top = tkinter.Tk()
top.resizable(width=False, height=False)
top.title("Attendance System using Speaker Identification")
warnings.filterwarnings("ignore")

def markAttendance(name):
    with open("AttendanceSpeakerIdentification\Attendance_"+str(date.today())+".csv",'a+') as f:
        col_names = ['ID', 'Time']
        writer = csv.writer(f)
        writer.writerow(col_names)
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            nameList.append(name)
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')
      #time.sleep(4.0)
      


def calculate_delta(array):
   
    rows,cols = array.shape
    print(rows)
    print(cols)
    deltas = np.zeros((rows,20))
    N = 2
    for i in range(rows):
        index = []
        j = 1
        while j <= N:
            if i-j < 0:
              first =0
            else:
              first = i-j
            if i+j > rows-1:
                second = rows-1
            else:
                second = i+j 
            index.append((second,first))
            j+=1
        deltas[i] = ( array[index[0][0]]-array[index[0][1]] + (2 * (array[index[1][0]]-array[index[1][1]])) ) / 10
    return deltas


def extract_features(audio,rate):
       
    mfcc_feature = mfcc.mfcc(audio,rate, 0.025, 0.01,20,nfft = 1200, appendEnergy = True)    
    mfcc_feature = preprocessing.scale(mfcc_feature)
    print(mfcc_feature)
    delta = calculate_delta(mfcc_feature)
    combined = np.hstack((mfcc_feature,delta)) 
    return combined

name_var = tkinter.StringVar()
def record_audio_train():
    Name = name_var.get()   
    name_var.set("")
    popup_recordstart()
    for count in range(5): 
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        CHUNK = 512
        RECORD_SECONDS = 10
        device_index = 2
        audio = pyaudio.PyAudio()
        index = 1        
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,input_device_index = index,
                        frames_per_buffer=CHUNK)
        print ("recording started")
        Recordframes = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            Recordframes.append(data)
        if count == 4:
            popup_record()
        print ("recording stopped")
        stream.stop_stream()
        stream.close()
        audio.terminate()
        OUTPUT_FILENAME=Name+"-sample"+str(count)+".wav"
        WAVE_OUTPUT_FILENAME=os.path.join("AttendanceSpeakerIdentification\training_set",OUTPUT_FILENAME)
        trainedfilelist = open("AttendanceSpeakerIdentification\training_set_addition.txt", 'a')
        trainedfilelist.write(OUTPUT_FILENAME+"\n")
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(Recordframes))
        waveFile.close()
def popup_record():
    messagebox.showinfo("Attention!", "Recording has been finished!")

def popup_recordstart():
    messagebox.showinfo("Attention!", "Recording has started!")

def record_audio_test():
    popup_recordstart()
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 512
    RECORD_SECONDS = 10
    device_index = 2
    audio = pyaudio.PyAudio()
    index = 1        
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,input_device_index = index,
                    frames_per_buffer=CHUNK)
    print ("recording started")
    Recordframes = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        Recordframes.append(data)
    popup_record()
    print ("recording stopped")
    stream.stop_stream()
    stream.close()
    audio.terminate()
    OUTPUT_FILENAME="sample.wav"
    WAVE_OUTPUT_FILENAME=os.path.join("AttendanceSpeakerIdentification\testing_set",OUTPUT_FILENAME)
    trainedfilelist = open("AttendanceSpeakerIdentification\testing_set_addition.txt", 'a')
    trainedfilelist.write(OUTPUT_FILENAME+"\n")
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(Recordframes))
    waveFile.close()

def train_model():

    source   = "AttendanceSpeakerIdentification\\training_set\\"   
    dest = "AttendanceSpeakerIdentification\trained_models\\"
    train_file = "AttendanceSpeakerIdentification\training_set_addition.txt"        
    file_paths = open(train_file,'r')
    count = 1
    features = np.asarray(())
    for path in file_paths:    
        path = path.strip()   
        print(path)

        sr,audio = read(source + path)
        print(sr)
        vector   = extract_features(audio,sr)
        
        if features.size == 0:
            features = vector
        else:
            features = np.vstack((features, vector))

        if count == 5:    
            gmm = GaussianMixture(n_components = 6, max_iter = 200, covariance_type='diag',n_init = 3)
            gmm.fit(features)
            
            # dumping the trained gaussian model
            picklefile = path.split("-")[0]+".gmm"
            pickle.dump(gmm,open(dest + picklefile,'wb'))
            print('+ modeling completed for speaker:',picklefile," with data point = ",features.shape)   
            features = np.asarray(())
            count = 0
        count = count + 1


def test_model():

    source   = "AttendanceSpeakerIdentification\\testing_set\\"  
    modelpath = "AttendanceSpeakerIdentification\trained_models\\"
    test_file = "AttendanceSpeakerIdentification\testing_set_addition.txt"       
    file_paths = open(test_file,'r')
     
    gmm_files = [os.path.join(modelpath,fname) for fname in
                  os.listdir(modelpath) if fname.endswith('.gmm')]
     
    #Load the Gaussian gender Models
    models    = [pickle.load(open(fname,'rb')) for fname in gmm_files]
    speakers   = [fname.split("\\")[-1].split(".gmm")[0] for fname 
                  in gmm_files]
     
    # Read the test directory and get the list of test audio files 
    for path in file_paths:   
         
        path = path.strip()   
        print(path)
        sr,audio = read(source + path)
        vector   = extract_features(audio,sr)
         
        log_likelihood = np.zeros(len(models)) 
        
        for i in range(len(models)):
            gmm    = models[i]  #checking with each model one by one
            scores = np.array(gmm.score(vector))
            log_likelihood[i] = scores.sum()
        winner = np.argmax(log_likelihood)
    markAttendance(speakers[winner])
    df = pd.read_csv("AttendanceSpeakerIdentification\\Attendance_"+str(date.today())+".csv")
    messagebox.showinfo("Attendance", speakers[winner]+", your attendance is marked ")

def checkID(name):
    print(name)

top.geometry("1795x1148")



def openNewWindow():    
    newWindow = Toplevel(top)    
    newWindow.title("new")
    
    Label(newWindow).pack()

background= ImageTk.PhotoImage(file="path to background image")
canvas= tkinter.Canvas(top, width=400, height= 200)
canvas.pack(expand=True, fill= "both")
canvas.create_image(0,0,image=background, anchor="nw")

def remove(event):
    name_entry.delete(0, tkinter.END)
    
name_entry = tkinter.Entry(canvas,fg = '#808080', textvariable = name_var, font=('Arial',35,'normal'))
name_entry.insert(0, "EN18CS301XXX")
name_entry.bind('<FocusIn>', remove)
name_entry.place(x=335 ,y=178)
s = tkinter.Button(canvas, bg= "#37371F",fg= "white", text="Record Train Model", command=record_audio_train, width=32, height=3, font=('Product Sans',15,'bold'))
s.place(x=107, y=296)
x = tkinter.Button(canvas,bg="#37371F",fg= "white", text="Train Model", command=train_model,width=32,height=3,font=('Product Sans',15,'bold'))
x.place(x=107,y=439)
w = tkinter.Button(canvas,bg="#37371F",fg= "white", text="Record Test Model", command=record_audio_test, width=32,height=3,font=('Product Sans',15,'bold'))
w.place(x=518,y=296)
y = tkinter.Button(canvas, bg="#37371F",fg= "white", text="Predict", command=test_model, width=32,height=3,font=('Product Sans',15,'bold'))
y.place(x=518,y=439)
top.mainloop()
        

