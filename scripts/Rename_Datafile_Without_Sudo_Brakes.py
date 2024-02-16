"""
	Name: Rename_Datafile_Without_Sudo_Brakes.py
	Description: To rename a Datafile, remote or local execution
	Team: Software Service Automation
	Author: Arnab Roy (arnab.d.roy@capgemini.com)
	Inputs: Arguments [HostName,Username,Password], LogFileLoc
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




################ Creating the log file ##################
try:
	if os.name == 'nt':
		logdir = os.getcwd()+"\\logs"
	if os.name == 'posix':
		logdir = os.getcwd()+"/logs"
	
	logfile = "Rename_Datafile.log"
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
		OldDatafile =sys.argv[6]			#Old Datafile name to Rename
		NewDatafilePath =sys.argv[7]		#New Datafile Path
		TBSType =sys.argv[8]				#Datafile Type
		Tablespace=sys.argv[9]				#Tablespace name
		Tablespace=Tablespace.upper()

		NewDatafilePath=NewDatafilePath.strip()
		Execution_Location=Execution_Location.upper()
		
		############################ For Remote execution ##########################
		
		if Execution_Location=="REMOTE":
			dssh = paramiko.SSHClient()
			dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			dssh.connect(HostName, username=OSUser, password=OSPassword)

			#loginline=". ~/.bash_profile\nsqlplus -s / as sysdba"
			#loginline="sqlplus -s / as sysdba"
			loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid
		

			############################################## Verifying whether datafile exists or not ###########################################
		
			command1 = "SELECT file_name from dba_data_files where file_name='%s';" %(OldDatafile)
			ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command1)
			log.info('Executing Query: {0}'.format(command1))
			stdin, stdout, stderr = dssh.exec_command(ucommand)
			output1=stdout.read()
			log.info('The command is: %s'%ucommand)
			log.info('The output is: %s'%output1)
			er= stderr.read()
			if er is not None:
				log.info('The error if any is: %s' %er)
				
			if output1 is not None:
				out1 = str(output1).translate(None, "[( ',	)]")
				out1=out1.strip() 
			if out1 == OldDatafile:
		
			
			############################ Taking the datafile offline #################################
			
				command2 = "Alter database datafile '%s' offline;" %(OldDatafile)
				ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command2)
				log.info('Executing Query: {0}'.format(command2))
			stdin, stdout, stderr = dssh.exec_command(ucommand)
			output2=stdout.read()
			log.info('The command is: %s'%ucommand)
			log.info('The output is: %s'%output2)
			er= stderr.read()
			if er is not None:
				log.info('The error if any is: %s' %er)
					
			
			
			
			################################################# Moving datafile to new dest ######################################################
			
				cmd = "mv %s %s" %(OldDatafile,NewDatafilePath)
				dssh.exec_command(cmd)
				log.info('Moving the DataFile using command: {0}'.format(cmd))
			
			################### Query to Rename the Database #######################

			
				command3="ALTER DATABASE RENAME FILE '%s' TO '%s';" %(OldDatafile,NewDatafilePath)
				ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command3)
				log.info('Executing Query: {0}'.format(command3))
				stdin, stdout, stderr = dssh.exec_command(ucommand)
				output3=stdout.read()
				log.info('The command is: %s'%ucommand)
				log.info('The output is: %s'%output3)
				er= stderr.read()
				if er is not None:
					log.info('The error if any is: %s' %er)
				
				
			############################ Taking the datafile online #################################
			
				command4 = "Alter database datafile '%s' online;" %(NewDatafilePath)
				ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command4)
				log.info('Executing Query: {0}'.format(command4))
				stdin, stdout, stderr = dssh.exec_command(ucommand)
				output4=stdout.read()
				log.info('The command is: %s'%ucommand)
				log.info('The output is: %s'%output4)
				er= stderr.read()
				if er is not None:
					log.info('The error if any is: %s' %er)
				
			################# Verifying whether renaming is successful or not############
			
				if TBSType == "TEMP":
					query = "select FILE_NAME from dba_temp_files where TABLESPACE_NAME='%s' and FILE_NAME= '%s';" %(Tablespace,NewDatafilePath)
				else:
					query = "select FILE_NAME from dba_data_files where TABLESPACE_NAME='%s' and FILE_NAME= '%s';" %(Tablespace,NewDatafilePath)
			
				ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,query)
				log.info('Executing Query: {0}'.format(query))
				stdin, stdout, stderr = dssh.exec_command(ucommand)
				output=stdout.read()
				log.info('The command is: %s'%ucommand)
				log.info('The output is: %s'%output)
				er= stderr.read()
				if er is not None:
					log.info('The error if any is: %s' %er)
				
				if output is not None:
					out = str(output).translate(None, "[( ',	)]")
					out=out.strip()
				#print "old"
				#print OldDatafile
				#print "Out: %s" %(out)
				#print "new"
				#print NewDatafilePath
				
				if out == NewDatafilePath:
					print "ExitCode: 0"
					print "ExitDesc: Datafile Rename successful. "
					log.info('ExitDesc : Datafile of the Tablespace {0} Rename succesful from  {1} to {2}'.format(Tablespace,OldDatafile,NewDatafilePath))
					log.info('Exitcode: 0')
					Status="Datafile Renaming Successful"

				else:
					print "ExitCode: 10"
					print "ExitDesc: Datafile Rename  failed"
					log.info('ExitDesc: Datafile Rename : {0} Failed'.format(Tablespace))
					log.info('Exitcode: 10')
					Status="Datafile Renaming Failed"
	
			else:
				print "ExitCode: 10"
				print "ExitDesc: Datafile rename failed, since Datafile does not exist"
				log.info('ExitCode: 10')
				log.info('ExitDesc: Datafile rename failed, since Datafile does not exist') 
				Status="Datafile Renaming Failed. Datafile does not exist"
            
		elif Execution_Location=="LOCAL":
			
			#loginline=". ~/.bash_profile\nsqlplus -s / as sysdba"
			#loginline="sqlplus -s / as sysdba"
                	loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid
				
			############################################## Verifying whether datafile exists or not ###########################################
		
			command1 = "SELECT file_name from dba_data_files where file_name='%s';" %(OldDatafile)
			ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command1)
			log.info('Executing Query: {0}'.format(command1))
			output1=os.popen(ucommand).read()
			log.info('The command is: %s'%ucommand)
			log.info('The output is: %s'%output1)
			if output1 is not None:
				out1 = str(output1).translate(None, "[( ',	)]")
				out1=out1.strip() 
			if out1 == OldDatafile:
			
			############################ Taking the datafile offline #################################
			
				command22 = "Alter database datafile '%s' offline;" %(OldDatafile)
				ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command22)
				log.info('Executing Query: {0}'.format(command22))
				output22=os.popen(ucommand).read()
				log.info('The command is: %s'%ucommand)
				log.info('The output is: %s'%output22)

			################################################# Moving datafile to new dest ######################################################
			
				cmd = "mv %s %s" %(OldDatafile,NewDatafilePath)
				dssh.exec_command(cmd)
				log.info('Moving the DataFile using command: {0}'.format(cmd))
			
			
			################### Query to Rename the Database #######################

			
				command="ALTER DATABASE RENAME FILE '%s' TO '%s';" %(OldDatafile,NewDatafilePath)
				ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command)
				log.info('Executing Query: {0}'.format(command))
				output2=os.popen(ucommand).read()
				log.info('The command is: %s'%ucommand)
				log.info('The output is: %s'%output2)
				
			############################ Taking the datafile online #################################
			
				command4 = "Alter database datafile '%s' online;" %(NewDatafilePath)
				ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command4)
				log.info('Executing Query: {0}'.format(command4))
				output4=os.popen(ucommand).read()
				log.info('The command is: %s'%ucommand)
				log.info('The output is: %s'%output4)	
				
			################# Verifying whether renaming is successful or not ###############
			
				if TBSType == "TEMP":
					query = "select FILE_NAME from dba_temp_files where TABLESPACE_NAME='%s' and FILE_NAME= '%s';" %(Tablespace,NewDatafilePath)
				else:
					query = "select FILE_NAME from dba_data_files where TABLESPACE_NAME='%s' and FILE_NAME= '%s';" %(Tablespace,NewDatafilePath)
					
					ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,query)
					log.info('Executing Query: {0}'.format(query))
					output=os.popen(ucommand).read()
					log.info('The command is: %s'%ucommand)
					log.info('The output is: %s'%output)
					
					if output == NewDatafilePath:
						print "ExitCode: 0"
						print "ExitDesc: Datafile Rename succesful. "
						log.info('ExitDesc : Datafile of the Tablespace {0} Rename successful from  {1} to {2}'.format(Tablespace,OldDatafile,NewDatafilePath))
						log.info('Exitcode: 0')
						Status="Datafile Renaming Successful"

					else:
						print "ExitCode: 10"
						print "ExitDesc: Datafile Rename  failed"
						log.info('ExitDesc: Datafile Rename : {0} Failed'.format(Tablespace))
						log.info('Exitcode: 10')
						Status="Datafile Renaming Failed"
						
			else:
				print "ExitCode: 10"
				print "ExitDesc: Datafile rename failed, since Datafile does not exist"
				log.info('ExitCode: 10')
				log.info('ExitDesc: Datafile rename failed, since Datafile does not exist')
				Status="Datafile Renaming Failed. Datafile does not exist"
						
			
	
    else:
		print "ExitCode: 10"
		print "ExitDesc: Missing Arguments"
		log.info('ExitCode: 10')
		log.info('ExitDesc: Missing Arguments')
		Status="Some error occurred. Check logs"
		
except Exception, e:
	print "ExitCode: 1"
	print "ExitDesc: script failed due to: {0}".format(e)
	log.info('ExitCode: 10')
	log.info('ExitDesc: Missing Arguments')
	Status="Some error occurred. Check logs"
	
################################ Mail part ##################################

now = datetime.now()
dt = now.strftime("%A,%d-%B-%y")
dt=str(dt)
FROM  = '%s'%frommail
TO = '%s'%tomail

SUBJECT = 'RENAME DATAFILE PROCESS '
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
<TH>  SID  </TH>
<TH>  Old Datfile Name  </TH>
<TH>  New Datfile Name  </TH>
<TH>  Tablespace Type  </TH>
<TH>  Tablespace Name  </TH>
<TH>  Status </TH>
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
</HTML>""" %(dt,Execution_Location,HostName,Sid,OldDatafile,NewDatafilePath,TBSType,Tablespace,Status)
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
	
