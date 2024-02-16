"""
	Name: Pfile_test_Without_Sudo_Brakes.py
	Description: To create p-file, remote target server or local target server
	Team: Software Service Automation
	Author: Arnab Roy(arnab.d.roy@capgemini.com)
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



################################### Creating Log File ###############################
try:
	if os.name == 'nt':
		logdir = os.getcwd()+"\\logs"
	if os.name == 'posix':
		logdir = os.getcwd()+"/logs"
	
	logfile = "Create_Pfile.log"
	log = Logger(logdir,logfile)

	log.info('*************************************************************************')

	log.info('Started Script Execution')
	
except Exception, e:
	print "ExitCode: 10"
	print "ExitDesc: Unable to create Logfile  {0} due to {1}".format(logfile,e)
	Status="Error Occurred"


try:
    
	if len(sys.argv) == 6:
		Execution_Location=sys.argv[1]
		HostName = sys.argv[2] 
		OSUser = sys.argv[3] 
		OSPassword = sys.argv[4]
		Sid=sys.argv[5]
		Execution_Location=Execution_Location.upper()

		if Execution_Location=="REMOTE":
			
			dssh = paramiko.SSHClient()
			dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			dssh.connect(HostName, username=OSUser, password=OSPassword)
			loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid
			#loginline=". ~/.bash_profile\nsqlplus -s / as sysdba"
			#loginline="sqlplus -s / as sysdba"	
			
			
	############################################## Query to create p-file ##############################################

		
			command2="CREATE PFILE FROM SPFILE;"
			ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command2)
			log.info('Executing Query: {0}'.format(command2))
			stdin, stdout, stderr = dssh.exec_command(ucommand)
			output2=stdout.read()
			log.info('The command is: %s'%ucommand)
			log.info('The output is: %s'%output2)
			er= stderr.read()
			if er is not None:
				log.info('The error if any is: %s' %er)
			

			if "ERROR" not in output2:
				log.info('ExitCode: 0')
				log.info("ExitDesc: P-File created Successfully")
				print "ExitCode: 0"
				print "ExitDesc: P-File created Successfully"
				Status = "P-File Created"	
			else:
				log.info('Exitcode: 1')
				log.info("ExitDesc: P-File Creation Failed")
				log.info('Error: {0} '.format(output2))
				print "ExitCode: 1"
				print "ExitDesc: SP-File Creation Failed. Error."
				Status = "P-File creation failed. Error. Check Logs"

						
		
		
		#################################################### For Local Execution ###########################################################
		
		
		elif Execution_Location=="LOCAL":
			loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid			
			#loginline=". ~/.bash_profile\nsqlplus -s / as sysdba"	
			#loginline="sqlplus -s / as sysdba"

				
			############################################## Query to create sp-file ##############################################

				
			command2="CREATE PFILE FROM SPFILE;"
			ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command2)
			log.info('Executing Query: {0}'.format(command2))
			output2=os.popen(ucommand).read()
			log.info('The command is: %s'%ucommand)
			log.info('The output is: %s'%output2)
			

			if "ERROR" not in output2:
				log.info('ExitCode: 0')
				log.info("ExitDesc: P-File created Successfully")
				print "ExitCode: 0"
				print "ExitDesc: P-File created Successfully"
				Status = "P-File Created"
			else:
				log.info('Exitcode: 1')
				log.info("ExitDesc: P-File Creation Failed")
				print "ExitCode: 1"
				print "ExitDesc: P-File Creation Failed. Error."
				Status = "P-File creation failed. Error. Check Logs"
				
		else:
			print "ExitCode:10"
			print "ExitDesc:Enter proper Execution_Location input"
			log.info("ExitCode:10")
			log.info("ExitDesc:Enter proper Execution_Location input")
			Status="Error Occurred."

	else:
		print "ExitCode: 10"
		print "ExitDesc: Missing Arguments"
		log.info('ExitCode: 10')
		log.info('ExitDesc: Missing Arguments')
		
except Exception, e:
	print "ExitCode: 10"
	print "ExitDesc: script failed due to: {0}".format(e)
	log.info('ExitCode: 10')
	log.info('ExitDesc: Script failed due to: {0}'.format(e))
	Status="Error Occurred. Check Logs"
	
	
################################ Mail part ##################################

now = datetime.now()
dt = now.strftime("%A,%d-%B-%y")
dt=str(dt)
FROM  = '%s'%frommail
TO = '%s'%tomail

SUBJECT = 'CREATE PFILE PROCESS '
body ="""
<html>
<H2> Database Status for %s </H2>
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

<TABLE>
<TR>
<TH>  Execution Type  </TH>
<TH>  Server Name  </TH>
<TH>  SID or Database name  </TH>
<TH>  Status  </TH>
</TR>
<TR>
<TD>  %s  </TD>
<TD>  %s  </TD>
<TD>  %s  </TD>
<TD>  %s  </TD>
</TR> 
</TABLE>
</BODY>
</HTML>""" %(dt,Execution_Location,HostName,Sid,Status)
	# Prepare actual message
	
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
