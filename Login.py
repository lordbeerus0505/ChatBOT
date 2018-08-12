import MySQLdb
import re
import getpass



#Reading Username and Password from the user
class Login:
	name=''
	uname=[]
	password=[]
	db=''
	cursor=''
	def register(self):
		user=input("Enter new Username: ")
		global name
		global uname
		global password
		global db
		global cursor
		log=Login()

		db=MySQLdb.connect("localhost","root","","Login_DB")

		cursor=db.cursor()
		cursor.execute("SELECT username FROM credentials")
		uname=cursor.fetchall()
		s=str(uname)
		if s.find(user)!=-1:#name exists
			name=log.register()
		else:
			#successful username
			pasw=getpass.getpass("Enter Password: ")
			name=input("Enter you name: ")
			cursor.execute("INSERT INTO credentials (username,password,name) values (\""+user+"\",\""+pasw+"\",\""+name+"\")")
			db.commit()
			return name,user
	def login(self):
		global name
		global uname
		global password
		global db
		global cursor
		log=Login()
		user=input("Username: ")
		pasw=getpass.getpass("Password: ")
		count=0
		flag=0
		for i in uname:
			i= " ".join(re.findall("[a-zA-Z0-9]+", str(i)))		
			if user==i:
				j= " ".join(re.findall("[a-zA-Z0-9]+", str(password[count])))
				if j==pasw:
					print("Login Successful")
					flag=1
					cursor.execute("SELECT name FROM credentials WHERE username=\""+user+"\"")
					name=str(cursor.fetchone())
					#print(name[2:-3])
					db.close()
					return name[:-1],user
			count=count+1
		if flag==0:
			print("Please try again\n\n")
			log.login()
			return name[:-1],user

	def logger(self):
		global name
		global uname
		global password
		global db
		global cursor

		db=MySQLdb.connect("localhost","root","","Login_DB")

		cursor=db.cursor()
		cursor.execute("SELECT username FROM credentials")
		uname=cursor.fetchall()
		cursor.execute("SELECT password FROM credentials")
		password=cursor.fetchall()
		log=Login()
		print("Enter Register to register an account\n Else press the enter key")#GUI will make this more sensible
		query=input()
		print(query)
		if query.find('egister') !=-1:
			print("inside")
			name,username=log.register()
			return name,username

		
		name,username=log.login()
		return name,username
		#print(uname,password)
	

	
