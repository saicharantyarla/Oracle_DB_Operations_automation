"""
Name: Create_Tablespace_Without_Sudo.py
Description: Executed as Remote or Local to  Create Permanent/UNDO/Temporary Tablespace
Team: Software Service Automation
Author: Saicharan Tyarla(sai-charan.thyarla@capgemini.com)
Inputs: Arguments [Hostname,DBUsername,DBPassword,TNSName,Tablespace,Size, Drive, Autoextent, MaxSize, bigfile,Execution_Location], LogFileLoc,TablespaceType
Output: Logfile, Outlogfile

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



if len(sys.argv) == 13:
	Execution_Location=sys.argv[1]
	Execution_Location=Execution_Location.upper()
	HostName = sys.argv[2] 
	OSUser = sys.argv[3] 
	OSPassword = sys.argv[4]
	Sid=sys.argv[5]
	#ctl_file_path=sys.argv[6]
	TablespaceName = sys.argv[6]#Tablespace Name
	TablespaceName=TablespaceName.upper()
	bigfile = sys.argv[7]#Big if Big file is selected	
	bigfile=bigfile.upper()
	Size = sys.argv[8]#Size of the Datafile	
	Autoextent = sys.argv[9]#Option to Auto extend	
	Autoextent=Autoextent.upper()
	MaxSize = sys.argv[10]#Maxsize of the tablespace
	TablespaceType=sys.argv[11]#Type of the tablespace
	TablespaceType = TablespaceType.upper()
	Datafilename=sys.argv[12] # Enter the datafilename
	Status=""
	Ora_Home_Sid=""
	count=0
	
	################################### Creating Log File ###############################
	try:
		if os.name == 'nt':
			logdir = os.getcwd()+"\\logs"
		if os.name == 'posix':
			logdir = os.getcwd()+"/logs"
		
		logfile = "Creating_Tablespace_%s.log"%(HostName)
		log = Logger(logdir,logfile)

		log.info('*************************************************************************')
		#print "Log file created"
		log.info('Started Script Execution')
		
	except Exception, e:
		print "ExitCode: 10"
		print "ExitDesc: Unable to create Logfile {0} {1}".format(logfile,e)

	################################### END OF LOG FILE CREATION ######################################
	
	try:
		log.info("Given input is %s"%Execution_Location)
		
########################################################### FOR REMOTE EXECUTION #######################################################################		
		
		if Execution_Location=="REMOTE":
			
			dssh = paramiko.SSHClient()
			dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			dssh.connect(HostName, username=OSUser, password=OSPassword)

			#loginline=". ~/.bash_profile\nsqlplus -s / as sysdba"	
			#loginline="sqlplus -s / as sysdba"
			loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid
			command="select tablespace_name from dba_tablespaces where tablespace_name = '%s';"%(TablespaceName)
			ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command)
			log.info('Executing Query: {0}'.format(command))
			stdin, stdout, stderr = dssh.exec_command(ucommand)
			output1=stdout.read()
			log.info('The command is: %s'%ucommand)
			log.info('The output is: %s'%output1)
			er= stderr.read()
			if er is not None:
				log.info('The error if any is: %s' %er)
			
			if "ERROR" not in output1:
				if TablespaceName in output1:
					log.info("ExitCode: 10")
					log.info("ExitDesc: Tablespace name already exists")
					print "ExitCode: 10"
					print "ExitDesc: Tablespacename already exists"
					Status="Tablespacename already exists"
				else:
					if TablespaceType=="PERMANENT":
						if Autoextent == 'TRUE':
							query = "create tablespace %s datafile '%s' size %sM autoextend on next 100m maxsize %sM;"%(TablespaceName,Datafilename,Size,MaxSize)
							if bigfile == 'TRUE':
								query = "create bigfile tablespace %s datafile '%s' size %sM autoextend on next 100m maxsize %sM;"%(TablespaceName,Datafilename,Size,MaxSize)
						elif Autoextent == 'FALSE':
							query = "create tablespace %s datafile '%s' size %sM;"%(TablespaceName,Datafilename,Size)
							if bigfile == 'TRUE':
								query = "create bigfile tablespace %s datafile '%s' size %sM;"%(TablespaceName,Datafilename,Size)
						else:
							log.info("ExitCode:10")
							log.info("ExitDesc:Enter TRUE/FALSE as an input")
							Status="Error Occurred. Check Logs"
						ucommand1 = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,query)
						log.info('Trying to Execute the command : {0}'.format(ucommand1))
						stdin, stdout, stderr = dssh.exec_command(ucommand1)
						output1 = stdout.read()
						Error=stderr.read()
						log.info("Fetching the output")
						log.info("Output:%s"%output1)
						out = output1.split("\n")
						for line in out:
							if "ERROR" in line:
								count = count+1
						log.info("No. of errors : %s"%count)
						if count == 0:
							log.info("Validating wether tablespace is created or not")
							command_val="select tablespace_name from dba_tablespaces where tablespace_name = '%s';"%(TablespaceName)
							ucommand_val = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command_val)
							log.info('Command for script Execution:%s'%ucommand_val)
							#print ucommand
							stdin, stdout, stderr = dssh.exec_command(ucommand_val)
							Final_output = stdout.read()
							Error=stderr.read()
							log.info("The output is %s"%Final_output)
							
							if "ERROR" not in Final_output and "ORA-" not in Final_output:
								if TablespaceName in Final_output:
									log.info("ExitCode: 0")
									log.info("ExitDesc: Tablespace created Successfully")
									print "ExitCode: 0"
									print "ExitDesc: Tablespace created Successfully"
									Status="Tablespace Created Successfully"
								else:
									log.info("ExitCode: 1")
									log.info("ExitDesc: Tablespace Creation Failed")
									print "ExitCode:1"
									print "ExitDesc: Tablespace Creation Failed"
									Status="Error Occurred. Check Logs"
							else:
								log.info("ExitCode: 1")
								log.info("The Error is %s"%Error)
								log.info("ExitDesc: Some Error found while executing command")
								print "ExitCode:1"
								print "ExitDesc:Some Error found while executing command"
								Status="Error Occurred. Check Logs"
						else:
							log.info("ExitCode: 1")
							log.info("The Error is %s"%Error)
							log.info("ExitDesc: Some Error found while executing command")
							print "ExitCode:1"
							print "ExitDesc:Some Error found while executing command"
							Status="Error Occurred. Check Logs"
					elif TablespaceType=="UNDO":
						log.info("User Selected TablespaceType as %s"%TablespaceType)
						if Autoextent == 'TRUE':
							query = "create undo tablespace %s datafile '%s' size %sM autoextend on next 100m maxsize %sM;"%(TablespaceName,Datafilename,Size,MaxSize)
						elif Autoextent == 'FALSE':
							query = "create undo tablespace %s datafile '%s' size %sM;"%(TablespaceName,Datafilename,Size)
						else:
							log.info("ExitCode:10")
							log.info("ExitDesc:Enter TRUE/FALSE as an input")
							print "ExitCode:10"
							print "ExitDesc:Enter TRUE/FALSE as an input"
							Status="Error Occurred. Check Logs"
						ucommand1 = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,query)
						log.info('Trying to Execute the command : {0}'.format(ucommand1))
						stdin, stdout, stderr = dssh.exec_command(ucommand1)
						output1 = stdout.read()
						Error=stderr.read()
						log.info("Fetching the output")
						log.info("Output:%s"%output1)
						out = output1.split("\n")
						for line in out:
							if "ERROR" in line:
								count = count+1
						log.info("No. of errors : %s"%count)
						if count == 0:
							log.info("Validating wether tablespace is created or not")
							command_val="select tablespace_name from dba_tablespaces where tablespace_name = '%s';"%(TablespaceName)
							ucommand_val ="%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command_val)
							log.info('Command for script Execution:%s'%ucommand_val)
							#print ucommand
							stdin, stdout, stderr = dssh.exec_command(ucommand_val)
							Final_output = stdout.read()
							Error=stderr.read()
							log.info("The output is %s"%Final_output)
							
							if "ERROR" not in Final_output and "ORA-" not in Final_output:
								if TablespaceName in Final_output:
									log.info("ExitCode: 0")
									log.info("ExitDesc: Tablespace created Successfully")
									print "ExitCode: 0"
									print "ExitDesc: Tablespace created Successfully"
									Status="Tablespace Created Successfully"
								else:
									log.info("ExitCode: 1")
									log.info("ExitDesc: Tablespace Creation Failed")
									print "ExitCode:1"
									print "ExitDesc: Tablespace Creation Failed"
									Status="Error Occurred. Check Logs"
							else:
								log.info("ExitCode: 1")
								log.info("The Error is %s"%Error)
								log.info("ExitDesc: Some Error found while executing command")
								print "ExitCode:1"
								print "ExitDesc:Some Error found while executing command"
								Status="Error Occurred. Check Logs"
						else:
							log.info("ExitCode: 1")
							log.info("The Error is %s"%Error)
							log.info("ExitDesc: Some Error found while executing command")
							print "ExitCode:1"
							print "ExitDesc:Some Error found while executing command"
							Status="Error Occurred. Check Logs"
					elif TablespaceType == "TEMP" or TablespaceType == "TEMPORARY":
						if Autoextent == 'TRUE':
							query = "create TEMPORARY tablespace %s tempfile '%s' size %sM autoextend on next 100m maxsize %sM;"%(TablespaceName,Datafilename,Size,MaxSize)
						elif Autoextent == 'FALSE':
							query = "create TEMPORARY tablespace %s tempfile '%s' size %sM;"%(TablespaceName,Datafilename,Size)
						else:
							log.info("ExitCode:10")
							log.info("ExitDesc:Enter TRUE/FALSE as an input")
							print "ExitCode:10"
							print "ExitDesc:Enter TRUE/FALSE as an input"
							Status="Error Occurred. Check Logs"
						ucommand1 = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,query)
						log.info('Trying to Execute the command : {0}'.format(ucommand1))
						stdin, stdout, stderr = dssh.exec_command(ucommand1)
						output1 = stdout.read()
						Error=stderr.read()
						log.info("Fetching the output")
						log.info("Output:%s"%output)
						out = output1.split("\n")
						for line in out:
							if "ERROR" in line:
								count = count+1
						log.info("No. of errors : %s"%count)
						if count == 0:
							log.info("Validating wether tablespace is created or not")
							command_val="select tablespace_name from dba_tablespaces where tablespace_name = '%s';"%(TablespaceName)
							ucommand_val = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command_val)
							log.info('Command for script Execution:%s'%ucommand_val)
							#print ucommand
							stdin, stdout, stderr = dssh.exec_command(ucommand_val)
							Final_output = stdout.read()
							Error=stderr.read()
							log.info("The output is %s"%Final_output)
							
							if "ERROR" not in Final_output and "ORA-" not in Final_output:
								if TablespaceName in Final_output:
									log.info("ExitCode: 0")
									log.info("ExitDesc: Tablespace created Successfully")
									print "ExitCode: 0"
									print "ExitDesc: Tablespace created Successfully"
									Status="Tablespace Creation Successfull"
								else:
									log.info("ExitCode: 1")
									log.info("ExitDesc: Tablespace Creation Failed")
									print "ExitCode:1"
									print "ExitDesc: Tablespace Creation Failed"
									Status="Error Occurred. Check Logs"
							else:
								log.info("ExitCode: 1")
								log.info("The Error is %s"%Error)
								log.info("ExitDesc: Some Error found while executing command")
								print "ExitCode:1"
								print "ExitDesc:Some Error found while executing command"
								Status="Error Occurred. Check Logs"
						else:
							log.info("ExitCode: 10")
							log.info("ExitDesc: Invalid tablespace Type")
							print "ExitCode:10"
							print "ExitDesc:Invalid tablespace Type"
							Status="Invalid TablespaceType"
					else:
						log.info("ExitCode: 10")
						log.info("ExitDesc: Error while executing query %s"%command)
						log.info("ExitDesc: Error :%s"%output1)
						print "ExitCode:10"
						print "ExitDesc: Error while executing query"
						Status="Error Occurred. Check Logs"
							
			else:
				log.info("ExitCode: 10")
				log.info("ExitDesc: Error while executing query %s"%command)
				log.info("ExitDesc: Error :%s"%output1)
				print "ExitCode:10"
				print "ExitDesc: Error while executing query"
				Status="Error Occurred. Check Logs"
					

					
########################################################### FOR LOCAL EXECUTION #######################################################################					
			
		elif Execution_Location == "LOCAL":
			
			
			#loginline=". ~/.bash_profile\nsqlplus -s / as sysdba"
			#loginline="sqlplus -s / as sysdba"
			loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid
			command="select tablespace_name from dba_tablespaces where tablespace_name = '%s';"%(TablespaceName)
			ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command)
			log.info('Command for script Execution:%s'%ucommand)
			output=os.popen(ucommand)
			log.info('Command execution on the target server is done')
			output=output.read()
			log.info("The output is %s"%output)
			if "ERROR" not in output:
				if TablespaceName in output:
					log.info("ExitCode: 10")
					log.info("ExitDesc: Tablespacename already exists")
					print "ExitCode: 10"
					print "ExitDesc: Tablespacename already exists"
					Status="Error Occurred. Check Logs"
				else:
					if TablespaceType=="PERMANENT":
						if Autoextent == 'TRUE':
							query = "create tablespace %s datafile '%s' size %sM autoextend on next 100m maxsize %sM;"%(TablespaceName,Datafilename,Size,MaxSize)
							if bigfile == 'TRUE':
								query = "create bigfile tablespace %s datafile '+%s' size %sM autoextend on next 100m maxsize %sM;"%(TablespaceName,Datafilename,Size,MaxSize)
						elif Autoextent == 'FALSE':
							query = "create tablespace %s datafile '%s' size %sM;"%(TablespaceName,Datafilename,Size)
							if bigfile == 'TRUE':
								query = "create bigfile tablespace %s datafile '+%s' size %sM;"%(TablespaceName,Datafilename,Size)
						else:
							log.info("ExitCode:10")
							log.info("ExitDesc:Enter TRUE/FALSE as an input")
							print "ExitCode:10"
							print "ExitDesc:Enter TRUE/FALSE as an input"
							Status="Error Occurred. Check Logs"
						ucommand1 = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,query)
						log.info('Trying to Execute the command : {0}'.format(ucommand1))
						output1=os.popen(ucommand1)
						log.info('Command execution on the target server is done')
						output1=output1.read()
						log.info("Fetching the output")
						log.info("Output:%s"%output)
						out = output1.split("\n")
						for line in out:
							if "ERROR" in line:
								count = count+1
						log.info("No. of errors : %s"%count)
						if count == 0:
							log.info("Validating wether tablespace is created or not")
							command_val="select tablespace_name from dba_tablespaces where tablespace_name = '%s';"%(TablespaceName)
							ucommand_val = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command_val)
							log.info('Command for script Execution:%s'%ucommand_val)
							Final_output=os.popen(ucommand_val)
							log.info('Command execution on the target server is done')
							Final_output=Final_output.read()

							log.info("The output is %s"%Final_output)
							
							if "ERROR" not in Final_output and "ORA-" not in Final_output:
								if TablespaceName in Final_output:
									log.info("ExitCode: 0")
									log.info("ExitDesc: Tablespace created Successfully")
									print "ExitCode: 0"
									print "ExitDesc: Tablespace created Successfully"
									Started="Tablespace Created Successfully"
								else:
									log.info("ExitCode: 1")
									log.info("ExitDesc: Tablespace Creation Failed")
									print "ExitCode:1"
									print "ExitDesc: Tablespace Creation Failed"
									Status="Error Occurred. Check Logs"
							else:
								log.info("ExitCode: 1")
								log.info("The Error is %s"%Error)
								log.info("ExitDesc: Some Error found while executing command")
								print "ExitCode:1"
								print "ExitDesc:Some Error found while executing command"
								Status="Error Occurred. Check Logs"
						else:
							log.info("ExitCode: 1")
							log.info("The Error is %s"%Error)
							log.info("ExitDesc: Some Error found while executing command")
							print "ExitCode:1"
							print "ExitDesc:Some Error found while executing command"
							Status="Error Occurred. Check Logs"
					elif TablespaceType=="UNDO":
						log.info("User Selected TablespaceType as %s"%TablespaceType)
						if Autoextent == 'TRUE':
							query = "create undo tablespace %s datafile '%s' size %sM autoextend on next 100m maxsize %sM;"%(TablespaceName,Datafilename,Size,MaxSize)
						elif Autoextent == 'FALSE':
							query = "create undo tablespace %s datafile '%s' size %sM;"%(TablespaceName,Datafilename,Size)
						else:
							log.info("ExitCode:10")
							log.info("ExitDesc:Enter TRUE/FALSE as an input")
							print "ExitCode:10"
							print "ExitDesc:Enter TRUE/FALSE as an input"
							Status="Error Occurred. Check Logs"
						ucommand1 = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,query)
						log.info('Trying to Execute the command : {0}'.format(ucommand1))
						output1=os.popen(ucommand1)
						output1=output1.read()
						log.info("Fetching the output")
						log.info("Output:%s"%output1)
						out = output1.split("\n")
						for line in out:
							if "ERROR" in line:
								count = count+1
						log.info("No. of errors : %s"%count)
						if count == 0:
							log.info("Validating wether tablespace is created or not")
							command_val="select tablespace_name from dba_tablespaces where tablespace_name = '%s';"%(TablespaceName)
							ucommand_val = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command_val)
							log.info('Command for script Execution:%s'%ucommand_val)
							#print ucommand
							Final_output=os.popen(ucommand_val)
							log.info('Command execution on the target server is done')
							Final_output=Final_output.read()

							log.info("The output is %s"%Final_output)
							
							if "ERROR" not in Final_output and "ORA-" not in Final_output:
								if TablespaceName in Final_output:
									log.info("ExitCode: 0")
									log.info("ExitDesc: Tablespace created Successfully")
									print "ExitCode: 0"
									print "ExitDesc: Tablespace created Successfully"
									Status="Tablespace Created Successfully"
								else:
									log.info("ExitCode: 1")
									log.info("ExitDesc: Tablespace Creation Failed")
									print "ExitCode:1"
									print "ExitDesc: Tablespace Creation Failed"
									Status="Error Occurred. Check Logs"
							else:
								log.info("ExitCode: 1")
								#log.info("The Error is %s"%Error)
								log.info("ExitDesc: Some Error found while executing command")
								print "ExitCode:1"
								print "ExitDesc:Some Error found while executing command"
								Status="Error Occurred. Check Logs"
						else:
							log.info("ExitCode: 1")
							#log.info("The Error is %s")
							log.info("ExitDesc: Some Error found while executing command")
							print "ExitCode:1"
							print "ExitDesc:Some Error found while executing command"
							Status="Error Occurred. Check Logs"
					elif TablespaceType == "TEMP" or TablespaceType == "TEMPORARY":
						if Autoextent == 'TRUE':
							query = "create TEMPORARY tablespace %s tempfile '%s' size %sM autoextend on next 100m maxsize %sM;"%(TablespaceName,Datafilename,Size,MaxSize)
						elif Autoextent == 'FALSE':
							query = "create TEMPORARY tablespace %s tempfile '%s' size %sM;"%(TablespaceName,Datafilename,Size)
						else:
							log.info("ExitCode:10")
							log.info("ExitDesc:Enter TRUE/FALSE as an input")
							print "ExitCode:10"
							print "ExitDesc:Enter TRUE/FALSE as an input"
							Status="Error Occurred. Check Logs"
						ucommand1 = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,query)
						log.info('Trying to Execute the command : {0}'.format(ucommand1))
						output1=os.popen(ucommand1)
						output1=output1.read()
						log.info("Fetching the output")
						log.info("Output:%s"%output1)
						out = output1.split("\n")
						for line in out:
							if "ERROR" in line:
								count = count+1
						log.info("No. of errors : %s"%count)
						if count == 0:
							log.info("Validating wether tablespace is created or not")
							command_val="select tablespace_name from dba_tablespaces where tablespace_name = '%s';"%(TablespaceName)
							ucommand_val = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command_val)
							log.info('Command for script Execution:%s'%ucommand_val)
							Final_output=os.popen(ucommand_val)
							Final_output=Final_output.read()
							log.info("The output is %s"%Final_output)
							
							if "ERROR" not in Final_output and "ORA-" not in Final_output:
								if TablespaceName in Final_output:
									log.info("ExitCode: 0")
									log.info("ExitDesc: Tablespace created Successfully")
									print "ExitCode: 0"
									print "ExitDesc: Tablespace created Successfully"
									Status="Tablespace created Successfully"
								else:
									log.info("ExitCode: 1")
									log.info("ExitDesc: Tablespace Creation Failed")
									print "ExitCode:1"
									print "ExitDesc: Tablespace Creation Failed"
									Status="Error Occurred. Check Logs"
							else:
								log.info("ExitCode: 1")
								#log.info("The Error is %s")
								log.info("ExitDesc: Some Error found while executing command")
								print "ExitCode:1"
								print "ExitDesc:Some Error found while executing command"
								Status="Error Occurred. Check Logs"
						else:
							log.info("ExitCode: 10")
							log.info("ExitDesc: Invalid tablespace Type")
							print "ExitCode:10"
							print "ExitDesc:Invalid tablespace Type"
							Status="Error Occurred. Check Logs"
					else:
						log.info("ExitCode: 10")
						log.info("ExitDesc: Error while executing query %s"%command)
						log.info("ExitDesc: Error :%s"%output)
						print "ExitCode:10"
						print "ExitDesc: Error while executing query"
						Status="Error Occurred. Check Logs"
							
			else:
				log.info("ExitCode: 10")
				log.info("ExitDesc: Error while executing query %s"%command)
				log.info("ExitDesc: Error :%s"%output)
				print "ExitCode:10"
				print "ExitDesc: Error while executing query"
				Status="Error Occurred. Check Logs"

		else:
			log.info("ExitCode:10")
			log.info("ExitDesc:Enter proper Execution_Location")
			print "ExitCode:10"
			print "ExitDesc:Enter proper Execution_Location"
			Status="Enter proper Execution_Location"

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

SUBJECT = ' Tablespace Creation '
body ="""
<html>
<H2> Tablespace Creation %s </H2>
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
				
			
