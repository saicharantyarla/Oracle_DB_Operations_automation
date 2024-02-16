"""
	Name: Stop_DB_Without_Sudo.py
	Description: To stop Database, remote target server or local target server
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
	
	logfile = "StopDB.log"
	log = Logger(logdir,logfile)

	log.info('*************************************************************************')

	log.info('Started Script Execution')
	
except Exception, e:
    print "ExitCode: 10"
    print "ExitDesc: Unable to create Logfile {0}".format(logfile)





try:
    
	if len(sys.argv) == 6:
		Execution_Location=sys.argv[1]
		HostName = sys.argv[2] 
		OSUser = sys.argv[3] 
		OSPassword = sys.argv[4]
		Sid=sys.argv[5]
		Execution_Location=Execution_Location.upper()
		
		if Execution_Location=="REMOTE":
			#loginline=". ~/.bash_profile\nsqlplus -S / as sysdbA"
			#loginline="sqlplus -s / as sysdba"	
			loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid
			dssh = paramiko.SSHClient()
			dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			dssh.connect(HostName, username=OSUser, password=OSPassword)			
			command1="SHUTDOWN IMMEDIATE"
			ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command1)
			stdin, stdout, stderr = dssh.exec_command(ucommand)
			output = stdout.read()
			log.info('The command is %s'%(ucommand))
			log.info('the output is %s'%(output))
			
			if "ERROR" not in output or "ORACLE not available" in output:
				if "closed" in output or "shut" in output:
					log.info('ExitCode: 0')
					log.info("ExitDesc: Database stopped Successfully")
					print "ExitCode: 0"
					print "ExitDesc: Database stopped Successfully"
					Status="Stopped successfully"
				elif "not available" in output:
					log.info('Exitcode: 0')
					log.info("ExitDesc: Database is already stopped")
					print "ExitCode: 0"
					print "ExitDesc: Database is already stopped"
					Status="Already stopped"
				else:
					log.info('Exitcode: 1')
					log.info("ExitDesc: Database failed to stop")
					print "ExitCode: 1"
					print "ExitDesc: Database failed to stop"
					Status="Failed to stop"
			else:
				print "ExitCode: 1"
				print "ExitDesc: Error Occured:%s"%output
				Status="Some error Occured. Check logs"
					
				
		#################################################### For Local Execution ####################################################		
				
		elif Execution_Location=="LOCAL":
			#loginline="sqlplus -s / as sysdba"
			#loginline=". ~/.bash_profile\nsqlplus -S / as sysdbA"			
			loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid
			command="SHUTDOWN IMMEDIATE"
			ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command)
			log.info("The Command is %s"%ucommand)
			output = os.popen(ucommand).read()
			if "ERROR" not in output:
				if "closed" in output:
					log.info('ExitCode: 0')
					log.info("ExitDesc: Database stopped Successfully")
					print "ExitCode: 0"
					print "ExitDesc: Database stopped Successfully"
					Status="Stopped successfully"
				elif "not available" in output:
					log.info('Exitcode: 0')
					log.info("ExitDesc: Database is already stopped")
					print "ExitCode: 0"
					print "ExitDesc: Database is already stopped"
					Status="Database is already stopped"
				else:
					log.info('Exitcode: 1')
					log.info("ExitDesc: Database failed to stop")
					print "ExitCode: 1"
					print "ExitDesc: Database failed to stop"
					Status="Failed to stop"
					
			else:
				print "ExitCode: 1"
				print "ExitDesc: Error Occured:%s"%output
				log.info('ExitCode: 1')
				log.info('ExitDesc: Error Occured: %s'%output)
				Status="Some error Occured. Check logs"					
		else:
			print "ExitCode:10"
			print "ExitDesc:Enter proper Execution_Location input"
			log.info("ExitCode:10")
			log.info("ExitDesc:Enter proper Execution_Location input")
			Status="Error Occurred."

	else:
		print "ExitCode: 10"
		print "ExitDesc: Missing Arguments"
		Status="Error Occurred. Check Logs"
		
except Exception, e:
	print "10"
	print "ExitDesc: script failed due to: {0}".format(e)
	Status="Error Occurred. Check Logs"
	
################################ Mail part ##################################

now = datetime.now()
dt = now.strftime("%A,%d-%B-%y")
dt=str(dt)
FROM  = '%s'%frommail
TO = '%s'%tomail


SUBJECT = 'STOP DATABASE PROCESS '
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

log.info("Sending Email to the %s"%(TO))

message = part1 + part2


try:
	client = smtplib.SMTP(smtpserver)
	client.sendmail(FROM, TO, message)
	client.quit()
	log.info("Email Sent Successfully")
	log.info("Email Sent Successfully")
	print "Email sent"
	
except Exception, e:
	print "Email sending failed due to: {0}".format(e)
