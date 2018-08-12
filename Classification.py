import nltk
import re
import string
import os
import time
from textblob.classifiers import NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from Reminders import Reminder
from Calculator import Calculate
from GOOGLEscrape import Search
from Login import Login
from TODO import Todo
from Mails import Mail

# '''
# '''
username=''


counter=1
name=''
def main():
# Basic response to begin conversation
    #first perform a login
    obj=Reminder()
    mailobj=Mail()
    global counter 
    global name
    global username
    log=Login()
    name,username=log.logger()
    #print("USERNAME="+username)
    name= " ".join(re.findall("[a-zA-Z0-9]+", str(name)))
    if name !='':
        counter=0
    
    if counter==1:#Add name to database yet to implement
        print("Welcome to ChatterBox. What is your name?")
        name=input();
        print("Hello "+name+"\n I'm Alice")

    if counter==0:
        print('Hello '+name+". Welcome back. Here are todays reminders...")
        #os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (1, 500))
        
        time.sleep(0.5)
        obj.RemindersToday(username)
        print("Here are your emails")

        time.sleep(2)
        mailobj.LatestMails()
        time.sleep(1)
        print("How can I help you?")
       #reception of inputs, for each input, perform processing to understand what the input requires.
   
    Statement=input()
    Statement=Statement.lower()
   # print(Statement)
    reply=Statement
    counter = 0
    global cond
    cond=0


#start giving replies
    while process(Statement)!=-1:
        #preprocessing done
        Statement=input("How can I help you?\n")
        #print("Loading...")

def mail(sentence):
    W=open("mails.txt","r")
    contents=W.read().split("\n")
    for i in contents:
        if i in sentence:
            #positive response means send mail or some mail action
            if sentence.find("show")>=0 or sentence.find("display")>=0:
                #have to show mails... show latest 5 mails...
                obj=Mail()
                obj.show_mails()
            else:
                to=input("Enter to address")
                From=input("Enter from address")
                subject=input("Enter subject of message")
                body=input("Enter body of message")
                print("Thank You, Your request is being processed")
                obj=Mail()
                obj.send_mail(From,to,subject,body)
def todo(sentence):
    W=open("todo.txt","r")
    contents=W.read().split("\n")
    X=open("search.txt","r")
    contents2=X.read().split("\n")
    for i in contents2:
        if i in sentence:
            return False
    flag=0
    for i in contents:
        if i in sentence:
            flag=1
    if flag==0:
        return False
    obj=Todo()
    
    # no google search for death note or something so now jot it down or display or delete
    if sentence.find("show")!=-1 or sentence.find("give")!=-1 or sentence.find("display")!=-1 or sentence.find("see")!=-1:
        
        obj.view_items(username)
        return True
    elif sentence.find("remove")!=-1 or sentence.find("delete")!=-1 or sentence.find("complete")!=-1:
        
        for i in sentence:
            x=obj.delete_item(i,username)
            if x==True:
                return True
    else:
        print("Creating a note")
        obj.create_item(username)
        return True


def reminder(sentence):
    w=open("Reminders.txt","r")
    contents=w.read().split("\n")
    X=open("search.txt","r")
    contents2=X.read().split("\n")
    for i in contents2:
        if i in sentence:
            return False
    flag=0
    for i in contents:
        if i in sentence:
            flag=1
    if flag==0:
        return False
    rem=Reminder()
    if sentence.find("show")!=-1 or sentence.find("give")!=-1 or sentence.find("display")!=-1 or sentence.find("see")!=-1:
        print("Inside show rem")
        rem.ShowReminder(username)
        return True
    else:
        rem.SetReminder(username)
        return True

def process(sentence):
    flag=0 #reply hasnt been generated
    with open("Train.json",'r') as fp:
        cl=NaiveBayesClassifier(fp,format="json")
    stop_words=set(stopwords.words('english'))

    #for now use this strategy--------------------------------------------
    sentence=sentence.lower()
    #----------------------------------------------------------------

    word_tokens = word_tokenize(sentence)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    #print(str(filtered_sentence)+"sent")
    prob_dist = cl.prob_classify(sentence)
    pd=prob_dist.max()
    prob_greet_welcome=prob_dist.prob("greetings-welcome")
    prob_greet_question=prob_dist.prob("greetings-question")


    calc=Calculate()
    regex=re.compile(r'[+*%]')
    if flag==0:
        if  re.findall(r'[+/*-]',sentence):
            for i in sentence:
                if i in string.ascii_letters or i =='.' or i=='?' or i=='!':
                    sentence=sentence.replace(i,"")
            #print(sentence)
            calc.calc(sentence)
            flag=1
            return
    
    if reminder(sentence)!=False:
        return
    if todo(sentence)!=False:
        return
    if mail(sentence)!=False:
        return

    obj = Search()
    
    if flag==0:#Search for meaning on google
        w=open("meaning.txt","r")
        contents=[]
        for i in w.read().split("\n"):
            contents.append(i)
        #print(str(contents)+"contents")
        for i in contents:
            if i in sentence:
                print(i)
                sentence=sentence.replace(i,"")
                obj.main(str(sentence),2)
                flag=1
                return

    if flag==0:#PLAY from youtube
        w=open("play.txt","r")
        contents=[]
        for i in w.read().split():
            contents.append(i)
        for i in contents:
            if i in sentence:
                sentence=sentence.replace(i,"")
                obj.main(str(sentence), 1)
                flag=1
                return

    
    if flag==0:#Search from google and render results
        w = open("search.txt", "r")
        contents = []
        for i in w.read().split():
            contents.append(i)
        for i in contents:
            if i in sentence:#searching is the priority
                sentence=sentence.replace(i,"")
                obj.main(str(sentence),0)
                flag=1

    if flag==0:
        if prob_greet_welcome>0.5:#high threshold for greet
            print("Hello again. I can perform basic Language processing. Why dont we start by you asking me questions")
        elif prob_greet_question>0.4:
            f=open("Intro.txt","r")
            contents=f.read()
            print(contents)

        #check irrelevance
        # print(pd)
        # print("WELCOME\t\t\t\tQUESTION\t\t\t\t\tCost")
        # print(prob_greet_welcome,prob_greet_question)

    #tokens=nltk.word_tokenize(sentence)
    #print(tokens)
    #tag=nltk.pos_tag(tokens)
    #print(tag)
    # if exit return -1

    # checks if customers wants to add to the TODO list






    






main()