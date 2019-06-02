import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from tkinter import messagebox
import easygui

from NumberPlate_App import Main1
from NumberPlateDetection_DataExtraction import settings
import cv2
import os

print("start")

def fetchToAddress(key):
    flag = 0
    print("Key=",key)
    f = open(os.path.dirname(__file__)+'/Book123.csv',"r")
    #key = input("Enter key")
    a = f.read().split("\n")
    for line in a:
        l = line.split(",")
        #print(l)
        if l[0] == key:
            return l
        else:
            print("inside else")
            flag = 1
            print(flag)

    print("Outside",flag)
    if(flag == 1):
        print("flag=",flag)
        return 0

    f.close()

def process(image,):
    global plateno
    plateno = Main1.main123(image)

    print("Recongnizing numbers in the plate")

    print("hello"+plateno)

    details = fetchToAddress(plateno)
    print("Hii",details)

    if details == 0:
        easygui.msgbox("Data not found", title="not found")
        return details
    else:
        return details[0],details[1],details[2],details[3],details[4],details[5],details[6],details[7]

def sendMail():
    print("plate num",plateno)
    print("fetching Mail Address")
    k=fetchToAddress(plateno)

    print(k)

    if k == None:
        return "There are no details about this car number in our database"

    fromaddr = "carolpereira037@gmail.com"
    toaddr = k[6]

    #instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Test Mail"

    # string to store the body of the mail
    body = "Test Mail with Photo"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = "imgOriginalScene.png"
    attachment = open("imgOriginalScene.png", "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    #To change the payload into encoded form")
    p.set_payload((attachment).read())

    #"encode into base64")
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    print("Authentication")
    s.login(fromaddr, 'carol@1997')

    # Converts the Multipart msg into a string
    text = msg.as_string()

    print("sending the mail")
    s.sendmail(fromaddr, toaddr, text)
    print("mail sent")

    # messagebox.showinfo("Email Sent", "Mail has been sent successfully")

    easygui.msgbox("Mail has been sent successfully", title="Mail Sent")

    return 1
    # terminating the session

    cv2.waitKey(0)					# hold windows open until user presses a key
    cv2.destroyAllWindows()
    s.quit()
