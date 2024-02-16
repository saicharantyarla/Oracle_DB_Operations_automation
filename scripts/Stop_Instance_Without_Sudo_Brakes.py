"""
	Name: Stop_Instance_Without_Sudo.py
	Description: To stop instance on remote or local system
	Team: Software Service Automation
	Author: Arnab Roy (arnab.d.roy@capgemini.com)
	Inputs: Arguments [Execution_Location,Hostname,OSUser,OSPassword,Listener,Sid], LogFileLoc
	Output: ExitCode, ExitDesc(Log File)
	
"""

#!/usr/bin/env python
from sys import path
import sys
from Logger import Logger 
import Logger as log
import time
import datetime
from os import system,getcwd,path,makedirs
import socket
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

	logfile = "Stop_Instance.log"
	log = Logger(logdir,logfile)

	log.info('*************************************************************************')

	log.info('Started Script Execution')
	
except Exception, e:
    print "ExitCode: 10"
    print "ExitDesc: Unable to create Logfile {0}".format(logfile)


try:
	log.info('Input Variables mapping...')
	if len(sys.argv) == 7:
		##Script Variables##
		Execution_Location=sys.argv[1]
		HostName = sys.argv[2]  		#Target HostName  	
		OSUser = sys.argv[3]			#Target Host user name to connect 
		OSPassword = sys.argv[4]		#Target Host user password to connect
		Instance = sys.argv[5]			#Instance name
		Sid=sys.argv[6]					#SID or Database name
		Execution_Location=Execution_Location.upper()
		
	
		if Execution_Location=="REMOTE":
	####################################################### Command to Stop Instance ####################################################
			command1="srvctl stop instance -d %s -i %s -o immediate" %(Sid,Instance)

			dssh = paramiko.SSHClient()
			dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			dssh.connect(HostName, username=OSUser, password=OSPassword)

			stdin, stdout, stderr = dssh.exec_command(command1)
			output2 = stdout.read()
			log.info('The command is %s'%(command1))
			log.info('the output is %s'%(output2))
			Error=stderr.read()
			log.info("The Error if any is %s  "%Error)	
			
			if "ERROR" or "unable" in output2:
				print "ExitCode: 1"
				print "ExitDesc: Error, failed to Stop Instance \n %s" %(output2)
				log.info('Exitcode: 1')
				log.info('Error: {0}'.format(output2))
				Status="Error Occurred. Check Logs"
			elif "has already been stopped" in output:
				print "ExitCode: 0"
				print "ExitDesc: Instance %s has already been stopped"%(Instance)
				log.info('ExitCode: 0')
				log.info('ExitDesc: Instance %s has already been stopped'%(Instance))
				Status="Instance already stopped"	
			else:
				print "ExitCode: 0"
				print "Exitdesc: Successfully stopped the instance"
				log.info('ExitCode:0')
				log.info('Info: Successfully stopped the instance')
				Status="Successfully stopped instance"
############################################### For Local Execution ###########################################
		elif Execution_Location=="LOCAL":
############################################################################ Command to Stop the Instance #############################################
			command1="srvctl stop instance -d %s -i %s -o immediate" %(Sid,Instance)
			output = os.popen(command1).read()
			
			log.info('The command is %s'%(command1))
			log.info('the output is %s'%(output))
		
			if "ERROR" or "unable" in output:
				print "ExitCode: 1"
				print "ExitDesc: Error, failed to Stop Instance \n %s" %(output)
				log.info('Exitcode: 1')
				Status="Error Occurred. Check Logs"
				log.info('Error: {0}'.format(output))
			elif "already stopped" in output:
				print "ExitCode: 0"
				print "ExitDesc: Instance %s has already been stopped"%(Instance)
				log.info('ExitCode: 0')
				log.info('ExitDesc: Instance %s has already been stopped'%(Instance))
				Status="Instance already stopped"
			else:
				print "ExitCode: 0"
				print "Exitdesc: Successfully stopped the instance."
				log.info('ExitCode:0')
				log.info('Info: Successfully stopped the instance.')
				Status="Successfully stopped instance"					
		else:
			print "ExitCode:10"
			print "ExitDesc:Enter proper Execution_Location input"
			log.info("ExitCode:10")
			log.info("ExitDesc:Enter proper Execution_Location input")
						
	else:
		print "ExitCode: 1"
		print "ExitDesc: Missing Arguments"
		log.info('Exitcode: 1')
		log.info('ExitDesc: Missing Arguments')
		Status="Error Occurred. Check Logs"
        
except Exception, e:
	log.info('Error: {0}'.format(e))
	print "ExitCode: 1"
	print "ExitDesc: {0}".format(e)
	Status="Error Occurred. Check Logs"

	
	
################################ Mail part ##################################


now = datetime.now()
dt = now.strftime("%A,%d-%B-%y")
dt=str(dt)
FROM  = '%s'%frommail
TO = '%s'%tomail

SUBJECT = 'STOP INSTANCE PROCESS'
body ="""
<html>
<H1> Database Status for %s </H1>
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
<TH>  Instance  </TH>
<TH>  Status </TH>
</TR>
<TR>
<TD>  %s  </TD>
<TD>  %s  </TD>
<TD>  %s  </TD>
<TD>  %s  </TD>
<TD>  %s  </TD>
</TR> 
</TABLE>
</HTML>""" %(dt,Execution_Location,HostName,Sid,Instance,Status)
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
