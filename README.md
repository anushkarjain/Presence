# Attendance using Speaker Identification and Facial Recognition

## SAMPLE IMAGES
### Home Page

![alt text](Misc/HomePageUI.jpg)

### Face Recognition Page

![alt text](Misc/FaceRecognitionUI.jpg)

### Speaker Identification Page

![alt text](Misc/SpeakerIdentificationUI.jpg)

#### Output.csv file

![alt text](Misc/output.jpg)

## ABOUT
A system that marks attendance is software for students studying in different institutes which can also be used in companies ,the knowledge is stored in Admin device who takes attendance, the scholar user can give attendance in their respective classes before entering the category. 
This system will also be beneficial in calculating eligibility criteria of attendance of a student. 
The aim of developing such a system is to computerize the traditional way of taking attendance. 
This software uses voice and face biometrics which gives authentication of attendance using very small data size and generate the report at the top of the session with the help of automated system. 
The system is developed as a Python application and GUI is implemented with Tkinter, and it will work for any teacher or faculty. 
LBPH (Local Binary Patterns Histograms) face recognizer Algorithm is used for face recognition and MFCC (Mel Frequency Cepstral Coefficient) + GMM (Gaussian Mixture Models) are used to implement Speaker Identification.


## INSTRUCTIONS
Follow the below steps to execute this project,
  - Download the repository.
  - Execute test.py file.
  - Install Required modules. 

Points to remember,
  - Change all the paths in code as per your directory.
  - Store your audio recorded for training in training_set and testing audio in testing_set Folder.
  - training_set_addition.txt use this file to append trained files and testing_set_addition.txt for appending test files.
  - Passwords get stored in password.txt, images while training the model are stored in TrainingImage folder
  - The data after registering is stored in StudentDetails.csv


 
