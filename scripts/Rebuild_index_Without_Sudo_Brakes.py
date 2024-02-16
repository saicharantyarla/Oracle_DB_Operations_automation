"""
	Name: Rebuild_index_Without_Sudo_Brakes.py
	Description: Rebuilding the Index details, remote target server or local target server
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



if len(sys.argv) == 7:
	Execution_Location=sys.argv[1]
	Execution_Location=Execution_Location.upper()
	HostName = sys.argv[2] 
	OSUser = sys.argv[3] 
	OSPassword = sys.argv[4]
	Sid=sys.argv[5]
	Dbusername=sys.argv[6]
	Dbusername=Dbusername.upper()
	Dbusername=Dbusername.split(",")
	Status=""
	Ora_Home_Sid=""
	Final_users=""
	Final_users1=""
	Final_indexes=""
	Final_indexes1=""
	count=1
	################################### Creating Log File #####################################
	
	try:
		if os.name == 'nt':
			logdir = os.getcwd()+"\\logs"
		if os.name == 'posix':
			logdir = os.getcwd()+"/logs"
		
		logfile = "Rebuild_index_%s.log"%(HostName)
		log = Logger(logdir,logfile)

		log.info('*************************************************************************')

		log.info('Started Script Execution')
		
	except Exception, e:
		print "ExitCode: 10"
		print "ExitDesc: Unable to create Logfile {0}".format(logfile)

	################################### END OF LOG FILE CREARION ######################################
	try:

		############################ For Remote execution ##########################
	
		if Execution_Location=="REMOTE":
			
			dssh = paramiko.SSHClient()
			dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			dssh.connect(HostName, username=OSUser, password=OSPassword)

			#loginline=". ~/.bash_profile\nsqlplus -s / as sysdba"
			#loginline="sqlplus -s / as sysdba"
			loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid
			log.info("The users are %s"%Dbusername)
			for user in Dbusername:
				query="select username from dba_users where username='%s';"%user
				ccommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,query)
				stdin, stdout, stderr = dssh.exec_command(ccommand)
				log.info('The command is %s'%(ccommand))
				user_val = stdout.read()
				log.info("The output is %s "%(user_val))
				error=stderr.read()
				log.info("The error if any is...%s "%error)
				#print user_val
				#print user
				if user in user_val:
					Final_users=Final_users+","+user
					log.info("The user %s is valid user and Fetching the Index details Associated to that user"%user)
					query1="select index_name from dba_indexes where owner='%s';"%user
					dcommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,query1)
					stdin, stdout, stderr = dssh.exec_command(dcommand)
					log.info('The command is %s'%(dcommand))
					output1 = stdout.read()
					log.info("The output is %s "%output1)
					if output1 and "ERROR" not in output1 and "ORA-" not in output1 and "sp-" not in output1:							
						log.info("The indexes associated to %s are %s "%(user,output1))	
						output1=output1.strip()
						output1 = output1.strip(' \t\n\r')
						output1=output1.splitlines()
						for index in output1:
							command="Alter index %s.%s rebuild online;"%(user,index)
							ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command)
							#print command
							stdin, stdout, stderr = dssh.exec_command(ucommand)
							
							log.info('The command is %s'%(ucommand))
							output = stdout.read()
							#print output
							log.info("The output is %s"%output)
							if "ERROR" not in output and "ORA-" not in output and "sp-" not in output:
								command1="Alter index %s.%s rebuild online parallel 4;"%(user,index)
								ucommand1 = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command1)
								#print command1
								
								stdin, stdout, stderr = dssh.exec_command(ucommand1)
								log.info('The command is %s'%(ucommand1))
								Final_op = stdout.read()
								log.info("The output is %s "%(Final_op))
								#print output1
								
								if "ERROR" not in Final_op and "ORA-" not in Final_op and "sp-" not in Final_op:
									Final_indexes=Final_indexes+","+index
									count=0
									
								else:
									Final_indexes1=Final_indexes1+","+index
							else:
								Final_indexes1=Final_indexes1+","+index
								#log.info("The command %s is failed and output is %s  "%(command,output1))
						log.info("The Rebuild index was successful for the user %s and the indexes are %s"%(user,Final_indexes[1:]))
						log.info("The rebuild index was failed for the user %s and the indexnames are %s"%(user,Final_indexes1[1:]))

					else:
						log.info("The Error occured while Executing the command %s "%query1)
				else:
					Final_users1=Final_users1+","+user
			if Final_users1:
				log.info("The user %s doesnot Exist Please check it."%Final_users1[1:])
			log.info("The user %s Exist"%Final_users[1:])
			if count==0:
				status ="Rebuilding index is successful"
				log.info("ExitCode:0")
				log.info("ExitDesc:Rebuilding index is successfull")
				print "ExitCode:0"
				print "ExitDesc:Rebuilding index is successfull"
				
			else:
				Status = "Rebuilding Index Failed"
				log.info("ExitCode:10")
				log.info("ExitDesc:Error occured while executing the command check the logs")
				print "ExitCode:10"
				print "ExitDesc:Error occured while executing the command check the logs"
					
				
					
		
		elif Execution_Location=="LOCAL":
			
			#loginline=". ~/.bash_profile\nsqlplus -s / as sysdba"	
			#loginline="sqlplus -s / as sysdba"
			loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid

			########################################### Actual Commands of the Script ##########################################
		
			log.info("The users are %s"%Dbusername)
			for user in Dbusername:
				query="select username from dba_users where username='%s';"%user
				ccommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,query)
				log.info('The command is %s'%(ccommand))
				user_val=os.popen(ccommand).read()
				log.info("The output is %s "%(user_val))
				if user_val in user:
					log.info("The user %s is valid user and Fetching the Index details Associated to that user"%user)
					query1="select index_name from dba_indexes where owner='%s';"%user
					dcommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,query1)
					output1=os.popen(dcommand)
					log.info('The command is %s'%(dcommand))
					log.info("The output is %s "%output1)
					if output1 and "ERROR" not in output1 and "ORA-" not in output1 and "sp-" not in output1:							
						log.info("The indexes associated to %s are %s "%(user,output1))	
						output1=output1.strip()
						output1 = output1.strip(' \t\n\r')
						output1=output1.splitlines()
						for index in output1:
							command="Alter index %s.%s rebuild online;"%(user,index)
							ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command)
							#print ucommand
							output = os.popen(ucommand).read()
							log.info('The command is %s'%(ucommand))
							
							print output
							log.info("The output is %s"%output)
							if "ERROR" not in output and "ORA-" not in output and "sp-" not in output:
								command1="Alter index %s.%s rebuild online parallel 4;"%(user,index)
								ucommand1 = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command1)
								#print ucommand
								Final_op = os.popen(ucommand1).read()	
								log.info('The command is %s'%(ucommand1))
								
								log.info("The output is %s "%(Final_op))
								#print output1
								
								if "ERROR" not in Final_op and "ORA-" not in Final_op and "sp-" not in Final_op:
									Final_indexes=Final_indexes+user
									count=0
									
								else:
									Final_indexes1=Final_indexes1+user
							log.info("The Rebuild index was successfull for the user %s and the indexes are %s"%(user,Final_indexes))
							log.info("The rebuild index was failed for the user %s and the indexnames are %s"%(user,Final_indexes1))
						else:
							log.info("The command %s is failed ")
					else:
						log.info("The Error occured while Executing the command %s "%query1)
				else:
					log.info("The user %s doesnot Exists Please check it."%user)
			if count==0:
				status ="Rebuilding index is successfull"
				log.info("ExitCode:0")
				log.info("ExitDesc:Rebuilding index is successfull")
				print "ExitCode:0"
				print "ExitDesc:Rebuilding index is successfull"
				
			else:
				Status = "Rebuilding Index Failed"
				log.info("ExitCode:10")
				log.info("ExitDesc:Error occured while executing the command check the logs")
				print "ExitCode:10"
				print "ExitDesc:Error occured while executing the command check the logs"
		else:
			print "ExitCode:10"
			print "ExitDesc:Enter proper Execution_Location input"
			log.info("ExitCode:10")
			log.info("ExitDesc:Enter proper Execution_Location input")
			Status="Enter proper Execution_Location input"
					
	except Exception, e:
		print "ExitCode: 10"
		print "ExitDesc: script failed due to: {0}".format(e)
		log.info("ExitCode: 10")
		log.info("ExitDesc: script failed due to: {0}".format(e))
		Status="Error Occured while Executing Command"
	
else:
	
	print "ExitCode: 10"
	print "ExitDesc: Missing Arguments"	

################################ Mailing  part ############################################

now = datetime.now()
dt = now.strftime("%A,%d-%B-%y")
dt=str(dt)
FROM  = '%s'%frommail
TO = '%s'%tomail

SUBJECT = ' Rebuilding Indexs  '
body ="""
<html>
<H2> Rebuilding Indexs </H2>
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
</html>"""%(HostName,Execution_Location,Sid,Status)


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
