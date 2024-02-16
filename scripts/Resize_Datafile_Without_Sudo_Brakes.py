"""
	Name: Resize_Datafile_Without_Sudo_Brakes.py
	Description: To resize a Datafile, remote target server or local target server
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
	
	logfile = "Resize_Datafile.log"
	log = Logger(logdir,logfile)

	log.info('*************************************************************************')

	log.info('Started Script Execution')
	
except Exception, e:
    print "ExitCode: 10"
    print "ExitDesc: Unable to create Logfile {0}".format(logfile)
	
	

try:
    
    if len(sys.argv) == 10:
		Execution_Location=sys.argv[1]
		HostName = sys.argv[2] 
		OSUser = sys.argv[3] 
		OSPassword = sys.argv[4]
		Sid=sys.argv[5]
		Datafile =sys.argv[6]					#Datafile name to resize
		Size =sys.argv[7]						#New Datafile Size
		DatafileType =sys.argv[8]				#Datafile Type
		Tablespace=sys.argv[9]					#Tablespace name
		Tablespace=Tablespace.upper()
		Execution_Location=Execution_Location.upper()
		DatafileType=DatafileType.upper()
		
		############################ For Remote execution ##########################
		
		if Execution_Location=="REMOTE":
			dssh = paramiko.SSHClient()
			dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			dssh.connect(HostName, username=OSUser, password=OSPassword)

			#loginline=". ~/.bash_profile\nsqlplus -s / as sysdba"
			#loginline="sqlplus -s / as sysdba"
			loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid
		

			############################################## Verifying whether DataFile exists or not ###########################################
		
			if DatafileType =="TEMP":
				command1 = """set lines 100
				col FILE_NAME for a500 
				set pages 1000
				SELECT file_name from dba_temp_files where file_name='%s';""" %(Datafile)
			else:
				command1 = """set lines 100
                                col FILE_NAME for a500
                                set pages 1000
                                SELECT file_name from dba_data_files where file_name='%s';""" %(Datafile)	
			ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command1)
			log.info('Executing Query: {0}'.format(command1))
			stdin, stdout, stderr = dssh.exec_command(ucommand)
			output1=stdout.read()
			log.info('The command is: %s'%ucommand)
			log.info('The output is: %s'%output1)
			er= stderr.read()
			
			if output1 is not None:
				out1 = str(output1).translate(None, "[( ',	)]")
				out1=out1.strip() 
			if out1 == Datafile:
		
		

			
			################### Query to Resize the DataFile #######################

				if DatafileType =="TEMP":
					command="ALTER DATABASE TEMPFILE '%s' RESIZE %sM;" %(Datafile,Size)
				else:
					command="ALTER DATABASE DATAFILE '%s' RESIZE %sM;" %(Datafile,Size)
				ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command)
				log.info('Executing Query: {0}'.format(command))
				stdin, stdout, stderr = dssh.exec_command(ucommand)
				cmdout=stdout.read()
				log.info('The command is: %s'%ucommand)
				log.info('The output is: %s'%cmdout)
				er= stderr.read()
				#print cmdout
				
				
			################# Verifying whether renaming is successful or not############
			
				if DatafileType == "TEMP":
					query = "select bytes/1024/1024 from dba_temp_files where TABLESPACE_NAME='%s' and FILE_NAME= '%s';" %(Tablespace,Datafile)
				else:
					query = "select bytes/1024/1024 from dba_data_files where TABLESPACE_NAME='%s' and FILE_NAME= '%s';" %(Tablespace,Datafile)
			
				ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,query)
				log.info('Executing Query: {0}'.format(query))
				stdin, stdout, stderr = dssh.exec_command(ucommand)
				output=stdout.read()
				log.info('The command is: %s'%ucommand)
				log.info('The output is: %s'%output)
				er= stderr.read()
				
				if output is not None:
					out = str(output).translate(None, "[( ',	)]")
					out=out.strip()
				
				if out == Size:
					print "ExitCode: 0"
					print "ExitDesc: Datafile Resizing succesful. "
					log.info('ExitDesc : Datafile {0} of the Tablespace {1} Resizing succesful to {2}'.format(Datafile,Tablespace,Size))
					log.info('Exitcode: 0')
					Status="Resizing successful"

				else:
					print "ExitCode: 10"
					print "ExitDesc: Datafile Resizing  failed"
					log.info('ExitDesc: Datafile Resizing Failed')
					log.info('Exitcode: 10')
					Status="Resizing failed"
	
			else:
				print "ExitCode: 10"
				print "ExitDesc: Datafile resizing failed, since Datafile does not exist"
				log.info('ExitCode: 10')
				log.info('ExitDesc: Datafile resizing failed, since Datafile does not exist')
				Status= "Failure. Datafile does not exist"
            
		elif Execution_Location=="LOCAL":
			
			#loginline=". ~/.bash_profile\nsqlplus -s / as sysdba"	
			#loginline="sqlplus -s / as sysdba"
                	loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid
				
			############################################## Verifying whether DataFile exists or not ###########################################
			if DatafileType =="TEMP":
                                command1 = """set lines 100
                                col FILE_NAME for a500
                                set pages 1000
                                SELECT file_name from dba_temp_files where file_name='%s';""" %(Datafile)
                        else:
                                command1 = """set lines 100
                                col FILE_NAME for a500
                                set pages 1000
                                SELECT file_name from dba_data_files where file_name='%s';""" %(Datafile)				
			ucommand= "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command1)
			log.info('Executing Query: {0}'.format(command1))
			output1=os.popen(ucommand).read()
			log.info('The command is: %s'%ucommand)
			log.info('The output is: %s'%output1)
			
			if output1 is not None:
				out1 = str(output1).translate(None, "[( ',	)]")
				out1=out1.strip() 
			if out1 == Datafile:

			
			
			
			################### Query to Resize the DataFile #######################

				if DatafileType =="TEMP":
					command="ALTER DATABASE TEMPFILE '%s' RESIZE %sM;" %(Datafile,Size)
				else:
					command="ALTER DATABASE DATAFILE '%s' RESIZE %sM;" %(Datafile,Size)
				ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command)
				log.info('Executing Query: {0}'.format(command))
				output2=os.popen(ucommand).read()
				log.info('The command is: %s'%ucommand)
				log.info('The output is: %s'%output2)
				
			################# Verifying whether renaming is successful or not ###############
			
				if DatafileType == "TEMP":
					query = "select bytes/1024/1024 from dba_temp_files where TABLESPACE_NAME='%s' and FILE_NAME= '%s';" %(Tablespace,Datafile)
				else:
					query = "select bytes/1024/1024 from dba_data_files where TABLESPACE_NAME='%s' and FILE_NAME= '%s';" %(Tablespace,Datafile)
					
					ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,query)
					log.info('Executing Query: {0}'.format(query))
					output=os.popen(ucommand).read()
					log.info('The command is: %s'%ucommand)
					log.info('The output is: %s'%output)
					
					if output == Size:
						print "ExitCode: 0"
						print "ExitDesc: Datafile Resizing succesful. "
						log.info('ExitDesc : Datafile {0} of the Tablespace {1} Resize succesful to {2}'.format(Datafile,Tablespace,Size))
						log.info('Exitcode: 0')
						Status="Resizing successful"

					else:
						print "ExitCode: 10"
						print "ExitDesc: Datafile Resizing  failed"
						log.info('ExitDesc: Datafile Resizing Failed')
						log.info('Exitcode: 10')
						Status="Resizing failed"
			else:
				print "ExitCode: 10"
				print "ExitDesc: Datafile resizing failed, since Datafile does not exist"
				log.info('ExitCode: 10')
				log.info('ExitDesc: Datafile resizing failed, since Datafile does not exist')
				Status= "Failure. Datafile does not exist"
    else:
		print "ExitCode: 10"
		print "ExitDesc: Missing Arguments"
		log.info('ExitCode: 10')
		log.info('ExitDesc: Missing Arguments')
		Status="Error occured. Check logs"
except Exception, e:
	print "ExitCode: 1"
	print "ExitDesc: script failed due to: {0}".format(e)
	log.info('ExitCode: 1')
	log.info('ExitDesc: Script failed due to: {0}'.format(e))
	Status="Error occured. Check logs"
	
	
################################ Mail part ##################################

now = datetime.now()
dt = now.strftime("%A,%d-%B-%y")
dt=str(dt)
FROM  = '%s'%frommail
TO = '%s'%tomail

SUBJECT = ' RESIZE DATAFILE PROCESS '
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
<TH>  Datafile Name  </TH>
<TH>  Tablespace_type </TH>
<TH>  Tablespace  </TH> 
<TH>  New Size (in MB)  </TH>
<TH>  Status  </TH>
</TR>
<TR>
<TD>  %s  </TD>
<TD>  %s  </TD>
<TD>  %s  </TD>
<TD>  %s  </TD>
<TD>  %s  </TD>
<TD>  %s  </TD>
<TD>  %s  </TD>
<TD>  %s  </TD>
</TR> 
</TABLE>
</BODY>
</HTML>""" %(dt,Execution_Location,HostName,Sid,Datafile,DatafileType,Tablespace,Size,Status)
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
