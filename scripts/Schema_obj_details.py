"""
	Name: Schema_obj_details.py
	Description: To check Schema object details, remote target server or local target server
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


if len(sys.argv) == 6:
	Execution_Location=sys.argv[1]
	Execution_Location=Execution_Location.upper()
	HostName = sys.argv[2] 
	OSUser = sys.argv[3] 
	OSPassword = sys.argv[4]
	Sid=sys.argv[5]
	tableHtml1=""
	tableHtml2=""
	Status=""


		################################### Creating Log File ###############################
	try:
		if os.name == 'nt':
			logdir = os.getcwd()+"\\logs"
		if os.name == 'posix':
			logdir = os.getcwd()+"/logs"
		
		logfile = "SCHEMA_OBJECT_DETAILS.log"
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

			#loginline="sqlplus -s / as sysdba"
			#loginline=". ~/.bash_profile\nsqlplus -s / as sysdba"
			#loginline="echo %s | . oraenv\nsqlplus -s / as sysdba"%Sid
			loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid

			command1="select status , count(*) from dba_objects where OWNER NOT IN ('SYS','SYSTEM') and status='INVALID' group by status;"
			ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command1)
			#print ucommand
			stdin, stdout, stderr = dssh.exec_command(ucommand)
			log.info('The command is %s'%(ucommand))
			output = stdout.read()
			log.info("The output is %s "%(output))
			print "STATUS 	COUNT(*)"
			print output
			error=stderr.read()
			log.info("The error if any is %s "%error)
			if output:
				output=output.strip(' \t\n\r')
				if "error" not in output and "ORA-" not in output:
					allLines1=""
					tablestrt="	<table><tr><th> Status </th><th> COUNT(*) </th></tr>"
					outx=output.splitlines()	
					for i in outx:
						i=i.split()
						i0=str(i[0])
						i1=str(i[1])
						beginning="<tr style='background-color:white;'>"
						bodyE3 ="<td style='text-align:center;'> " + i0 + " </td>"
						bodyE3+="<td style='text-align:center;'> " + i1 + "</td>"
						end="</tr>"
						allLines1+=beginning+bodyE3+end
					tableBody=allLines1
					tableEnd="</table>"
					tableHtml1=tablestrt+tableBody+tableEnd
					log.info("The html part is  of the 1st command is %s"%(tableHtml1))
					Status = "Successfully Executed"
				else:
					Status = "Failed"
					log.info("ExitDesc:Error occured while executing the command check the logs")
					
			else:
				Status = "Success, No INVALID SCHEMA objects  found check log file for command"
				log.info("ExitDesc:No INVALID SCHEMA objects  found check log file for command")
			command2="""set lines 900
			set pages 2000
			col OWNER for a15;
			col OBJECT_NAME for a30;
			select OWNER,OBJECT_NAME,OBJECT_ID,CREATED,STATUS,OBJECT_TYPE from dba_objects where OWNER NOT IN ('SYS','SYSTEM') and status='INVALID';"""
			ucommand1 = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command2)
			#print ucommand
			stdin, stdout, stderr = dssh.exec_command(ucommand1)
			log.info('The command is %s'%(ucommand1))
			output2 = stdout.read()
			error=stderr.read()
                        log.info("The error if any is %s "%error)
			log.info("The output is %s "%output2)
			if output2:
				output2 = output2.strip(' \t\n\r')
				if "error" not in output2 and "ORA-" not in output2:
					allLines2=""
					tablestrt="	<table><tr><th> OWNER </th><th> OBJECT_NAME </th><th> OBJECT_ID </th><th> OBJECT_TYPE </th><th> CREATED </th><th> STATUS </th></tr>"
					outx=output2.splitlines()
					for i in outx:
						i=i.split()
						i0=str(i[0])
						i1=str(i[1])
						i2=str(i[2])
						i3=str(i[3])
						i4=str(i[4])
						
						if len(i)== 7:
							i5=str(i[5])+" "+str(i[6])
						if len(i) == 8:
							i5=str(i[5])+" "+str(i[6])+" "+str(i[7])
						if len(i) == 9:
							i5=str(i[5])+" "+str(i[6])+" "+str(i[7])+" "+str(i[8])
						else:
							i5=str(i[5])
						beginning="<tr style='background-color:white;'>"
						bodyE3 ="<td style='text-align:center;'> " + i0 + " </td>"
						bodyE3+="<td style='text-align:center;'> " + i1 + " </td>"
						bodyE3+="<td style='text-align:center;'> " + i2 + " </td>"
						bodyE3+="<td style='text-align:center;'> " + i5 + " </td>"
						bodyE3+="<td style='text-align:center;'> " + i3 + " </td>"
						bodyE3+="<td style='text-align:center;'> " + i4 + " </td>"
						end="</tr>"
						allLines2+=beginning+bodyE3+end
					tableBody=allLines2
					tableEnd="</table>"
					tableHtml2=tablestrt+tableBody+tableEnd
					log.info("The html part is  of the 1st command is %s"%(tableHtml2))
					Status = "Successfully Executed"
				else:
					Status = "Failed"
					log.info("ExitCode:10")
					log.info("ExitDesc:Error occured while executing the command check the logs")
					print "ExitCode:10"
					print "ExitDesc:Error occured while executing the command check the logs"
			else:
				Status = "Success , No INVALID SCHEMA objects  found check log file for command"
				log.info("ExitCode:0")
				log.info("ExitDesc:No INVALID SCHEMA objects  found check log file for command")
				print "ExitCode:0"
				print "ExitDesc:No INVALID SCHEMA objects  found check log file for command"						

		elif Execution_Location=="LOCAL":

			#loginline="sqlplus -s / as sysdba"
			#loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv\nsqlplus -s / as sysdba"%Sid
			#loginline=". ~/.bash_profile\nsqlplus -s / as sysdba"
			loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid
			
			command1="select status , count(*) from dba_objects where OWNER NOT IN ('SYS','SYSTEM') and status='INVALID' group by status;"
			ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command1)
			#print ucommand
			output=os.popen(ucommand).read()
			log.info('The command is %s'%(ucommand))
			output = stdout.read()
			log.info("The output is %s "%(output))
			print "STATUS 	COUNT(*)"
			print output
				
			if output:
				output=output.strip(' \t\n\r')
				if "error" not in output and "ORA-" not in output:
					allLines1=""
					tablestrt="	<table><tr><th> Status </th><th> COUNT(*) </th></tr>"
					outx=output.splitlines()	
					for i in outx:
						i=i.split()
						i0=str(i[0])
						i1=str(i[1])
						beginning="<tr style='background-color:white;'>"
						bodyE3 ="<td style='text-align:center;'> " + i0 + " </td>"
						bodyE3+="<td style='text-align:center;'> " + i1 + "</td>"
						end="</tr>"
						allLines1+=beginning+bodyE3+end
					tableBody=allLines1
					tableEnd="</table>"
					tableHtml1=tablestrt+tableBody+tableEnd
					log.info("The html part is  of the 1st command is %s"%(tableHtml1))
					Status = "Successfully Executed"
				else:
					Status = "Failed"
					log.info("ExitDesc:Error occured while executing the command check the logs")
						
			else:
				Status = "Success, No INVALID SCHEMA objects  found check log file for command"
				log.info("ExitDesc:No INVALID SCHEMA objects  found check log file for command")
			command2="""set lines 900
			set pages 2000
			col OWNER for a20;
			col OBJECT_NAME for a35;
			select OWNER,OBJECT_NAME,OBJECT_ID,CREATED,STATUS,OBJECT_TYPE from dba_objects where OWNER NOT IN ('SYS','SYSTEM') and status='INVALID';"""

			ucommand1 = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command2)
			#print ucommand
			output2=os.popen(ucommand1).read()
			log.info('The command is %s'%(ucommand1))
			output2 = stdout.read()
			log.info("The output is %s"%output2)
			if output2:
				output2 = output2.strip(' \t\n\r')
				if "error" not in output2 and "ORA-" not in output2:
					allLines2=""
					tablestrt="	<table><tr><th> OWNER </th><th> OBJECT_NAME </th><th> OBJECT_ID </th><th> OBJECT_TYPE </th><th> CREATED </th><th> STATUS </th></tr>"
					outx=output2.splitlines()
					for i in outx:
						i=i.split()
						i0=str(i[0])
						i1=str(i[1])
						i2=str(i[2])
						i3=str(i[3])
						i4=str(i[4])
						
						if len(i)== 7:
                                                        i5=str(i[5])+" "+str(i[6])
                                                if len(i) == 8:
                                                        i5=str(i[5])+" "+str(i[6])+" "+str(i[7])
                                                if len(i) == 9:
                                                        i5=str(i[5])+" "+str(i[6])+" "+str(i[7])+" "+str(i[8])
                                                else:
                                                        i5=str(i[5])




						beginning="<tr style='background-color:white;'>"
						bodyE3 ="<td style='text-align:center;'> " + i0 + " </td>"
						bodyE3+="<td style='text-align:center;'> " + i1 + " </td>"
						bodyE3+="<td style='text-align:center;'> " + i2 + " </td>"
						bodyE3+="<td style='text-align:center;'> " + i5 + " </td>"
						bodyE3+="<td style='text-align:center;'> " + i3 + " </td>"
						bodyE3+="<td style='text-align:center;'> " + i4+ " </td>"
						end="</tr>"
						allLines2+=beginning+bodyE3+end
					tableBody=allLines2
					tableEnd="</table>"
					tableHtml2=tablestrt+tableBody+tableEnd
					log.info("The html part is  of the 1st command is %s"%(tableHtml2))
					Status = "Successfully Executed"
				else:
					Status = "Failed"
					log.info("ExitCode:10")
					log.info("ExitDesc:Error occured while executing the command check the logs")
					print "ExitCode:10"
					print "ExitDesc:Error occured while executing the command check the logs"
			else:
				Status = "Success , No INVALID SCHEMA objects  found check log file for command"
				log.info("ExitCode:0")
				log.info("ExitDesc:No INVALID SCHEMA objects  found check log file for command")
				print "ExitCode:0"
				print "ExitDesc:No INVALID SCHEMA objects  found check log file for command"						

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
	log.info("ExitCode: 10")
	log.info("ExitDesc: Missing Arguments")
	print "ExitCode: 10"
	print "ExitDesc: Missing Arguments"	

################################ Mailing  part ############################################

now = datetime.now()
dt = now.strftime("%A,%d-%B-%y")
dt=str(dt)
FROM  = '%s'%frommail
TO = '%s'%tomail

SUBJECT = ' SCHEMA OBJECT DETAILS '
body ="""
<html>
<H2> SCHEMA OBJECT DETAILS </H2>
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
%s
%s
</body>	
</html>"""%(HostName,Execution_Location,Sid,Status,tableHtml1,tableHtml2)


	
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

						
			

			
