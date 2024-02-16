"""
	Name: Alter_privileges_Without_Sudo_Brakes.py
	Description: Altering privileges to a user Without Sudo, remote target server or local target server
	Team: Software Service Automation
	Author: Saicharan Tyarla(sai-charan.thyarla@capgemini.com)
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


if len(sys.argv) == 11:
	Execution_Location=sys.argv[1]
	HostName = sys.argv[2] 
	OSUser = sys.argv[3] 
	OSPassword = sys.argv[4]
	Sid=sys.argv[5]
	Privilege_Type=sys.argv[6] # GRANT/REVOKE Type of privilege
	Privilege_Type=Privilege_Type.upper()
	privilege_name=sys.argv[7] #the type of privilege(Select/Insert/update/alter) wants to assign to the user
	#Multiple privileges were also allowed here 
	privilege_name=privilege_name.upper()
	schema_name=sys.argv[8]		#The ownername of the object
	schema_name=schema_name.upper()
	object_name=sys.argv[9]		# On which object (Table/Schema/index) owner wants to give privilege
	object_name=object_name.upper()
	user_name=sys.argv[10]		# to which user the you want to assign privileges
	user_name=user_name.upper()
	Status=""
	Execution_Location=Execution_Location.upper()		
	################################### Creating Log File ###############################
	try:
		if os.name == 'nt':
			logdir = os.getcwd()+"\\logs"
		if os.name == 'posix':
			logdir = os.getcwd()+"/logs"
		
		logfile = "Alter_privileges_%s.log"%(HostName)
		log = Logger(logdir,logfile)

		log.info('*************************************************************************')
		#print "Log file created"
		log.info('Started Script Execution')
		
	except Exception, e:
		print "ExitCode: 10"
		print "ExitDesc: Unable to create Logfile {0} {1}".format(logfile,e)

	################################### END OF LOG FILE CREARION ######################################
	try:
		log.info("Given input is %s"%Execution_Location)
		if Execution_Location=="REMOTE":
			log.info('Started Script Execution in remote location')
			#loginline=". ~/.bash_profile\nsqlplus -S / as sysdbA"
			#loginline="sqlplus -s / as sysdba"
			loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid

			if Privilege_Type == "GRANT":
				log.info("The user selected GRANT privilege")
				command="GRANT %s on %s.%s to %s;"%(privilege_name,schema_name,object_name,user_name)
				ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command)
				dssh = paramiko.SSHClient()
				dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				dssh.connect(HostName, username=OSUser, password=OSPassword)
				log.info('Server Connection Successfull')
				log.info("The command is %s "%ucommand)
				stdin, stdout, stderr = dssh.exec_command(ucommand)
				output = stdout.read()
				log.info("The output is %s "%(output))
				if "ORA-" not in output and "ERROR" not in output:
					log.info("The command Executed successfully ")
					log.info("Validating wether the privileges assigned to the user or not")
					command1="select PRIVILEGE from user_tab_privs where GRANTEE='%s' and TABLE_NAME ='%s' and GRANTOR='%s';"%(user_name,object_name,schema_name)
					ucommand1 = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command1)
					stdin, stdout, stderr = dssh.exec_command(ucommand1)
					output1 = stdout.read()
					log.info("The output is %s "%(output1))
					error=stderr.read()
					log.info("The error if any is .. %s"%error)
					if output1 and privilege_name in output1 and "ORA-" not in output1 and "ERROR" not in output1:
						log.info("ExitCode:0")
						log.info("ExitDesc:The Grant privilege successful")
						print "ExitCode:0"
						print "ExitDesc:The Grant privilege successful"
						Status="Grant privileges successful"
					else:
						log.info("ExitCode:1")
						log.info("ExitDesc:Grant privilege failed check logs")
						print "ExitCode:1"
						print "ExitDesc: Grant privileges Failed"
						Status="Grant privilege failed check logs"
				else:
					log.info("ExitCode:10")
					log.info("ExitDesc:Error Occured while Executing command check logs")
					print "ExitCode:10"
					print "ExitDesc:Error occured while executing the check logs"
					Status="Error Occured while Executing the command check logs"
					
			elif Privilege_Type == "REVOKE":
				log.info("The user selected REVOKE privilege")
				command="REVOKE %s on %s.%s from %s;"%(privilege_name,schema_name,object_name,user_name)
				ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command)
				dssh = paramiko.SSHClient()
				dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				dssh.connect(HostName, username=OSUser, password=OSPassword)
				log.info('Server Connection Successfull')
				log.info("The command is %s "%ucommand)
				stdin, stdout, stderr = dssh.exec_command(ucommand)
				output = stdout.read()
				error=stderr.read()
				log.info("The error if any is .. %s"%error)
				log.info("The output is %s "%(output))
				if "ORA-" not in output and "ERROR" not in output:
					log.info("The command Executed successfully ")			
					log.info("ExitCode:0")
					log.info("ExitDesc:The REVOKE privilege successful")
					print "ExitCode:0"
					print "ExitDesc:The REVOKE privilege successful"
					Status="REVOKE privileges successful"
				else:
					log.info("ExitCode:1")
					log.info("ExitDesc:REVOKE privilege failed check logs")
					print "ExitCode:1"
					print "ExitDesc: REVOKE	privileges Failed"
					Status="REVOKE privilege failed check logs"	
			else:
				log.info("ExitCode:10")
				log.info("ExitDesc:Enter the GRANT/REVOKE for the Privilege_Type")
				print "ExitCode:10"
				print "ExitDesc:Enter the GRANT/REVOKE for the Privilege_Type"
		elif Execution_Location == "LOCAL":
			log.info("Local Execution starts..")
			#loginline="sqlplus -s / as sysdba"
			#loginline=". ~/.bash_profile\nsqlplus -S / as sysdbA"
			loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid
			if Privilege_Type == "GRANT":
				log.info("The user selected GRANT privilege")
				command="GRANT %s on %s.%s to %s;"%(privilege_name,schema_name,object_name,user_name)
				ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command)
				log.info("The command is %s "%ucommand)
				output = os.popen(ucommand).read()
				log.info("The output is %s "%(output))
				if "ORA-" not in output and "ERROR" not in output:
					log.info("The command Executed successfully ")
					log.info("Validating wether the privileges assigned to the user or not")
					command1="select PRIVILEGE from user_tab_privs where GRANTEE='%s' and TABLE_NAME ='%s' and GRANTOR='%s';"%(user_name,object_name,schema_name)
					ucommand1 = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command1)
					output1 = os.popen(ucommand1).read()
					if output1 and privilege_name in output1 and "ORA-" not in output1 and "ERROR" not in output1:
						log.info("ExitCode:0")
						log.info("ExitDesc:The Grant privilege successful")
						print "ExitCode:0"
						print "ExitDesc:The Grant privilege successful"
						Status="Grant privileges successful"
					else:
						log.info("ExitCode:1")
						log.info("ExitDesc:Grant privilege failed check logs")
						print "ExitCode:1"
						print "ExitDesc: Grant privileges Failed"
						Status="Grant privilege failed check logs"
				else:
					log.info("ExitCode:10")
					log.info("ExitDesc:Error Occured while Executing command check logs")
					print "ExitCode:10"
					print "ExitDesc:Error occured while executing the check logs"
					Status="Error Occured while Executing the command check logs"
			elif Privilege_Type == "REVOKE":
				log.info("The user selected REVOKE privilege")
				command="REVOKE %s on %s.%s from %s;"%(privilege_name,schema_name,object_name,user_name)
				ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command)
				output = os.popen(ucommand).read()
				log.info("The output is %s "%(output))
				if "ORA-" not in output and "ERROR" not in output:
					log.info("The command Executed successfully ")			
					log.info("ExitCode:0")
					log.info("ExitDesc:The REVOKE privilege successful")
					print "ExitCode:0"
					print "ExitDesc:The REVOKE privilege successful"
					Status="REVOKE privileges successful"
				else:
					log.info("ExitCode:1")
					log.info("ExitDesc:REVOKE privilege failed check logs")
					print "ExitCode:1"
					print "ExitDesc: REVOKE	privileges Failed"
					Status="REVOKE privilege failed check logs"	
			else:
				log.info("ExitCode:10")
				log.info("ExitDesc:Enter the GRANT/REVOKE for the Privilege_Type")
				print "ExitCode:10"
				print "ExitDesc:Enter the GRANT/REVOKE for the Privilege_Type"	
				Status="Error occured check log file"
		else:
			log.info("ExitCode:10")
			log.info("ExitDesc:Enter proper Execution_Location")
			print "ExitCode:10"
			print "ExitDesc:Enter proper Execution_Location"
			Status="ERROR Occured check log file"

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

SUBJECT = ' Alter privileges  '
body ="""
<html>
<H2> Alter privileges %s </H2>
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
	
