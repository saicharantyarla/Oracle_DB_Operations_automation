"""
	Name: Create_User_Without_Sudo_Brakes.py
	Description: To Create a user for a tablespace, remote or local execution
	Team: Software Service Automation
	Author: Arnab Roy (arnab.d.roy@capgemini.com)
	Inputs: Arguments [HostName,Username,Password], LogFileLoc
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



################################### Creating Log File ###########################
try:
	if os.name == 'nt':
		logdir = os.getcwd()+"\\logs"
	if os.name == 'posix':
		logdir = os.getcwd()+"/logs"

	logfile = "Create_User.log"
	log = Logger(logdir,logfile)

	log.info('*************************************************************************')

	log.info('Started Script Execution')
	
except Exception, e:
    print "ExitCode: 10"
    print "ExitDesc: Unable to create Logfile {0}".format(logfile)




try:
    
	if len(sys.argv) == 9:
		Execution_Location=sys.argv[1]
		HostName = sys.argv[2] 
		OSUser = sys.argv[3] 
		OSPassword = sys.argv[4]
		Sid=sys.argv[5]
		Username=sys.argv[6]
		Password=sys.argv[7]
		TablespaceName=sys.argv[8]
		Execution_Location=Execution_Location.upper()
		Username=Username.upper()
		

	############################ For Remote execution ##########################	
		
		if Execution_Location=="REMOTE":
			
			dssh = paramiko.SSHClient()
			dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			dssh.connect(HostName, username=OSUser, password=OSPassword)

			#loginline=". ~/.bash_profile\nsqlplus -s / as sysdba"
			#loginline="sqlplus -s / as sysdba"
			loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid
			
			############################################## Verifying whether User exists or not ###########################################
			
			command = "SELECT username from dba_users where username='%s';" %(Username)
			ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command)
			log.info('Executing Query: {0}'.format(command))
			stdin, stdout, stderr = dssh.exec_command(ucommand)
			output=stdout.read()
			log.info('The command is: %s'%ucommand)
			log.info('The output is: %s'%output)
			er= stderr.read()
			if er is not None:
				log.info('The error if any is: %s' %er)
			
			if output is not None:
				out = str(output).translate(None, "[( ',	)]")
				out=out.strip() 
			if out != Username:
			
			
		###################################### Creating User ####################################

				
				command1="create user %s identified by %s default tablespace %s;" %(Username,Password,TablespaceName)
				ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command1)
				log.info('Executing Query: {0}'.format(command1))
				stdin, stdout, stderr = dssh.exec_command(ucommand)
				output1=stdout.read()
				log.info('The command is: %s'%ucommand)
				log.info('The output is: %s'%output1)
				er= stderr.read()
				if er is not None:
					log.info('The error if any is: %s' %er)
				
				if "ERROR" in output1:
					log.info('Exitcode: 1')
					log.info("ExitDesc: User Creation Failed")
					log.info('Error: {0} '.format(output1))
					print "ExitCode: 1"
					print "ExitDesc: User Creation Failed. Error."
					Status = "User creation failed. Error. Check Logs"
					
					
			############################ Grant connect privileg to User ###########################	
				
				command2="grant connect,create session to %s;" %Username
				ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command2)
				log.info('Executing Query: {0}'.format(command2))
				stdin, stdout, stderr = dssh.exec_command(ucommand)
				output2=stdout.read()
				log.info('The command is: %s'%ucommand)
				log.info('The output is: %s'%output2)
				er= stderr.read()
				if er is not None:
					log.info('The error if any is: %s' %er)
				
				if "ERROR" in output2:
					log.info('ExitCode: 1')
					log.info("ExitDesc: Granting permissions to %s failed" %Username)
					print "ExitCode: 1"
					print "ExitDesc: Granting permissions to %s failed" %Username
					Status="Granting permissions failed. Error. Check Logs"
				else:
					log.info('Exitcode: 0')
					log.info("ExitDesc:User %s created successfully"%Username)
					print "ExitCode: 0"
					print "ExitDesc:User %s created successfully"%Username
					Status="User Created Successfully"
					
			else:
				print "ExitCode: 10"
				print "ExitDesc: User Creation failed, since exists already"
				log.info('ExitCode: 10')
				log.info('ExitDesc: User Creation failed, since exists already')
				Status="User Creation Failed. User exists already"
					
			
	
	###################################### For Local execution #######################################
	

		elif Execution_Location=="LOCAL":
			
			#loginline=". ~/.bash_profile\nsqlplus -s / as sysdba"	
			#loginline="sqlplus -s / as sysdba"
 	
			loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid
			command1="create user %s identified by %s default tablespace %s;" %(Username,Password,TablespaceName)
			ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command1)
			log.info('Executing Query: {0}'.format(command1))
			output=os.popen(ucommand).read()
			log.info('The command is: %s'%ucommand)
			log.info('The output is: %s'%output1)
			er= stderr.read()
			if er is not None:
				log.info('The error if any is: %s' %er)
			
			if "ERROR" in output1:
				log.info('Exitcode: 1')
				log.info("ExitDesc: User Creation Failed")
				log.info('Error: {0} '.format(output2))
				print "ExitCode: 1"
				print "ExitDesc: User Creation Failed. Error."
				Status = "User creation failed. Error. Check Logs"
				
				
		############################ Grant connect privileg to User ###########################	
			
			command2="grant connect,create session to %s;" %Username
			ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command2)
			log.info('Executing Query: {0}'.format(command2))
			output2=os.popen(ucommand).read()
			log.info('The command is: %s'%ucommand)
			log.info('The output is: %s'%output2)
			er= stderr.read()
			if er is not None:
				log.info('The error if any is: %s' %er)
			
			if "ERROR" in output2:
				log.info('ExitCode: 1')
				log.info("ExitDesc: Granting permissions to %s failed" %Username)
				print "ExitCode: 1"
				print "ExitDesc: Granting permissions to %s failed" %Username
				Status="Granting permissions failed. Error. Check Logs"
			else:
				log.info('Exitcode: 0')
				log.info("ExitDesc:User %s created successfully"%Username)
				print "ExitCode: 0"
				print "ExitDesc:User %s created successfully"%Username
				Status="User Created Successfully"
				
				
				
		else:
			log.info("ExitCode: 10")
			log.info("Enter valid Execution Location")
			print "Enter valid Execution Location"
			Status="Error Occurred. Check Logs"
	else:
		print "ExitCode: 10"
		print "ExitDesc: Missing Arguments"
		log.info("ExitCode:10")
		log.info("ExitDesc: Missing Arguments")
		Status="Error Occurred. Check Logs"
except Exception, e:
	print "ExitCode: 1"
	print "ExitDesc: script failed due to: {0}".format(e)
	log.info("ExitCode:1")
	log.info("ExitDesc: script failed due to: {0}".format(e))
	Status="Error Occurred. Check Logs"



################################ Mail part ##################################

now = datetime.now()
dt = now.strftime("%A,%d-%B-%y")
dt=str(dt)
FROM  = '%s'%frommail
TO = '%s'%tomail

SUBJECT = 'CREATE USER PROCESS '
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
<TH> Tablespace Name  </TH>
<TH>  User Name  </TH>
<TH>  Status  </TH>

</TR>
<TR>
<TD>  %s  </TD>
<TD>  %s  </TD>
<TD>  %s  </TD>
<TD>  %s  </TD>
<TD>  %s  </TD>
<TD>  %s  </TD>

</TR> 
</TABLE>
</BODY>
</HTML>"""%(dt,Execution_Location,HostName,Sid,TablespaceName,Username,Status)
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
