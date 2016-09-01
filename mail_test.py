'''
This program demonstrates how you can send a mail from a Python program and the commented part at the end shows how yo can use
a loop structure to send the same message multiple times to the same user.
Steps :
1. We first login to my gmail account using the in-App password that could be generated in Gmail.
2. We use the gmail server to send the message using SMTP protocol, through its corresponding port no. This details vary across 
the different mail services.
3. After logging in, we send the single or multiple times and then log out.
NOTE : These codes are strictly for educational purposes. Use them sensibly.
'''

import smtplib
import time

smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.ehlo()
smtpObj.starttls()

password = 'app-password'
message = '''From: Soumyadeep Roy <soumyadeep.roy9@gmail.com>
To: Soumya Roy <soumya.ace9@rediffmail.com>
Subject: Freshers Orientation Python Mail test SNB-222

Sir,
Link for R-course:
https://www.datacamp.com/courses/free-introduction-to-r

Best regards,
Soumyadeep Roy
Kalyani Government Engineering College
'''
smtpObj.login('soumyadeep.roy9@gmail.com', password)
smtpObj.sendmail('soumyadeep.roy9@gmail.com', 'soumya.ace9@rediffmail.com', message)
print 'Mails Sent successfully(Buggy code)'

'''
#Used only for sending the same message multiple times
for spamming in range(1,20):
	print("Spam mail no.{0} sent").format(spamming)
	smtpObj.sendmail('soumyadeep.roy9@gmail.com', 'soumya.ace9@rediffmail.com', message)
	time.sleep(1.0)
'''
smtpObj.quit()

