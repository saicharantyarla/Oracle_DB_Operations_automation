"""
	Name: Analysing_ORA_Errors_Without_Sudo_Brakes.py
	Description: To check for presence of ORACLE Errors, remote or local execution
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

	logfile = "Analysing_ORA_Errors.log"
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

		
		input_var = raw_input("Enter Date (e.g. Wed Jun 13): ")
		print ("you entered {0}".format(input_var))
		print input_var

			
		dssh = paramiko.SSHClient()
		dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		dssh.connect(HostName, username=OSUser, password=OSPassword)

		#loginline=". ~/.bash_profile\nsqlplus -s / as sysdba"
		#loginline="sqlplus -s / as sysdba"
		loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid		
		
		command1="SELECT VALUE FROM V\$DIAG_INFO WHERE NAME = 'Diag Trace';"
		ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF\nexit" %(loginline,command1)
		log.info('Executing Query: {0}'.format(command1))
		stdin, stdout, stderr = dssh.exec_command(ucommand)
		output1=stdout.read()
		
		log.info('The command is: %s'%ucommand)
		log.info('The output is: %s'%output1)
		er= stderr.read()
		
		output1=output1.strip('\n')
		print "Out: %s"%output1
		print "Error: %s"%er 
		
		if er is not None:
			log.info('The error if any is: %s' %er)
		
		
		command2="cd %s\ncat alert_%s.log | awk 'BEGIN{ found=0} /%s/{found=1} {if (found) print }'" %(output1,Sid,input_var)
		
		log.info('Executing Query: {0}'.format(command2))
		stdin, stdout, stderr = dssh.exec_command(command2)
		output2=stdout.read()
		#print output2
		
		
		#logdt=now.strftime("%a %b %d")
				
		filename="/mnt/dumps/crisk/Oracle_Errors.txt"
		with open(file,"w") as f:
			f.write("%s"%output2)
		
		
		if "ERROR" not in output1:
			if output1:
				log.info('ExitCode: 0')
				log.info("ExitDesc: Oracle Errors found and script executed Successfully")
				print "ExitCode: 0"
				print "ExitDesc: Oracle Errors found and script executed Successfully"
				Status="Orace Errors Found"
			else:
				log.info('Exitcode: 0')
				log.info("ExitDesc:No Oracle Errors found Script executed successfully")
				print "ExitCode: 0"
				print "ExitDesc:No oracle Errors found Script executed successfully"
				Status="No Oracle Errors"
				
		else:
			log.info("ExitCode: 10")
			log.info("ExitDesc: Error Occured:%s"%output1)
			print "ExitCode: 1"
			print "ExitDesc: Error Occured:%s"%output1
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

SUBJECT = ' ORACLE ERRORS PROCESS '
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
</HTML>"""%(dt,Execution_Location,HostName,Sid,Status)
	# Prepare actual message
	
part1="""From: %s 
To: %s 
Subject: %s
Content-Type: multipart/mixed;
""" %(frommail, tomail, SUBJECT)

part2 = """Content-Type: text/html
%s
""" %body

part3= """Content-Type: multipart/mixed; name=\"%s"\
Content-Transfer-Encoding:base64
Content-Disposition: attachment; filename=%s
"""(filename,filename)


message = part1 + part2 + part3


try:
	client = smtplib.SMTP(smtpserver)
	client.sendmail(FROM, TO, message)
	client.quit()
	print "Email sent"
	log.info('Email Sent')
	
except Exception, e:
	print "Email sending failed due to: {0}".format(e)
	log.info('Email sending failed due to: {0}'.format(e))
