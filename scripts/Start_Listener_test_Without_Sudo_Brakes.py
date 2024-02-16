"""
	Name: Start_Listener_test_Without_Sudo.py
	Description: To startup the listener on remote or local system
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

	logfile = "Start_Listener.log"
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
		Listener = sys.argv[5]			#Listener name
		Sid=sys.argv[6]					#SID or Database name
		Execution_Location=Execution_Location.upper()
		
	
		if Execution_Location=="REMOTE":
			
						
	####################################################### Command to Start Listener ####################################################
	

			#command1="lsnrctl start %s"%Listener
			command1="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv>/dev/null 2>&1\nlsnrctl start %s"%(Sid,Listener)
			dssh = paramiko.SSHClient()
			dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			dssh.connect(HostName, username=OSUser, password=OSPassword)			
			stdin, stdout, stderr = dssh.exec_command(command1)
			output2 = stdout.read()
			#inp = stdin.read()
#			error=stderr.read()
			#log.info('Input: %s' %(inp))
#			log.info('Err
			log.info('The command is %s'%(command1))
			log.info('the output is %s'%(output2))
			error=stderr.read()
			log.info("If any error %s"%(error))
			
			if output2 and "ERROR" in output2:
				print "ExitCode: 1"
				print "ExitDesc: %s" %(output2)
				log.info('Exitcode: 1')
				log.info('Error: {0}'.format(output2))
				Status="Error Occurred. Check Logs"
			elif "has already been started" in output2:
				print "ExitCode: 0"
				print "ExitDesc: Listener using listener name %s has already been started"%(Listener)
				log.info('ExitCode: 0')
				log.info('Error: Listener using listener name %s has already been started'%(Listener))
				Status="Listener already started"	
			elif "TNS-" in output2:
				print "ExitCode: 10"
				print "ExitDesc: Could not find listener name or service name"
				log.info('Exitcode: 10')
				log.info('Error: Could not find listener name or service name')
				Status="Error. Could not find listener name"
			elif "successfully" in output2 or "listening" in output2:
				print "ExitCode: 0"
				print "Exitdesc: Successfully started the listeners."
				log.info('ExitCode:0')
				log.info('Info: Successfully started the listeners.')
				Status="Successfully started listener"
                        else:
				print "ExitCode: 10"
				print "ExitDesc: Error %s" % (err)
				log.info('ExitCode:10')
				log.info('ExitDesc: Error: {0}'.format(err))
				Status="Error Occurred. Check Logs"
				



############################################### For Local Execution ###########################################
		
		elif Execution_Location=="LOCAL":
	############################################################################ COommand to Start the Listener #############################################
			command1="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv>/dev/null 2>&1\nlsnrctl start %s"%(Sid,Listener)
			output = os.popen(command1).read()
			log.info("The command is %s"%command1)
			log.info("The output is %s "%output)
			if "ERROR" in output:
				print "ExitCode: 1"
				print "ExitDesc: %s" %(err)
				log.info('Exitcode: 1')
				Status="Error Occurred. Check Logs"
				log.info('Error: {0}'.format(err))
			elif "has already been started" in output:
				print "ExitCode: 0"
				print "ExitDesc: Listener using listener name %s has already been started"%(Listener)
				log.info('Exitcode: 0')
				log.info('Error: Listener using listener name %s has already been started'%(Listener))
				Status="Listener already started"
			elif "TNS-" in output:
				print "ExitCode: 10"
				print "ExitDesc: Could not find listener name or service name"
				log.info('Exitcode: 10')
				log.info('Error: Could not find listener name or service name')
				Status="Error. Could not find listener name"
			elif "successfully" in output or "listening" in output  :
				print "ExitCode: 0"
				print "Exitdesc: Successfully started the listeners."
				log.info('ExitCode:0')
				log.info('Info: Successfully started the listeners.')
				Status="Successfully started listener"
			else:
				print "ExitCode: 10"
				print "ExitDesc: Error %s" % (err)
				log.info('ExitCode:10')
				log.info('ExitDesc: Error: {0}'.format(err))
				Status="Error Occurred. Check Logs"
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


SUBJECT = 'START LISTENER PROCESS'
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
<TH>  Listener  </TH>
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
</HTML>""" %(dt,Execution_Location,HostName,Sid,Listener,Status)
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
	log.info("Email Sent Successfully")
	log.info("Email Sent Successfully")
	print "Email sent"
	
except Exception, e:
	print "Email sending failed due to: {0}".format(e)
