"""
	Name: ASM_RAC_Cluster_Status_Without_Sudo_Brakes.py
	Description: To check RAC and ASM cluster status on remote or local system
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
	if len(sys.argv) == 6:
		##Script Variables##
		Execution_Location=sys.argv[1]
		HostName = sys.argv[2]  		#Target HostName  	
		OSUser = sys.argv[3]			#Target Host user name to connect 
		OSPassword = sys.argv[4]		#Target Host user password to connect
		#Listener = sys.argv[5]			#Listener name
		Sid=sys.argv[5]					#SID or Database name
		Execution_Location=Execution_Location.upper()
		
	
		if Execution_Location=="REMOTE":
			
			dssh = paramiko.SSHClient()
			dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			dssh.connect(HostName, username=OSUser, password=OSPassword)

					
	
	####################################################### Command to Scan Status ####################################################
	
	
			command1="srvctl status scan"
			stdin, stdout, stderr = dssh.exec_command(command1)
			output1 = stdout.read()
			log.info('The command is %s'%(command1))
			log.info('the output is %s'%(output1))
			
			
			if "ERROR" in output1:
				print "ExitCode: 1"
				print "ExitDesc: %s" %(output1)
				log.info('Exitcode: 1')
				log.info('Error: {0}'.format(output1))
				Status="Error Occurred. Check Logs"
				
				
####################################################### Command to Scan Config ####################################################


			command2="srvctl config scan"
			stdin, stdout, stderr = dssh.exec_command(command2)
			output2 = stdout.read()
			log.info('The command is %s'%(command2))
			log.info('the output is %s'%(output2))
			
			
			if "ERROR" in output2:
				print "ExitCode: 1"
				print "ExitDesc: Status check failed \n %s" %(output2)
				log.info('Exitcode: 1')
				log.info('Error: {0}'.format(output2))
				Status="Error Occurred. Check Logs"				
			else:
				print "ExitCode: 0"
				print "ExitDesc: ASM_RAC Cluster status check performed successfully"
				log.info('ExitCode: 0')
				log.info('ExitDesc: ASM_RAC Cluster status check performed successfully')
				
		

############################################### For Local Execution ###########################################
		
		elif Execution_Location=="LOCAL":
								
					
					
	####################################################### Command to Scan Status ####################################################
	
	
			command1="srvctl status scan"
			stdin, stdout, stderr = dssh.exec_command(command1)
			output1 = stdout.read()
			log.info('The command is %s'%(command1))
			log.info('the output is %s'%(output1))
			
			
			if "ERROR" in output1:
				print "ExitCode: 1"
				print "ExitDesc: %s" %(output1)
				log.info('Exitcode: 1')
				log.info('Error: {0}'.format(output1))
				Status="Error Occurred. Check Logs"
				
				
	####################################################### Command to Scan Config ####################################################


			command2="srvctl config scan"
			stdin, stdout, stderr = dssh.exec_command(command2)
			#output2 = stdout.read()
			if stdout.read():
				output2=stdout.read()
			else:
				output2="Error"
			log.info('The command is %s'%(command2))
			log.info('the output is %s'%(output2))
			
			
			if "ERROR" in output2:
				print "ExitCode: 1"
				print "ExitDesc: Status check failed \n %s" %(output2)
				log.info('Exitcode: 1')
				log.info('Error: {0}'.format(output2))
				Status="Error Occurred. Check Logs"				
			else:
				print "ExitCode: 0"
				print "ExitDesc: ASM_RAC Cluster status check performed successfully"
				log.info('ExitCode: 0')
				log.info('ExitDesc: ASM_RAC Cluster status check performed successfully')
				
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

SUBJECT = 'ASM RAC CLUSTER STATUS CHECK PROCESS'
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
<TH>  Output1  </TH>
<TH>  Output2 </TH>
</TR>
<TR>
<TD>  %s  </TD>
<TD>  %s  </TD>
<TD>  %s  </TD>
<TD>  %s  </TD>
<TD>  %s  </TD>
</TR> 
</TABLE>
</HTML>""" %(dt,Execution_Location,HostName,Sid,output1,output2)
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
