"""
	Name: Drop_Tablespace_Without_Sudo_Brakes.py
	Description: To drop an existing tablespace, remote or local server
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




################################### Creating Log File ###############################
try:
	if os.name == 'nt':
		logdir = os.getcwd()+"\\logs"
	if os.name == 'posix':
		logdir = os.getcwd()+"/logs"
	
	logfile = "Drop_Tablespace.log"
	log = Logger(logdir,logfile)

	log.info('*************************************************************************')

	log.info('Started Script Execution')
	
except Exception, e:
    print "ExitCode: 10"
    print "ExitDesc: Unable to create Logfile {0}".format(logfile)



try:
    
	if len(sys.argv) == 7:
		Execution_Location=sys.argv[1]
		HostName = sys.argv[2] 
		OSUser = sys.argv[3] 
		OSPassword = sys.argv[4]
		Sid=sys.argv[5]
		TBSName =sys.argv[6]					#Tablespace name to be dropped
		TBSName=TBSName.upper()
		Execution_Location=Execution_Location.upper()
		

		
########################################################### FOR REMOTE EXECUTION #######################################################################


		if Execution_Location=="REMOTE":
			
			dssh = paramiko.SSHClient()
			dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			dssh.connect(HostName, username=OSUser, password=OSPassword)

			#loginline=". ~/.bash_profile\nsqlplus -s / as sysdba"
			#loginline="sqlplus -s / as sysdba"
			loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid

		############################################## Verifying whether tablespace exists or not ###########################################
		
			command1 = "SELECT tablespace_name from dba_tablespaces where tablespace_name='%s';" %(TBSName)
			ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command1)
			log.info('Executing Query: {0}'.format(command1))
			stdin, stdout, stderr = dssh.exec_command(ucommand)
			output1=stdout.read()
			log.info('The command is: %s'%ucommand)
			log.info('The output is: %s'%output1)
			er= stderr.read()
			if er is not None:
				log.info('The error if any is: %s' %er)
			
			if output1 is not None:
				out1 = str(output1).translate(None, "[( ',	)]")
				out1=out1.strip() 
			if out1 == TBSName:				
			
			################################################ Query to Drop the Tablespace ######################################################
			
				command2="drop tablespace %s including contents and datafiles;"%(TBSName)
				ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command2)
				log.info('Executing Query: {0}'.format(command2))
				stdin, stdout, stderr = dssh.exec_command(ucommand)
				output2=stdout.read()
				log.info('The command is: %s'%ucommand)
				log.info('The output is: %s'%output2)
				er= stderr.read()
				if er is not None:
					log.info('The error if any is: %s' %er)
				
				
			################################################ Verifying whether dropping is successful or not ##########################################

				query= "select TABLESPACE_NAME from dba_tablespaces where TABLESPACE_NAME='%s';" %(TBSName)
				ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,query)
				log.info('Executing Query: {0}'.format(query))
				stdin, stdout, stderr = dssh.exec_command(ucommand)
				output3=stdout.read()
				log.info('The command is: %s'%ucommand)
				log.info('The output is: %s'%output3)
				er= stderr.read()
				if er is not None:
					log.info('The error if any is: %s' %er)
				
				if output3 is not None:
					out = str(output3).translate(None, "[( ',	)]")
					out=out.strip()

				if out != TBSName:
					print "ExitCode: 0"
					print "ExitDesc: Tablespace Drop successful. "
					log.info('ExitDesc : Tablespace Drop successful')
					log.info('Exitcode: 0')
					Status="Tablespace Dropping Successful"
				else:
					print "ExitCode: 10"
					print "ExitDesc: Tablespace Drop failed"
					log.info('ExitDesc: Tablespace Drop Failed')
					log.info('ExitCode: 10')
					Status="Tablespace Dropping Failed"
	
			else:
				print "ExitCode: 10"
				print "ExitDesc: Tablespace drop failed, since does not exist"
				log.info('ExitCode: 10')
				log.info('ExitDesc: Tablespace drop failed, since does not exist')
				Status="Tablespace dropping Failed. Tablespace does not exist."
			
				
########################################################### FOR LOCAL EXECUTION #######################################################################
            
		elif Execution_Location=="LOCAL":
			
			#loginline=". ~/.bash_profile\nsqlplus -s / as sysdba"
			#loginline="sqlplus -s / as sysdba"
			loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid	
		
		############################################## Verifying whether tablespace exists or not ###########################################
		
			command1 = "SELECT tablespace_name from dba_tablespaces where tablespace_name='%s';" %(TBSName)
			ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command1)
			log.info('Executing Query: {0}'.format(command1))
			output1=os.popen(ucommand).read()
			log.info('The command is: %s'%ucommand)
			log.info('The output is: %s'%output1)
			
			if output1 is not None:
				out1 = str(output1).translate(None, "[( ',	)]")
				out1=out1.strip() 
			if out1 == TBSName:
			
				
			################################################ Query to Drop the Tablespace ######################################################

			
				command2="drop tablespace %s including contents and datafiles;"%(TBSName)
				ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command2)
				#print ucommand
				log.info('Executing Query: {0}'.format(command2))
				output2=os.popen(ucommand).read()
				log.info('The command is: %s'%ucommand)
				log.info('The output is: %s'%output2)

			################################################ Verifying whether Dropping is successful or not #########################################

				query= "select TABLESPACE_NAME from dba_tablespaces where TABLESPACE_NAME='%s';" %(TBSName)
					
				ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,query)
				#print ucommand
				log.info('Executing Query: {0}'.format(query))
				output=os.popen(ucommand).read()
				log.info('The command is: %s'%ucommand)
				log.info('The output is: %s'%output)

				output = os.popen(ucommand).read()
				output=output.strip() 
				
				if output != TBSName:
					print "ExitCode: 0"
					print "ExitDesc: Tablespace Drop successful. "
					log.info('ExitDesc : Tablespace Drop successful')
					log.info('Exitcode: 0')
					Status="Tablespace Dropping Successful"

				else:
					print "ExitCode: 10"
					print "ExitDesc: Tablespace Drop  failed"
					log.info('ExitDesc: Tablespace Drop Failed')
					log.info('Exitcode: 10')
					Status="Tablespace Dropping Failed"
				
			else:
				print "ExitCode: 10"
				print "ExitDesc: Tablespace drop failed, since does not exist"
				log.info('ExitCode: 10')
				log.info('ExitDesc: Tablespace drop failed, since does not exist')
				Status="Tablespace dropping Failed. Tablespace does not exist."
					
				
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
		Status="Error occurerd. Check logs"
		
except Exception, e:
	print "ExitCode: 1"
	print "ExitDesc: script failed due to: {0}".format(e)
	log.info("ExitCode: 1")
	log.info("ExitDesc: script failed due to: {0}".format(e))
	Status="Error occurerd. Check logs"
	
################################ Mail part ##################################

now = datetime.now()
dt = now.strftime("%A,%d-%B-%y")
dt=str(dt)
FROM  = '%s'%frommail
TO = '%s'%tomail

SUBJECT = 'DROP TABLESPACE PROCESS '
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
<TH>  Tablespace Name  </TH>
<TH>  Status  </TH>
</TR>
<TR>
<TD>  %s  </TD>
<TD>  %s  </TD>
<TD>  %s  </TD>
<TD>  %s  </TD>
<TD>  %s  </TD>
</TR> 
</TABLE>
</BODY>
</HTML>""" %(dt,Execution_Location,HostName,Sid,TBSName,Status)
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



