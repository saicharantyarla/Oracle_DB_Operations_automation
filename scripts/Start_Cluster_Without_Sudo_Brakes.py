"""
	Name: Start_Cluster_Without_Sudo.py
	Description: Start a Cluster 
	Team: Software Service Automation
	Author: Saicharan Tyarla(sai-charan.thyarla@capgemini.com)
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

if len(sys.argv) == 5:
	Execution_Location=sys.argv[1]
	Execution_Location=Execution_Location.upper()
	HostName = sys.argv[2] 
	OSUser = sys.argv[3] 
	OSPassword = sys.argv[4]
	Status=""
	Ora_Home_Sid=""
	 

	try:
		if os.name == 'nt':
			logdir = os.getcwd()+"\\logs"
		if os.name == 'posix':
			logdir = os.getcwd()+"/logs"
		
		logfile = "Start_Cluster_%s.log"%(HostName)
		log = Logger(logdir,logfile)

		log.info('*************************************************************************')
		#print "Log file created"
		log.info('Started Script Execution')
		
	except Exception, e:
		print "ExitCode: 10"
		print "ExitDesc: Unable to create Logfile {0} {1}".format(logfile,e)

	################################### END OF LOG FILE CREARION ######################################
		
	try:
		if Execution_Location=="REMOTE":
			log.info('Started Script Execution in remote location')
			command = "$GRID_HOME/bin/crsctl start cluster -all"
			log.info("The command is ... %s"%command)
			dssh = paramiko.SSHClient()
			dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			dssh.connect(HostName, username=OSUser, password=OSPassword)
			log.info('Server Connection Successful')
			stdin, stdout, stderr = dssh.exec_command(command)
			output = stdout.read()
			errout = stderr.read()
			log.info("The output is : %s "%output)
			if "ERROR" not in output and "ORA-" not in output and "sp-" not in output:
				if errout:
					log.info("The error is %s"%errout)
					print "ExitCode: 1"
					print "ExitDesc: Error Occured:%s"%errout
					log.info("ExitCode: 1")
					log.info("ExitDesc: Error Occured:%s"%errout)						
					Status="Some error Occured. Check logs"					
				else:
					log.info("ExitCode:0")
					log.info("ExitDesc:Cluster started successfully")
					print "ExitCode:0"
					print "ExitDesc:Cluster started successfully"
					Status="The Cluster Started Successfully"
			else:
				print "ExitCode: 1"
				print "ExitDesc: Error Occured:%s"%output
				log.info("ExitCode: 1")
				log.info("ExitDesc: Error Occured:%s"%output)						
				Status="Some error Occured. Check logs"
			
		elif Execution_Location=="LOCAL":
			log.info('Started Script Execution in remote location')
			command = "$GRID_HOME/bin/crsctl start cluster -all"
			log.info("The command is ... %s"%command)
			output=os.popen(command).read()
			log.info("The output is %s"%output)
			if "ERROR" not in output and "ORA-" not in output and "sp-" not in output:
				log.info("ExitCode:0")
				log.info("ExitDesc:Cluster started successfully")
				print "ExitCode:0"
				print "ExitDesc:Cluster started successfully"
				Status="The Cluster Started Successfully"
			else:
				print "ExitCode: 1"
				print "ExitDesc: Error Occured:%s"%output
				log.info("ExitCode: 1")
				log.info("ExitDesc: Error Occured:%s"%output)						
				Status="Some error Occured. Check logs"	
		else:
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

SUBJECT = ' Start Cluster  '
body ="""
<html>
<H2> Start Cluster %s </H2>
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
<tr><th>HostName </th> <th>Execution Location </th> <th> Status</th>  </tr>
<tr> <td>%s</td><td>%s</td><td>%s</td></tr>
</table>
</body>	
</html>"""%(dt,HostName,Execution_Location,Status)


part1="""From: %s 
To: %s 
Subject: %s
Content-Type: multipart/mixed;
""" %(frommail, tomail, SUBJECT)

part2 = """Content-Type: text/html
%s
""" %body

log.info("the Html code is %s "%body)
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
