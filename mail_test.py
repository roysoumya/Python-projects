import smtplib
import time

smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.ehlo()
smtpObj.starttls()

password = 'ovzkcwskaaelhxyc'
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
smtpObj.login('soumyadeep.roy9@gmail.com', 'ovzkcwskaaelhxyc')
smtpObj.sendmail('soumyadeep.roy9@gmail.com', 'soumya.ace9@rediffmail.com', message)
print 'Mails Sent successfully(Buggy code)'

for spamming in range(1,20):
	print("Spam mail no.{0} sent").format(spamming)
	smtpObj.sendmail('soumyadeep.roy9@gmail.com', 'soumya.ace9@rediffmail.com', message)
	time.sleep(1.0)

smtpObj.quit()

