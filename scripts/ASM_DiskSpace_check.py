"""
	Name: ASM_Archive_Spacecheck_Without_Sudo_Brakes.py
	Description: To generate ASM disk space report, remote target server or local target server
	Team: Software Service Automation
	Author: sai charan Tyarla(sai-charan.thyarla@capgemini.com)
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
	HostName = sys.argv[2] 
	OSUser = sys.argv[3] 
	OSPassword = sys.argv[4]
	Sid=sys.argv[5]
	Execution_Location = Execution_Location.upper()
	
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
		dssh = paramiko.SSHClient()
		dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		dssh.connect(HostName, username=OSUser, password=OSPassword)		
		loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid
		command1="""col name for a30
				  select name,total_mb,free_mb from v\$asm_diskgroup;"""
		ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF\nexit" %(loginline,command1)
		log.info('Executing Query: {0}'.format(command1))
		stdin, stdout, stderr = dssh.exec_command(ucommand)
		output1=stdout.read()
		allLines=""	
		log.info('The command is: %s'%ucommand)
		log.info('The output is: %s'%output1)
		er= stderr.read()
		if output1 and "ERROR" not in output1 and "ORA-" not in output1 and "sp-" not in output1:
			output1=output1.strip(' \t\n\r')
			tablestrt="	<table><tr><th> Name </th><th> Total MB </th><th> Free MB </th></tr>"
			outx=output1.splitlines()
			for i in outx:
				i=i.split()
				i0=str(i[0])
				i1=str(i[1])
				i2=str(i[2])
				beginning="<tr style='background-color:white;'>"
				bodyEl ="<td style='text-align:center;'> " + i0 + " </td>"
				bodyEl+="<td style='text-align:center;'> " + i1 + " </td>"
				bodyEl+="<td style='text-align:center;'> " + i2 + " </td>"
				end="</tr>"			
				allLines+=beginning+bodyEl+end
				tableBody=allLines
				tableEnd="</table>"
				tableHtml5=tablestrt+tableBody+tableEnd
		else:
			print "ExitCode: 1"
			print "ExitDesc: Error Occured:%s"%output
			Status="Some error Occured. Check logs"		
		command2="""set line 300 pages 1000
col diskgroup for a30
col diskname for a25
col path for a30
select a.name DiskGroup,b.name DiskName, b.total_mb, b.free_mb,b.path, b.header_status from v\$asm_disk b, v\$asm_diskgroup a where a.group_number (+) =b.group_number order by b.group_number,b.name;"""
		ucommand1 = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF\nexit" %(loginline,command2)
		log.info('Executing Query: {0}'.format(command2))
		stdin, stdout, stderr = dssh.exec_command(ucommand1)
		output2=stdout.read()
		allLines1=""
		log.info('The command is: %s'%ucommand)
		log.info('The output is: %s'%output2)
		er= stderr.read()
		print output2
		if output2 and "ERROR" not in output2 and "ORA-" not in output2 and "sp-" not in output2:
			output2=output2.strip(' \t\n\r')
			tablestrt="	<table><tr><th> DISKGROUP </th><th> DISKNAME </th><th> TOTAL_MB </th><th> FREE_MB </th><th> PATH </th><th> HEADER_STATUS </th></tr>"
			outx1=output2.splitlines()
			for i in outx1:
				i=i.split()
				
				if len(i)==6:
					i0=str(i[0])
					i1=str(i[1])
					i2=str(i[2])				
					i3=str(i[3])
					i4=str(i[4])
					i5=str(i[5])
				elif len(i)==4:
					i2=str(i[0])
					i3=str(i[1])
					i4=str(i[2])
					i5=str(i[3])
					i0=""
					i1=""
					
				

				beginning1="<tr style='background-color:white;'>"
				bodyE2 ="<td style='text-align:center;'> " + i0 + " </td>"
				bodyE2+="<td style='text-align:center;'> " + i1 + " </td>"
				bodyE2+="<td style='text-align:center;'> " + i2 + " </td>"
				bodyE2+="<td style='text-align:center;'> " + i3 + " </td>"
				bodyE2+="<td style='text-align:center;'> " + i4 + " </td>"
				bodyE2+="<td style='text-align:center;'> " + i5 + " </td>"				
				end="</tr>"
				
				allLines1+=beginning1+bodyE2+end
				tableBody1=allLines1
				tableEnd="</table>"
				tableHtml4=tablestrt+tableBody1+tableEnd
			print "ExiCode:0"
			print "ExitDesc: ASM Diskspace Report Successfully"
			log.info("ExitCode:0")
			log.info("ExitDesc:ASM Diskspace Report Successfully")
			Status="ASM Diskspace Report Successfully"
		else:
			print "ExitCode: 1"
			print "ExitDesc: Error Occured:%s"%output
			log.info("ExitCode: 1")
			log.info("ExitDesc: Error Occured:%s"%output)
			Status="Some error Occured. Check logs"
	except Exception, e:
		print "ExitCode: 10"
		print "ExitDesc: script failed due to: {0}".format(e)
		log.info('ExitCode: 10')
		log.info('ExitDesc: Error Occurred. Check Logs')
		Status="Error Occured"			
else:
	print "ExitCode:10"
	print "ExitDesc:Missing Arguments"
	
################################ Mail part ##################################

now = datetime.now()
dt = now.strftime("%A,%d-%B-%y")
dt=str(dt)
FROM  = '%s'%frommail
TO = '%s'%tomail 

SUBJECT = 'ASM_Archive Space Check '
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
<TH>  Archive space check  </TH>

</TR>
<TR>
<TD>  %s  </TD>
<TD>  %s  </TD>
<TD>  %s  </TD>
<TD>  %s  </TD>
<TD>  %s  </TD>

</TR> 
</TABLE>	

<TABLE>
<TR>
<TH>  Execution Type  </TH>
<TH>  Server Name  </TH>
<TH>  SID or Database name  </TH>
<TH>  Status  </TH>
<TH>  SPACE CHECK REPORT  </TH>

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
</HTML>""" %(dt,Execution_Location,HostName,Sid,Status,tableHtml5,Execution_Location,HostName,Sid,Status,tableHtml4)
	
	
part1="""From: %s 
To: %s 
Subject: %s
Content-Type: multipart/mixed;
""" %(frommail, tomail, SUBJECT)

part2 = """Content-Type: text/html
%s
""" %body


message = part1 + part2
log.info("The HTML part is ... %s"%message)

try:
	client = smtplib.SMTP(smtpserver)
	client.sendmail(FROM, TO, message)
	client.quit()
	print "Email sent"
	log.info('Email Sent')
	
except Exception, e:
	print "Email sending failed due to: {0}".format(e)
	log.info('Email sending failed due to: {0}'.format(e))

				
			
					
					
					
			
			
		

		

