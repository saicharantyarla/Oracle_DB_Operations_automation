"""
	Name: DataGuard_Status_Without_Sudo_v1.py
	Description: To check Dataguard status, remote target server or local target server
	Team: Software Service Automation
	Author: Arnab Roy(arnab.d.roy@capgemini.com)
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
	tableHtml5=""
	tableHtml4=""
	tableHtml3=""

		################################### Creating Log File ###############################
	try:
		if os.name == 'nt':
			logdir = os.getcwd()+"\\logs"
		if os.name == 'posix':
			logdir = os.getcwd()+"/logs"
		
		logfile = "Data_status_%s.log"%(HostName)
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
			#loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid
			loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid
			command1="""SELECT ARCH.THREAD# "Thread", ARCH.SEQUENCE# "Last Sequence Received", APPL.SEQUENCE# "Last Sequence Applied", (ARCH.SEQUENCE# - APPL.SEQUENCE#) "Difference"
			FROM
			(SELECT THREAD# ,SEQUENCE# FROM V\$ARCHIVED_LOG WHERE (THREAD#,FIRST_TIME ) IN (SELECT THREAD#,MAX(FIRST_TIME) FROM V\$ARCHIVED_LOG GROUP BY THREAD#)) ARCH,
			(SELECT THREAD# ,SEQUENCE# FROM V\$LOG_HISTORY WHERE (THREAD#,FIRST_TIME ) IN (SELECT THREAD#,MAX(FIRST_TIME) FROM V\$LOG_HISTORY GROUP BY THREAD#)) APPL
			WHERE ARCH.THREAD# = APPL.THREAD#;""" 
			
			ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command1)
			#print ucommand
			stdin, stdout, stderr = dssh.exec_command(ucommand)
			log.info('The command is %s'%(ucommand))
			output = stdout.read()
			error=stderr.read()
			log.info("The error if any is %s "%error)
			
			log.info('the output is %s'%(output))
			print "  THREAD	LAST SEQUENCE RECEIVED  LAST SEQURNCE APPLIED  DIFFERENCE   "
			print output
			if output:
				output=output.strip(' \t\n\r')
				
				if "ERROR" not in output:
					allLines=""
					#tableHtml5=""
					header=" <h3>ARCHIVED LOG and LOG history </h3>"
					tablestrt="	<table><tr><th> Thread </th><th> Last Sequence Received </th><th> Last Sequence Applied </th><th>  Difference </th></tr>"
					outx=output.splitlines()

					for i in outx:
						i=i.split()
						i0=str(i[0])
						i1=str(i[1])
						i2=str(i[2])
						i3=str(i[3])

						beginning="<tr style='background-color:white;'>"
						bodyEl ="<td style='text-align:center;'> " + i0 + " </td>"
						bodyEl+="<td style='text-align:center;'> " + i1 + " </td>"
						bodyEl+="<td style='text-align:center;'> " + i2 + " </td>"
						bodyEl+="<td style='text-align:center;'> " + i3 + " </td>"
						end="</tr>"
						allLines+=beginning+bodyEl+end
					tableBody=allLines
					tableEnd="</table>"
					tableHtml5=header+tablestrt+tableBody+tableEnd 
					log.info("The html part is  of the 1st command is %s"%(tableHtml5))
				else:
					print "ExitCode: 1"
					print "ExitDesc: Error Occured:%s"%output
					Status="Some error Occured. Check logs"
			else:
				Status="No view Present"
				print "ExitCode: 1"
				print "ExitDesc: No view Present "

			command2='select round((sysdate-max(first_time))*24,2) "Hours Behind" from V\$log_history;'
			ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command2)
			#print ucommand
			log.info('The command is %s'%(ucommand))
			stdin, stdout, stderr = dssh.exec_command(ucommand)
			output1 = stdout.read()
			error=stderr.read()
                        log.info("The error if any is %s "%error)
			log.info("the output is %s "%(output1))
			print "	HOURS BEHIND	"
			print output1
			output1=output1.strip(' \t\n\r')
			tableHtml4 =""
			if output1:
				if "ERROR" not in output1:
					allLines1=""
					#tableHtml4=""
					header=" <h3>LOG history </h3>"
					tablestrt="	<table><tr><th> HOURS_Behind </th></tr>"
					outx=output1.splitlines()

					for i in outx:
						i=i.split()
						i0=str(i[0])
						beginning="<tr style='background-color:white;'>"
						bodyE2 ="<td style='text-align:center;'> " + i0 + " </td>"
						end="</tr>"
						allLines1+=beginning+bodyE2+end
					tableBody=allLines1
					tableEnd="</table>"
					tableHtml4=header+tablestrt+tableBody+tableEnd
					log.info("The html part is  of the 1st command is %s"%(tableHtml4))
				else:
					print "ExitCode: 1"
					print "ExitDesc: Error Occured:%s"%output
					Status="Some error Occured. Check logs"	
			else:
				Status="No view Present"
				print "ExitCode: 1"
				print "ExitDesc: No view Present "
			command3="""set lines 900
			set pages 1000
			col status for a20
			select process, status, thread#, sequence#, block#, blocks from V\$managed_standby;"""
			ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command3)
			#print ucommand
			log.info('The command is %s'%(ucommand))
			stdin, stdout, stderr = dssh.exec_command(ucommand)
			output2 = stdout.read()
			log.info('The output is %s '%(output2))
			error=stderr.read()
			log.info("The error if any is %s"%error)
			print "  THREAD     SEQUENCE     BLOCK  "
			print output2
			tableHtml3=""
			if output2:
				output2=output2.strip(' \t\n\r')
				if "ERROR" not in output2:
					allLines2=""
					
					header=" <h3>LOG Managed Stand BY </h3>"
					tablestrt="	<table><tr><th> process </th><th> status </th><th> thread# </th><th> sequence# </th><th> block </th><th> blocks </th></tr>"
					outx=output2.splitlines()
					
						
					for i in outx:
						
						i=i.split()
						i0=str(i[0])
						i1=str(i[1])
						i2=str(i[2])
						i3=str(i[3])
						i4=str(i[4])
						i5=str(i[5])

						beginning="<tr style='background-color:white;'>"
						bodyE3 ="<td style='text-align:center;'> " + i0 + " </td>"
						bodyE3+="<td style='text-align:center;'> " + i1 + " </td>"
						bodyE3+="<td style='text-align:center;'> " + i2 + " </td>"
						bodyE3+="<td style='text-align:center;'> " + i3 + " </td>"
						bodyE3+="<td style='text-align:center;'> " + i4 + " </td>"
						bodyE3+="<td style='text-align:center;'> " + i5 + " </td>"
						
						end="</tr>"
						allLines2+=beginning+bodyE3+end
					tableBody=allLines2
					tableEnd="</table>"
					tableHtml3=header+tablestrt+tableBody+tableEnd
					log.info("The html part is  of the 1st command is %s"%(tableHtml3))
					log.info('ExitCode: 0')
					log.info("ExitDesc: DATAGUARD STATUS DETAILS FETCHED SUCCESSFULLY")
					print "ExitCode: 0"
					print "ExitDesc: DATAGUARD STATUS DETAILS FETCHED SUCCESSFULLY"				
					Status="Successfully Fetched Details"
				
				else:
					print "ExitCode: 1"
					print "ExitDesc: Error Occured:%s"%output
					Status="Some error Occured. Check logs"
			else:
				log.info('No rows affected')
				Status="Successful Execution. \n No output for %s" %command3
					
		############################ For Local execution ##########################
		
		
		elif Execution_Location == "LOCAL":
			#loginline=". ~/.bash_profile\nsqlplus -s / as sysdba"		
			#loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid
			loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid
			command1="""SELECT ARCH.THREAD# "Thread", ARCH.SEQUENCE# "Last Sequence Received", APPL.SEQUENCE# "Last Sequence Applied", (ARCH.SEQUENCE# - APPL.SEQUENCE#) "Difference"
			FROM
			(SELECT THREAD# ,SEQUENCE# FROM V\$ARCHIVED_LOG WHERE (THREAD#,FIRST_TIME ) IN (SELECT THREAD#,MAX(FIRST_TIME) FROM V\$ARCHIVED_LOG GROUP BY THREAD#)) ARCH,
			(SELECT THREAD# ,SEQUENCE# FROM V\$LOG_HISTORY WHERE (THREAD#,FIRST_TIME ) IN (SELECT THREAD#,MAX(FIRST_TIME) FROM V\$LOG_HISTORY GROUP BY THREAD#)) APPL
			WHERE ARCH.THREAD# = APPL.THREAD#;""" 
			
			ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command1)
			#print ucommand
			output=os.popen(ucommand).read()
			log.info('The command is %s'%(ucommand))
			tableHtml5=""
			
			log.info('the output is %s'%(output))
			print "  THREAD	LAST SEQUENCE RECEIVED  LAST SEQURNCE APPLIED  DIFFERENCE   "
			print output
			if output:
				output=output.strip(' \t\n\r')
				
				if "ERROR" not in output:
					allLines=""
					#tableHtml5=""
					header=" <h3>ARCHIVED LOG and LOG history </h3>"
					tablestrt="	<table><tr><th> Thread </th><th> Last Sequence Received </th><th> Last Sequence Applied </th><th>  Difference </th></tr>"
					outx=output.splitlines()

					for i in outx:
						i=i.split()
						i0=str(i[0])
						i1=str(i[1])
						i2=str(i[2])
						i3=str(i[3])

						beginning="<tr style='background-color:white;'>"
						bodyEl ="<td style='text-align:center;'> " + i0 + " </td>"
						bodyEl+="<td style='text-align:center;'> " + i1 + " </td>"
						bodyEl+="<td style='text-align:center;'> " + i2 + " </td>"
						bodyEl+="<td style='text-align:center;'> " + i3 + " </td>"
						end="</tr>"
						allLines+=beginning+bodyEl+end
					tableBody=allLines
					tableEnd="</table>"
					tableHtml5=header+tablestrt+tableBody+tableEnd 
					log.info("The html part is  of the 1st command is %s"%(tableHtml5))
				else:
					print "ExitCode: 1"
					print "ExitDesc: Error Occured:%s"%output
					Status="Some error Occured. Check logs"
			else:
				Status="No view Present"
				print "ExitCode: 1"
				print "ExitDesc: No view Present "

			command2='select round((sysdate-max(first_time))*24,2) "Hours Behind" from V\$log_history;'
			ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command2)
			#print ucommand
			log.info('The command is %s'%(ucommand))
			output1=os.popen(ucommand).read()
			log.info("the output is %s "%(output1))
			print "	HOURS BEHIND	"
			print output1
			output1=output1.strip(' \t\n\r')
			tableHtml4 =""
			if output1:
				if "ERROR" not in output1:
					allLines1=""
					#tableHtml4=""
					header=" <h3>LOG history </h3>"
					tablestrt="	<table><tr><th> HOURS_Behind </th></tr>"
					outx=output1.splitlines()

					for i in outx:
						i=i.split()
						i0=str(i[0])
						beginning="<tr style='background-color:white;'>"
						bodyE2 ="<td style='text-align:center;'> " + i0 + " </td>"
						end="</tr>"
						allLines1+=beginning+bodyE2+end
					tableBody=allLines1
					tableEnd="</table>"
					tableHtml4=header+tablestrt+tableBody+tableEnd
					log.info("The html part is  of the 1st command is %s"%(tableHtml4))
				else:
					print "ExitCode: 1"
					print "ExitDesc: Error Occured:%s"%output
					Status="Some error Occured. Check logs"	
			else:
				Status="No view Present"
				print "ExitCode: 1"
				print "ExitDesc: No view Present "
			command3="""set lines 900
                        set pages 1000
                        col status for a20
                        select process, status, thread#, sequence#, block#, blocks from V\$managed_standby;"""
			ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command3)

			#print ucommand
			log.info('The command is %s'%(ucommand))
			output2=os.popen(ucommand).read()
			log.info('The output is %s '%(output2))
			print "  THREAD     SEQUENCE     BLOCK  "
			print output2
			tableHtml3=""
			if output2:
				output2=output2.strip(' \t\n\r')
				if "ERROR" not in output2:
					allLines2=""
					
					header=" <h3>LOG Managed Stand BY </h3>"
					tablestrt="	<table><tr><th> process </th><th> status </th><th> thread# </th><th> sequence# </th><th> block </th><th> blocks </th></tr>"
					outx=output2.splitlines()
					
						
					for i in outx:
						
						i=i.split()
						i0=str(i[0])
						i1=str(i[1])
						i2=str(i[2])
						i3=str(i[3])
						i4=str(i[4])
						i5=str(i[5])

						beginning="<tr style='background-color:white;'>"
						bodyE3 ="<td style='text-align:center;'> " + i0 + " </td>"
						bodyE3+="<td style='text-align:center;'> " + i1 + " </td>"
						bodyE3+="<td style='text-align:center;'> " + i2 + " </td>"
						bodyE3+="<td style='text-align:center;'> " + i3 + " </td>"
						bodyE3+="<td style='text-align:center;'> " + i4 + " </td>"
						bodyE3+="<td style='text-align:center;'> " + i5 + " </td>"
						
						end="</tr>"
						allLines2+=beginning+bodyE3+end
					tableBody=allLines2
					tableEnd="</table>"
					tableHtml3=header+tablestrt+tableBody+tableEnd
					log.info("The html part is  of the 1st command is %s"%(tableHtml3))
					log.info('ExitCode: 0')
					log.info("ExitDesc: DATAGUARD STATUS DETAILS FETCHED SUCCESSFULLY")
					print "ExitCode: 0"
					print "ExitDesc: DATAGUARD STATUS DETAILS FETCHED SUCCESSFULLY"				
					Status="Successfully Fetched Details"
				
				else:
					print "ExitCode: 1"
					print "ExitDesc: Error Occured:%s"%output
					Status="Some error Occured. Check logs"
			else:
				log.info('No rows affected')
				Status="Successful Execution. \n No output for %s" %command3
				
		else:
			print "ExitCode:10"
			print "ExitDesc:Enter proper Execution_Location input"
			log.info("ExitCode:10")
			log.info("ExitDesc:Enter proper Execution_Location input")
					
	except Exception, e:
		print "ExitCode: 10"
		print "ExitDesc: script failed due to: {0}".format(e)
		Status="Error Occured while Executing Command"
	
else:
	print "ExitCode: 10"
	print "ExitDesc: Missing Arguments"	
################################ Mail part ##################################

now = datetime.now()
dt = now.strftime("%A,%d-%B-%y")
dt=str(dt)
FROM  = '%s'%frommail
TO = '%s'%tomail

SUBJECT = ' DATAGUARD STATUS PROCESS '
body ="""
<html>
<H2> DataGuard Status </H2>
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
<BODY>
<table>
<tr><th>HostName </th> <th>Execution Location </th> <th> SID </th><th> Status</th>  </tr>
<tr> <td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>
</table>
%s
%s
%s
</BODY>
</HTML>""" %(HostName,Execution_Location,Sid,Status,tableHtml5,tableHtml4,tableHtml3)
	# Prepare actual message
	
part1="""From: %s
To: %s
Subject: %s
Content-Type: multipart/mixed;
""" %(frommail, tomail,SUBJECT)

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
	print "Email sent"
	
except Exception, e:
	print "Email sending failed due to: {0}".format(e)

