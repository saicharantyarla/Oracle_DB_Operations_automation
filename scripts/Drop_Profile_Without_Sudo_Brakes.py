"""
	Name: Drop_Profile_Without_Sudo_Brakes.py
	Description: Registering Database in Recovery Catalog Without Sudo, remote target server or local target server
	Team: Software Service Automation
	Author: Saicharan Tyarla(sai-charan.thyarla@capgemini.com)
	Inputs: Arguments [HostName,Username,Password,SID], LogFileLoc
	Output: ExitCode, ExitDesc(Log File)
"""

#!/usr/bin/env python
from sys import path
import sys
from Logger import Logger
import Logger as log
import time
import datetime
from os import system, getcwd, path, makedirs
import paramiko
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from smptconfig import smtpserver, frommail, tomail


if len(sys.argv) == 7:
	Execution_Location=sys.argv[1]
	HostName = sys.argv[2] 
	OSUser = sys.argv[3] 
	OSPassword = sys.argv[4]
	Sid=sys.argv[5]
	profile_name=sys.argv[6]
	profile_name=profile_name.upper()
	Status=""
	Execution_Location=Execution_Location.upper()		
	################################### Creating Log File ###############################
	try:
		if os.name == 'nt':
			logdir = os.getcwd()+"\\logs"
		if os.name == 'posix':
			logdir = os.getcwd()+"/logs"
		
		logfile = "Drop_Profile_%s.log"%(HostName)
		log = Logger(logdir,logfile)

		log.info('*************************************************************************')
		#print "Log file created"
		log.info('Started Script Execution')
		
	except Exception, e:
		print "ExitCode: 10"
		print "ExitDesc: Unable to create Logfile {0} {1}".format(logfile,e)
		
	try:
		log.info("Given input is %s"%Execution_Location)
		if Execution_Location=="REMOTE":
		
			log.info('Started Script Execution in remote location')
			#loginline=". ~/.bash_profile\nsqlplus -S / as sysdba"
			#loginline="sqlplus -s / as sysdba"
			loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid
			commandd="select PROFILE from DBA_PROFILES where PROFILE='%s';"%(profile_name)

			ucommandd = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,commandd)
			dssh = paramiko.SSHClient()
			dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			dssh.connect(HostName, username=OSUser, password=OSPassword)
			log.info('Server Connection Successfull')
			#print ucommand
			log.info("Checking Profile Existance")
			log.info("The command is %s"%(ucommandd))
			stdin, stdout, stderr = dssh.exec_command(ucommandd)
			outputt = stdout.read()

			log.info("The output is %s "%(outputt))
			if profile_name in outputt:
				log.info("The Given Profile exists %s"%profile_name)
				log.info("Dropping User")
				command1="drop profile %s;"%profile_name
				ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command1)
				stdin, stdout, stderr = dssh.exec_command(ucommand)
				output = stdout.read()
				log.info('The command is %s'%(ucommand))
				log.info('the output is %s'%(output))
				error=stderr.read()
				if error:
					log.info("ExitCode:10")
					log.info("ExitDesc:Error is .. %s"%error)
					print "ExitCode:10"
					print "ExitDesc:Error is %s"%error
					Status="Error occured check the log file"
				else:
				
					if "ORA-" not in output and "ERROR" not in output:
						log.info('ExitCode: 0')
						log.info("ExitDesc: Profile Dropped Successfully")
						print "ExitCode: 0"
						print "ExitDesc: Profile Dropped Successfully"
						Status = "Profile Dropped Successfully"
					else:
						log.info("ExitCode:1")
						log.info("ExitDesc: Dropping Profile  Failed")
						print "ExitCode:1"
						print "ExitDesc:Dropping Profile Failed"
						Status="Dropping Profile Failed"						
			else:
				log.info("ExitCode:10")
				log.info("ExitDesc:Given Profile doesnot Exists Check log file")
				print "ExitCode:10"
				print "ExitDesc:Given Profile doesnot Exists Check log file"
				Status="Given Profile doesnot Exists Check log file"
		elif Execution_Location=="LOCAL":
			#loginline="sqlplus -s / as sysdba"
			#loginline=". ~/.bash_profile\nsqlplus -S / as sysdbA"
			loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid
			commandd="select PROFILE from DBA_PROFILES where PROFILE='%s';"%(profile_name)

			ucommandd = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,commandd)
			#print ucommand
			log.info("Checking Profile Existance")
			log.info("The command is %s"%(ucommandd))
			outputt = os.popen(ucommandd).read()
			log.info("The output is %s "%(outputt))
			if profile_name in outputt:
				log.info("The Given Profile exists %s"%profile_name)
				log.info("Dropping User")
				command1="drop profile %s;"%profile_name
				ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command1)
				#print ucommand
				log.info("The command is %s"%(ucommand))
				output = os.popen(ucommand).read()
				log.info("The output is %s "%(output))
				if "ORA-" not in output and "ERROR" not in output:
					log.info('ExitCode: 0')
					log.info("ExitDesc: Profile Dropped Successfully")
					print "ExitCode: 0"
					print "ExitDesc: Profile Dropped Successfully"
					Status = "Profile Dropped Successfully"
				else:
					log.info("ExitCode:1")
					log.info("ExitDesc: Dropping Profile  Failed")
					print "ExitCode:1"
					print "ExitDesc:Dropping Profile Failed"
					Status="Dropping Profile Failed"						
			else:
				log.info("ExitCode:10")
				log.info("ExitDesc:Given Profile doesnot Exists Check log file")
				print "ExitCode:10"
				print "ExitDesc:Given Profile doesnot Exists Check log file"
				Status="Given Profile doesnot Exists Check log file"
		else:
			log.info("ExitCode:10")
			log.info("ExitDesc:Enter proper Execution_Location")
			print "ExitCode:10"
			print "ExitDesc:Enter proper Execution_Location"
			Status="ERROR Occured check log file"

	except Exception, e:
		log.info("10: ExitDesc: Error Occured:%s"%e)
		print "1"
		print "ExitDesc: script failed due to: {0}".format(e)
		Status="Error Occurred. Check Logs"						
else:
	print "10"
	print "ExitDesc: Missing Arguments"
	Status="Error Occurred. Check Logs"
	
################################ Mailing  part ############################################

now = datetime.now()
dt = now.strftime("%A,%d-%B-%y")
dt=str(dt)
FROM  = '%s'%frommail
TO = '%s'%tomail

SUBJECT = ' Dropping Profile  '
body ="""
<html>
<H2> Dropping Profile %s </H2>
<style>
  table, th, td {
	border: 2px solid cyan;
	}
th, td {
	padding: 10px;
}
th {
	background-color:#f1f1c1;
}
body {
	margin-left: 5px;
	margin-top: 5px;
	margin-right: 0px;
	margin-bottom: 10px;
	table {
	border: thin solid #000000;
}
</style>
<body>
<table>
<tr><th>HostName </th> <th>Execution Location </th> <th> SID </th><th> Status</th>  </tr>
<tr> <td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>
</table>
</body>	
</html>"""%(dt,HostName,Execution_Location,Sid,Status)


part1="""From: %s 
To: %s 
Subject: %s
Content-Type: multipart/mixed;
""" %(frommail, tomail, SUBJECT)

part2 = """Content-Type: text/html
%s
""" %body


message = part1 + part2


try:
	client = smtplib.SMTP(smtpserver)
	client.sendmail(FROM, TO, message)
	client.quit()
	print "Email sent"
	log.info('Email Sent')
	
except Exception, e:
	print "Email sending failed due to: {0}".format(e)
	log.info('Email sending failed due to: {0}'.format(e))				
				

			
