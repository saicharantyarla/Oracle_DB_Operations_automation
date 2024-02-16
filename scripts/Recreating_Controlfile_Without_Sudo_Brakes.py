"""
	Name: Recreating_Controlfile_Without_Sudo_Brakes.py
	Description: Recreating the control file 
	Team: Software Service Automation
	Author: Saicharan Tyarla(sai-charan.thyarla@capgemini.com)
	Inputs: Arguments [HostName,Username,Password], LogFileLoc,ctl_file_path is Exceptional
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
	Execution_Location=Execution_Location.upper()
	HostName = sys.argv[2] 
	OSUser = sys.argv[3] 
	OSPassword = sys.argv[4]
	Sid=sys.argv[5]
	ctl_file_path=sys.argv[6]	# This path is Exceptional if it is not defined the it will use TRACE
	Status=""
	Ora_Home_Sid=""

		################################### Creating Log File ###############################
	try:
		if os.name == 'nt':
			logdir = os.getcwd()+"\\logs"
		if os.name == 'posix':
			logdir = os.getcwd()+"/logs"
		
		logfile = "Recreating_ctlFile_%s.log"%(HostName)
		log = Logger(logdir,logfile)

		log.info('*************************************************************************')
		print "Log file created"
		log.info('Started Script Execution')
		
	except Exception, e:
		print "ExitCode: 10"
		print "ExitDesc: Unable to create Logfile {0} {1}".format(logfile,e)

	################################### END OF LOG FILE CREARION ######################################
		
	try:
		if Execution_Location=="REMOTE":
			
			dssh = paramiko.SSHClient()
			dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			dssh.connect(HostName, username=OSUser, password=OSPassword)

			#loginline=". ~/.bash_profile\nsqlplus -s / as sysdba"
			#loginline="sqlplus -s / as sysdba"
			loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid
			
			######################################## Script Execution started ##################
			if "/" in ctl_file_path:
				command="ALTER DATABASE BACKUP CONTROLFILE TO '%s'; "%(ctl_file_path)
			else:
				command="alter database backup controlfile to trace;"
			ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command)
			log.info('Command for script Execution:%s'%ucommand)
			#print ucommand
			stdin, stdout, stderr = dssh.exec_command(ucommand)
			output = stdout.read()
			log.info("The output is %s"%output)
			error=stderr.read()
			#print output
			if error:
				log.info("ExitCode:10")
				log.info("ExitDesc:The error is %s"%error)
				print "ExitCode:10"
				print "ExitDesc:Error Occured Check logs"
				Status="Error Occured Check logs"
			else:
				if "ERROR" not in output and "ORA-" not in output:
					Status=" Recreate control File Successfull"	
					log.info("ExitCode:0")
					log.info("ExitDesc: Recreating controlfile successfull")
					print "ExitCode	:0"
					print "ExitDesc:Recreating controlfile successfull"
				else:
					Status=" Recreate control File Successfull"				
					log.info("ExitCode:10")
					log.info("ExitDesc: Recreating controlfile Failed")
					print "ExitCode	:10"
					print "ExitDesc:Recreating controlfile Failed"

					
				
		elif Execution_Location == "LOCAL":
			
			#loginline=". ~/.bash_profile\nsqlplus -s / as sysdba"	
			#loginline="sqlplus -s / as sysdba"
			loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid
			
		########################################### Actual Commands of the Script ##########################################				
			if "/" in ctl_file_path:
				command="ALTER DATABASE BACKUP CONTROLFILE TO '%s'; "%(ctl_file_path)
			else:
				command="alter database backup controlfile to trace;"
			ucommand ="%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command)
			log.info('Command for script Execution:%s'%ucommand)
			#print ucommand
			stdin, stdout, stderr = dssh.exec_command(ucommand)
			output = stdout.read()
			log.info("The output is %s"%output)
			#print output
			if "ERROR" not in output and "ORA-" not in output:
				Status=" Recreate control File Successfull"
				log.info("ExitCode:0")
				log.info("ExitDesc: Recreating controlfile successfull")
				print "ExitCode	:0"
				print "ExitDesc:Recreating controlfile successfull"
			else:
				Status="Failed to Reacreate control File"
				log.info("ExitCode:10")
				log.info("ExitDesc: Recreating controlfile Failed")
				print "ExitCode	:10"
				print "ExitDesc:Recreating controlfile Failed"

		else:
			Status="Failed"
			log.info("ExitCode:10")
			log.info("ExitDesc:Enter proper Execution_Location")
			print "ExitCode:10"
			print "ExitDesc:Enter proper Execution_Location"

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

SUBJECT = ' Recreating control files  '
body ="""
<html>
<H2> Recreating control files %s </H2>
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
	
		
					
