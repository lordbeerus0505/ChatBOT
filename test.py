
import smtplib
import gmail
import imaplib
import email 

userid="abhiram.natarajan@gmail.com"
passwd="abhiawesome"
class Mail:
	def send_mail(self,From,to,subject,Message):
		# FROM = "abhiram.natarajan@gmail.com"
		# TO = "abhiram.natarajan@gmail.com"
		# SUBJECT = "TEST"
		# TEXT = "testing API calls"
		FROM=From
		TO=to
		SUBJECT=subject
		TEXT=Message
		# Prepare actual message
		message = """Subject: %s\n\n%s
		""" % ( SUBJECT, TEXT)
		try:
			server = smtplib.SMTP("smtp.gmail.com", 587)
			server.ehlo()
			server.starttls()
			server.login(userid, passwd)
			server.sendmail(FROM, TO, message)
			server.close()
			print('successfully sent the mail')
		except:
			print ("failed to send mail")

	def show_mails(self):
		
		SMTP_SERVER = "imap.gmail.com"
		SMTP_PORT   = 993
		mail = imaplib.IMAP4_SSL(SMTP_SERVER)
		mail.login(userid,passwd)
		
		# play with your gmail...
		x=mail.select('inbox')
		
		type, data = mail.search(None, 'ALL')
		mail_ids = data[0]
		

		id_list = mail_ids.split()   
		
		first_email_id = int(id_list[0])
		latest_email_id = int(id_list[-1])


		print(latest_email_id)
		#last 5 emails shown, can be customised
		for i in range(latest_email_id,latest_email_id-5, -1):
			typ, data = mail.fetch(str(i), '(RFC822)' )
		

			for response_part in data:
				if isinstance(response_part, tuple):
					msg = email.message_from_string(response_part[1].decode())
					# print(msg)
					email_subject = msg['subject']
					email_from = msg['from']
					print('From : ' +str(email_from) + '\n')
					print ('Subject : ' + email_subject + '\n')
					ch=input("press b to view body, any other key to continue")
					if ch=='b':
						if msg.is_multipart():
							#display body only is b pressed
							for payload in msg.get_payload():
								
								print(payload.get_payload())
						else:
							print(msg.get_payload())

		

# obj=Mail()
# # obj.send_mail("abhiram.natarajan@gmail.com","abhiram.natarajan@gmail.com","Yolo!@#","Testing lolol")
# obj.show_mails()