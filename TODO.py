'''
IMPLEMENTING A TODO LIST THAT HOLDS ITEM TITLE AND DESCRIPTION IN A DATABASE.
'''
import MySQLdb

class Todo:

	def create_item(self,username):
		#username is the primary key in table 1 use as foreign in table 2
		title=input("Enter the title: ")
		description=input("Enter the description: ")
		db=MySQLdb.connect("localhost","root","","Login_DB")
		cursor=db.cursor()
		cursor.execute("INSERT INTO TODO VALUES (\""+title+"\",\""+description+"\",\""+username+"\")")
		db.commit()
		print("Your TODO list has been updated")

	def delete_item(self,title,username):
		db=MySQLdb.connect("localhost","root","","Login_DB")
		cursor=db.cursor()
		cursor.execute("SELECT Title from TODO where username=\'"+username+"\'")
		results=str(cursor.fetchall())
		flag=0
		if title not in results:
			flag=1
		if flag==1:
			title=input("Please enter the title of the note: ")
			flag=0
		if flag==0:
			cursor.execute("DELETE FROM TODO WHERE Title=\'"+title+"\'") 
			db.commit()
			print("Congrats, you have completed the activity "+title)
			return True

	def view_items(self,username):
		db=MySQLdb.connect("localhost","root","","Login_DB")
		cursor=db.cursor()
		cursor.execute("SELECT * FROM TODO WHERE username=\'"+username+"\'")
		todo_list=cursor.fetchall()
		#print(todo_list) 
		for tod in todo_list:
			print("TITLE: "+tod[0])
			print("DESCRIPTION: "+tod[1],"\n")


#todo=Todo()
#todo.create_item("Abhidogg")
#todo.delete_item("Get milk")
#todo.view_items("Abhidogg")
