"""
	Name: ASM_Disk_Space_Test_Without_Sudo_Brakes.py
	Description: To generate ASM disk space report, remote target server or local target server
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




################################### Creating Log File ###############################
try:
	if os.name == 'nt':
		logdir = os.getcwd()+"\\logs"
	if os.name == 'posix':
		logdir = os.getcwd()+"/logs"
	
	logfile = "ASM_Disk_Space_Report.log"
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
		tableHtml5=""
		Execution_Location = Execution_Location.upper()

		############################ For Remote execution ##########################
	
		if Execution_Location=="REMOTE":
			
			dssh = paramiko.SSHClient()
			dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			dssh.connect(HostName, username=OSUser, password=OSPassword)

			#loginline=". ~/.bash_profile\nsqlplus -s / as sysdba"
			#loginline="sqlplus -s / as sysdba"
			loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid			
			command1="""col NAME for a35 
			select name,decode(type,'NORMAL',2,'HIGH',3,'EXTERN',1) Redundancy, (total_mb/decode(type,'NORMAL',2,'HIGH',3,'EXTERN',1)) Total_MB,(free_mb/decode(type,'NORMAL',2,'HIGH',3,'EXTERN',1)) Free_MB,((free_mb/decode(type,'NORMAL',2,'HIGH',3,'EXTERN',1))/(total_mb/decode(type,'NORMAL',2,'HIGH',3,'EXTERN',1)))*100 "%Free" from v\$asm_diskgroup;"""
			ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command1)
			stdin, stdout, stderr = dssh.exec_command(ucommand)
			output=stdout.read()
			log.info('The command is %s'%(ucommand))
			log.info('the output is %s'%(output))
			error=stderr.read()
			log.info("The error if any is %s"%error)

			if output:
				output=output.strip(' \t\n\r')

				if "ERROR" not in output:
				
					print "NAME				REDUNDANCY	  TOTAL_MB    FREE_MB	%FREE"
					print output
					
					allLines=""
					tableHtml5=""
					tablestrt="	<table><tr><th> Name </th><th> Redundancy </th><th> Total_MB </th><th> Free_MB </th><th> %Free </th></tr>"
					outx=output.splitlines()
					print outx
					for i in outx:
						i=i.split()
						i0=str(i[0])
						i1=str(i[1])
						i2=str(i[2])
						i3=str(i[3])
						i4=str(i[4])

						beginning="<tr style='background-color:white;'>"
						bodyEl ="<td style='text-align:center;'> " + i0 + " </td>"
						bodyEl+="<td style='text-align:center;'> " + i1 + " </td>"
						bodyEl+="<td style='text-align:center;'> " + i2 + " </td>"
						bodyEl+="<td style='text-align:center;'> " + i3 + " </td>"
						bodyEl+="<td style='text-align:center;'> " + i4 + " </td>"
						end="</tr>"
						allLines+=beginning+bodyEl+end
					tableBody=allLines
					tableEnd="</table>"
					tableHtml5=tablestrt+tableBody+tableEnd 

					log.info('ExitCode: 0')
					log.info("ExitDesc: ASM Disk Space Report generated")
					print "ExitCode: 0"
					print "ExitDesc: ASM Disk Space Report generated"
					Status="Successful Execution"
				else:
					print "ExitCode: 1"
					print "ExitDesc: Error Occured:%s"%output
					Status="Some error Occured. Check logs"
			
			else:
				Status="No view Present"
				print "ExitCode: 1"
				print "ExitDesc: No view Present "
				log.info("ExitCode: 1")
				log.info("ExitDesc: No view Present ")
			
		
		
		########################################################### For Local execution ########################################################################
		
		
		elif Execution_Location == "LOCAL":
			
			#loginline=". ~/.bash_profile\nsqlplus -s / as sysdba"
			#loginline="sqlplus -s / as sysdba"
			loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid		
					
			command="""col NAME for a35 
		select name,decode(type,'NORMAL',2,'HIGH',3,'EXTERN',1) Redundancy, (total_mb/decode(type,'NORMAL',2,'HIGH',3,'EXTERN',1)) Total_MB,(free_mb/decode(type,'NORMAL',2,'HIGH',3,'EXTERN',1)) Free_MB,((free_mb/decode(type,'NORMAL',2,'HIGH',3,'EXTERN',1))/(total_mb/decode(type,'NORMAL',2,'HIGH',3,'EXTERN',1)))*100 "%Free" from v\$asm_diskgroup;"""
			ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command)
			output = os.popen(ucommand).read()
			
			if output:
				if "ERROR" not in output:
					
					print "NAME				REDUNDANCY	  TOTAL_MB    FREE_MB	%FREE"
					print output
					output=output.strip(' \t\n\r')
					
					allLines=""
					tableHtml5=""
					tablestrt="	<table><tr><th> Name </th><th> Redundancy </th><th> Total_MB </th><th> Free_MB </th><th> %Free </th></tr>"
					outx=output.splitlines()

					for i in outx:
						i=i.split()
						i0=str(i[0])
						i1=str(i[1])
						i2=str(i[2])
						i3=str(i[3])
						i4=str(i[4])

						beginning="<tr style='background-color:white;'>"
						bodyEl ="<td style='text-align:center;'> " + i0 + " </td>"
						bodyEl+="<td style='text-align:center;'> " + i1 + " </td>"
						bodyEl+="<td style='text-align:center;'> " + i2 + " </td>"
						bodyEl+="<td style='text-align:center;'> " + i3 + " </td>"
						bodyEl+="<td style='text-align:center;'> " + i3 + " </td>"
						end="</tr>"
						allLines+=beginning+bodyEl+end
					tableBody=allLines
					tableEnd="</table>"
					tableHtml5=tablestrt+tableBody+tableEnd 
			

					log.info('ExitCode: 0')
					log.info("ExitDesc: ASM Disk Space Report generated")
					print "ExitCode: 0"
					print "ExitDesc: ASM Disk Space Report generated"
					Status="Successful Execution"
				else:
					print "ExitCode: 1"
					print "ExitDesc: Error Occured:%s"%output
					log.info('ExitCode: 1')
					log.info('ExitDesc: Error Occured:%s'%output)
					Status="Some error Occured. Check logs"
			
			else:
				log.info('No rows affected')
				print "No output found"
				Status="Successful Execution. \n No output for %s" %command
				
		else:
			print "ExitCode: 10"
			print "ExitDesc: Enter proper Execution_Location input"
			log.info("ExitCode:10")
			log.info("ExitDesc: Enter proper Execution_Location input")
			Status="Error Occurred."
			

	else:
		print "ExitCode: 10"
		print "ExitDesc: Missing Arguments"
		log.info('ExitCode:10')
		log.info('ExitDesc: Missing Arguments')
		Status="Error Occurred"
		
except Exception, e:
	print "ExitCode: 10"
	print "ExitDesc: script failed due to: {0}".format(e)
	log.info('ExitCode: 10')
	log.info('ExitDesc: Error Occurred. Check Logs')
	Status="Error Occured"
	
	
################################ Mail part ##################################

now = datetime.now()
dt = now.strftime("%A,%d-%B-%y")
dt=str(dt)
FROM  = '%s'%frommail
TO = '%s'%tomail 

SUBJECT = ' ASM DISK SPACE REPORT '
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
<TH>  Output  </TH>

</TR>
<TR>
<TD>  %s  </TD>
<TD>  %s  </TD>
<TD>  %s  </TD>
<TD>  %s  </TD>
<TD>  %s  </TD>

</TR> 
</TABLE>
</BODY>
</HTML>""" %(dt,Execution_Location,HostName,Sid,Status,tableHtml5)
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
