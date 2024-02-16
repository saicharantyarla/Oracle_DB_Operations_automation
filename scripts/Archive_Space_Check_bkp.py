"""
	Name: Archive_Space_Check_Test_Without_Sudo_Brakes.py
	Description: To perform Archive Space Checks, remote target server or local target server
	Team: Software Service Automation
	Author: Arnab Roy(arnab.d.roy@capgemini.com)
	Edited By:Saicharan Tyarla(sai-charan.thyarla@capgemini.com)
	Inputs: Arguments [Execution_Location,HostName,OSUser,OSPassword,SID], LogFileLoc
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
allLines=""
tableHtml5=""



if len(sys.argv) == 7:
	Execution_Location=sys.argv[1]
	HostName = sys.argv[2] 
	OSUser = sys.argv[3] 
	OSPassword = sys.argv[4]
	Sid=sys.argv[5]
	FRA_Used=sys.argv[6]	#Enter either True or False 
	FRA_Used=FRA_Used.upper()
	Execution_Location=Execution_Location.upper()
		
		################################### Creating Log File ###############################
	try:
		if os.name == 'nt':
			logdir = os.getcwd()+"\\logs"
		if os.name == 'posix':
			logdir = os.getcwd()+"/logs"
		
		logfile = "Archive_Space_Check_%s.log"%(HostName)
		log = Logger(logdir,logfile)

		log.info('*************************************************************************')

		log.info('Started Script Execution')
		
	except Exception, e:
		print "ExitCode: 10"
		print "ExitDesc: Unable to create Logfile {0}".format(logfile)
		
		################################### END OF LOG FILE CREARION ######################################
	

	############################ For Remote execution ##########################
	
	try:	
	
		if Execution_Location=="REMOTE":
			log.info("The User Selected Remote Execution")
			
			dssh = paramiko.SSHClient()
			dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			dssh.connect(HostName, username=OSUser, password=OSPassword)
			loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid
			#loginline=". ~/.bash_profile\nsqlplus -S / as sysdbA"
			#loginline="sqlplus -s / as sysdba"
			if FRA_Used=="TRUE":
			
				command1="""col NAME for a25 
	SELECT name,ceil( space_limit / 1024 / 1024 /1024) SIZE_M,ceil( space_used  / 1024 / 1024 /1024) USED_M,decode( nvl( space_used, 0),0, 0, ceil ( ( space_used / space_limit) * 100) ) PCT_USED FROM v\$recovery_file_dest ORDER BY name;"""
				ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command1)
				#print ucommand
				stdin, stdout, stderr = dssh.exec_command(ucommand)
				output = stdout.read()
				log.info('The command is: %s'%ucommand)
				log.info('The output is: %s'%output)
				error= stderr.read()
				#log.info('The error if any is: %s' %error)
				if error:
					print "ExitCode: 1"
					print "ExitDesc: Error Occured:%s"%error
					Status="Some error Occured. Check logs"
				else:	
					if output and "ORA-" not in output and "ERROR" not in output: 
						output=output.strip(' \t\n\r')
						allLines=""
						tableHtml5=""
						tablestrt="	<table><tr><th> Name </th><th> Size_M </th><th> Used_M </th><th> PCT_Used </th></tr>"
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
						tableHtml5=tablestrt+tableBody+tableEnd
						log.info('ExitCode: 0')
						log.info("ExitDesc: Archive Space Check performed")
						print "ExitCode: 0"
						print "ExitDesc: Archive Space Check performed"
						Status="Successful Execution"
					else:
						print "ExitCode: 1"
						print "ExitDesc: Error Occured:%s"%output
						Status="Some error Occured. Check logs"
			elif FRA_Used=="FALSE":
				command1="archive log list;"
				
				ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command1)
				
				#print ucommand
				stdin, stdout, stderr = dssh.exec_command(ucommand)
				output = stdout.read()
				log.info('The command is: %s'%ucommand)
				log.info('The output is: %s'%output)
				error= stderr.read()
				log.info('The error if any is: %s' %error)
				allLines1=""
				if error:
					print "ExitCode: 1"
					print "ExitDesc: Error Occured:%s"%error
					Status="Some error Occured. Check logs"
				else:	
					if output and "ORA-" not in output and "ERROR" not in output: 
						output=output.strip(' \t\n\r')
						outx=output.splitlines()
						for j in outx:
							if "Archive destination" in j:
								j=j.split()
								j0=str(j[0])
								j1=str(j[1])
								j2=str(j[2])
								
						j2=j2.split("/")
						m=""
						l=len(j2)
						for k in j2:
							if k!=j2[l-1]:
								m=m+k+"/"
						
						#j2="/dev/sda1"
						log.info("The Archive mounted point is %s"%m)
						command2="df -h %s"%m
#						print command2
						log.info("The command is %s"%command2)
						stdin, stdout, stderr = dssh.exec_command(command2)
						error=stderr.read()
						log.info("The Error if any is %s"%error)
						out = stdout.read()
						log.info("The output is %s"%out)
						out=out.strip(' \t\n\r')
						tablestrt1="	<table> <tr> <th>Filesystem </th> <th> Size </th> <th> Used </th>  <th> Avail </th> <th> Use% </th> <th> Mounted on </th> </tr>"
						outx1=out.splitlines()	

						for i in outx1:
							i=i.split()
							if len(i)>=6:
							
								i0=str(i[0])
								i1=str(i[1])
								i2=str(i[2])
								i3=str(i[3])
								i4=str(i[4])
								i5=str(i[5])
								beginning="<tr style='background-color:white;'>"
								bodyEl ="<td style='text-align:center;'> " + i0 + " </td>"
								bodyEl+="<td style='text-align:center;'> " + i1 + " </td>"
								bodyEl+="<td style='text-align:center;'> " + i2 + " </td>"
								bodyEl+="<td style='text-align:center;'> " + i3 + " </td>"
								bodyEl+="<td style='text-align:center;'> " + i4 + " </td>"
								bodyEl+="<td style='text-align:center;'> " + i5 + " </td>"


								end="</tr>"
								allLines+=beginning+bodyEl+end
							else:
								if len(i) == 1:
									i0=str(i[0])
									beginning="<tr style='background-color:white;'>"
									bodyEl ="<td style='text-align:center;'> " + i0 + " </td>"
								else:
									i1=str(i[1])
									i2=str(i[2])
									i3=str(i[3])
									i4=str(i[4])
									i5=str(i[5])
									bodyEl+="<td style='text-align:center;'> " + i1 + " </td>"
									bodyEl+="<td style='text-align:center;'> " + i2 + " </td>"
									bodyEl+="<td style='text-align:center;'> " + i3 + " </td>"
									bodyEl+="<td style='text-align:center;'> " + i4 + " </td>"
									bodyEl+="<td style='text-align:center;'> " + i5 + " </td>"
									end="</tr>"
									allLines+=beginning+bodyEl+end
					
						tableBody=allLines

						tableEnd="</table>"
						tableHtml5=tablestrt1+tableBody+tableEnd
						log.info("the body is %s"%tableHtml5)
						print "ExitCode: 0"
						print "ExitDesc: Archive Space Check performed"
						Status="Successful Execution"
					else:
						print "ExitCode: 1"
						print "ExitDesc: Error Occured:%s"%output
						Status="Some error Occured. Check logs"
						
			else:
				log.info("ExitCode:10")
				log.info("ExitDesc:Enter either TRUE or FALSE for FRA_Used")
				print "ExitCode:10"
				print "ExitDesc:Enter either TRUE or FALSE for FRA_Used"
				Status="Some error Occured. Check logs"
		elif Execution_Location == "LOCAL":
			log.info("The Local Execution")
			loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid
			#loginline="sqlplus -s / as sysdba"
			#loginline=". ~/.bash_profile\nsqlplus -S / as sysdbA"
			if FRA_Used=="TRUE":
		
				command="""set lines 180
	SELECT tablespace_name,size_mb,free_mb,max_size_mb,max_free_mb,
		   TRUNC((max_free_mb/max_size_mb) * 100) AS free_pct,
		   RPAD(' '|| RPAD('X',ROUND((max_size_mb-max_free_mb)/max_size_mb*10,0), 'X'),11,'-') AS used_pct
	FROM   (
			SELECT a.tablespace_name,
				   b.size_mb,
				   a.free_mb,
				   b.max_size_mb,
				   a.free_mb + (b.max_size_mb - b.size_mb) AS max_free_mb
			FROM   (SELECT tablespace_name,
						   TRUNC(SUM(bytes)/1024/1024) AS free_mb
					FROM   dba_free_space
					GROUP BY tablespace_name) a,
				   (SELECT tablespace_name,
						   TRUNC(SUM(bytes)/1024/1024) AS size_mb,
						   TRUNC(SUM(GREATEST(bytes,maxbytes))/1024/1024) AS max_size_mb
					FROM   dba_data_files
					GROUP BY tablespace_name) b
			WHERE  a.tablespace_name = b.tablespace_name
		   )
	ORDER BY Free_pct;"""
				ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command)
				log.info("The Command is %s"%ucommand)
				output = os.popen(ucommand).read()
				output=output.strip(' \t\n\r')
				log.info("The output is %s"%output)
				if output and "ORA-" not in output and "ERROR" not in output: 
					output=output.strip(' \t\n\r')
					tablestrt="	<table><tr><th> Name </th><th> Size_M </th><th> Used_M </th><th> PCT_Used </th></tr>"
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
					tableHtml5=tablestrt+tableBody+tableEnd
					
					log.info('ExitCode: 0')
					log.info("ExitDesc: Archive Space Check performed")
					print "ExitCode: 0"
					print "ExitDesc: Archive Space Check performed"
					Status="Successful Execution"
				else:
					print "ExitCode: 1"
					print "ExitDesc: Error Occured:%s"%output
					Status="Some error Occured. Check logs"
			elif FRA_Used=="FALSE":
				command1="archive log list;"
				ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command1)
				output = os.popen(ucommand).read()
				output=output.strip(' \t\n\r')
				log.info('The command is: %s'%ucommand)
				log.info('The output is: %s'%output)
				if output and "ORA-" not in output and "ERROR" not in output: 
					output=output.strip(' \t\n\r')
					outx=output.splitlines()
					if "Enabled" in outx:
						log.info("The Automatic Archival is Enabled")
						for i in outx:
							if "Archive destination" in i:
								i=i.split()
								i0=str(i[0])
								i1=str(i[1])
								i2=str(i[2])
								
								
								
						i2=i2.split("/")
						m=""
						l=len(i2)
						for k in i2:
							if k!=i2[l-1]:
								m=m+k+"/"
						log.info("The Archive destination is %s "%m)
						command2="df -h %s"%m
						log.info("The command is %s"%command2)
						out = os.popen(command2).read()
						out=out.strip(' \t\n\r')
						tablestrt1="<table> <tr> <th>Filesystem </th> <th> Size </th> <th> Used </th>  <th> Avail </th> <th> Use% </th> <th> Mounted on </th> </tr>"						

								
						for i in out:
							i=i.split()
							if len(i)>=6:
							
								i0=str(i[0])
								i1=str(i[1])
								i2=str(i[2])
								i3=str(i[3])
								i4=str(i[4])
								i5=str(i[5])
								beginning="<tr style='background-color:white;'>"
								bodyEl ="<td style='text-align:center;'> " + i0 + " </td>"
								bodyEl+="<td style='text-align:center;'> " + i1 + " </td>"
								bodyEl+="<td style='text-align:center;'> " + i2 + " </td>"
								bodyEl+="<td style='text-align:center;'> " + i3 + " </td>"
								bodyEl+="<td style='text-align:center;'> " + i4 + " </td>"
								bodyEl+="<td style='text-align:center;'> " + i5 + " </td>"


								end="</tr>"
								allLines+=beginning+bodyEl+end
							else:
								if len(i) == 1:
									i0=str(i[0])
									beginning="<tr style='background-color:white;'>"
									bodyEl ="<td style='text-align:center;'> " + i0 + " </td>"
								else:
									i1=str(i[1])
									i2=str(i[2])
									i3=str(i[3])
									i4=str(i[4])
									i5=str(i[5])
									bodyEl+="<td style='text-align:center;'> " + i1 + " </td>"
									bodyEl+="<td style='text-align:center;'> " + i2 + " </td>"
									bodyEl+="<td style='text-align:center;'> " + i3 + " </td>"
									bodyEl+="<td style='text-align:center;'> " + i4 + " </td>"
									bodyEl+="<td style='text-align:center;'> " + i5 + " </td>"
									end="</tr>"
									allLines+=beginning+bodyEl+end
											

						tableBody=allLines

						tableEnd="</table>"
						tableHtml5=tablestrt1+tableBody+tableEnd
						log.info("The Table Html File is %s"%tableHtml5)

						
						print "ExitCode: 0"
						print "ExitDesc: Archive Space Check performed"
						Status="Successful Execution"
					else:
						print "ExitCode: 1"
						print "ExitDesc: Error Occured:%s"%output
						Status="Some error Occured. Check logs"
				else:
					print "ExitCode:10"
					print "ExitDesc:Automatic Archival is DISABLED"
					log.info("ExitCode:10")
					log.info("ExitDesc:Automatic Archival is DISABLED")
					Status="Automatic Archival is DISABLED"
			else:
				log.info("ExitCode:10")
				log.info("ExitDesc:Enter either TRUE or FALSE for FRA_Used")
				print "ExitCode:10"
				print "ExitDesc:Enter either TRUE or FALSE for FRA_Used"
				Status="Some error Occured. Check logs"
		else:
			print "ExitCode:10"
			print "ExitDesc:Enter proper Execution_Location input"
			log.info("ExitCode:10")
			log.info("ExitDesc:Enter proper Execution_Location input")
			Status="Enter proper Execution_Location input"
					
	except Exception, e:
		print "ExitCode: 10"
		print "ExitDesc: script failed due to: {0}".format(e)
		log.info('ExitCode: 10')
		log.info('ExitDesc: Error Occurred. Check Logs')
		Status="Error Occured"
	
else:
	print "ExitCode: 10"
	print "ExitDesc: Missing Arguments"
	Status="Missing Arguments"
######################### Mailing Part #################################
now = datetime.now()
dt = now.strftime("%A,%d-%B-%y")
dt=str(dt)
FROM  = '%s'%frommail
TO = '%s'%tomail 

SUBJECT = 'ARCHIVE SPACE CHECK '
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
<TH>  Archive Space Check  </TH>

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
