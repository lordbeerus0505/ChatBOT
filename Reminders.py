import time
import MySQLdb
import os

class Reminder:
	def SetReminder(self,username):

		db=MySQLdb.connect("localhost","root","","Login_DB")

		cursor=db.cursor()
		time=input("Enter the time of the event in DDMMYYHHMM: ")
		if len(time)!=10:
			time=input("Please reenter in the correct format.\nEnter the time of the event in DDMMYYHHMM: ")
		reminder=input("Enter the reminder description: ")
		cursor.execute("INSERT INTO Reminder VALUES(\""+time+"\",\""+reminder+"\",\""+username+ "\")")
		db.commit()
		print("Successfull saved a reminder")
		return
	def ShowReminder(self,username):

		db=MySQLdb.connect("localhost","root","","Login_DB")

		cursor=db.cursor()
		
		#start deleting the old reminders, before the current day but the program has to run everyday then
		today=time.strftime('%d%m')
		today=str(int(today)-100)
		
		cursor.execute("DELETE FROM Reminder WHERE Date LIKE \'%"+today+"%\'")
		db.commit()

		cursor.execute("SELECT * FROM Reminder WHERE username=\""+username+ "\"")
		results=cursor.fetchall()
		for res in results:
			date=res[0][0:2]+"/"+res[0][2:4]+"/"+res[0][4:6]+"    "+res[0][6:8]+":"+res[0][8:10]
			print("TIME: "+date)
			print("REMINDER: "+res[1]+"\n")

		#print(results)
	def RemindersToday(self,username):
		today = time.strftime('%d%m%y')#As long as the day matches were good to go

		db=MySQLdb.connect("localhost","root","","Login_DB")

		cursor=db.cursor()
		cursor.execute("SELECT * FROM Reminder WHERE username=\""+username+ "\"")
		results=cursor.fetchall()
		flag=0
		r=''
		for res in results:
			if res[0].find(today)!=-1:
				r=str(res[1])
				os.system('echo  "\a"')
				os.system('notify-send "Reminders Today: ' + r+'" -t 2000')
				flag=1
		if flag!=1:
			os.system('notify-send "No Reminders Today!"')
 
# rem=Reminder()
#rem.SetReminder("Abhidogg")
# rem.ShowReminder("Abhidogg")
