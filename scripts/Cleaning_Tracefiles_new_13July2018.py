"""
        Name: Cleaning_Tracefiles.py
        Description: To check for presence of ORACLE Errors, remote or local execution
        Team: Software Service Automation
        Author: Saicharan Tyarla (sai-charan.thyarla@capgemini.com)
        Inputs: Arguments [HostName,Username,Password,ExecLoc]
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



if len(sys.argv) == 5:
	Execution_Location=sys.argv[1]
	HostName = sys.argv[2]
	OSUser = sys.argv[3]
	OSPassword = sys.argv[4]

	Execution_Location=Execution_Location.upper()
	################################### Creating Log File ###############################
	try:
			if os.name == 'nt':
					logdir = os.getcwd()+"\\logs"
			if os.name == 'posix':
					logdir = os.getcwd()+"/logs"

			logfile = "House_Keeping_Tracefile_%s.log"%HostName
			log = Logger(logdir,logfile)

			log.info('*************************************************************************')

			log.info('Started Script Execution')

	except Exception, e:
			print "ExitCode: 10"
			print "ExitDesc: Unable to create Logfile {0}".format(logfile)

	try:
		log.info("Trying to connect the target host %s"%HostName)
		dssh = paramiko.SSHClient()
		dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		dssh.connect(HostName, username=OSUser, password=OSPassword)
		log.info("The connection is successful")
		DB=""
		St=""
		command="ps -ef | awk '/smon/&&!/awk/{instance=substr($8,10,length($8)-10+1);print instance}'|sort"

		log.info("The Command is %s"%command)
		log.info("trying to execute the command")
		stdin, stdout, stderr = dssh.exec_command(command)
		output = stdout.read()
		log.info("The Output is %s "%output)
		error=stderr.read()
		if error:
				log.info("ExitCode:1")
				log.info("ExitDesc:The Error is %s "%error)
				Status="The Error Occured"
		elif output and "ERROR" not in output:
			output=output.splitlines()
			for i in output:
				loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%i
				command1="""set pages 100
						set feed off
						set head off
						set lines 150
						col value for A80
						select value from v\$diag_info where name='Diag Trace';"""
				ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command1)
				log.info("The Command is %s"%command1)
				log.info("trying to execute the command")
				stdin, stdout, stderr = dssh.exec_command(ucommand)
				output1 = stdout.read()
				output1=output1.strip()
				log.info("The Output is %s "%output1)
				
				if "ERROR" not in output1 and "ORA-" not in output1 and "sp-" not in output1:
					log.info("checking if this TRACE directory is owned by current user")
					command2="ps -ef|grep smon_%s$|awk '{print $1}'"%(i)
					log.info("The Command is %s"%command2)
					log.info("trying to execute the command")
					stdin, stdout, stderr = dssh.exec_command(command2)
					output2 = stdout.read()
					log.info("The Output is %s "%output2)
					output2=output2.strip()
					if output2==OSUser:
						log.info("The TRACE Directory %s  and Database %s is owned by the current %s user"%(output1,i,OSUser))
						command3="""find %s \( -name "*.trm" -o -name "*.trc" \) -user %s -type f -mtime +15 -exec ls -ltrh {} \;"""%(output1,OSUser)
						log.info("The Command is %s"%command3)
						log.info("trying to execute the command")
						stdin, stdout, stderr = dssh.exec_command(command3)
						output3 = stdout.read()
						er=stderr.read()
						log.info("The error if any is %s"%er)
						log.info("The Following files are deleted %s "%output3)
						command4="""find %s \( -name "*.trm" -o -name "*.trc" \) -user %s -type f -mtime +15 | xargs rm -f"""%(output1,OSUser)
						
						log.info("The Command is %s"%command4)
						log.info("trying to execute the command")
						stdin, stdout, stderr = dssh.exec_command(command4)
						output4 = stdout.read()
						error1=stderr.read()
						if error1:
							log.info("The error if any is %s"%error1)
						if "ERROR" not in output4:
							DB=DB+","+i
							print "ExitCode:0"
							print "ExitDesc:Cleaning trace files  Successful for database %s"%(i)
							log.info("ExitCode:0")
							log.info("ExitDesc:Cleaning trace files Successful for database %s"%(i))
							Status="Cleaning Tracefiles Successful for Databases %s"%(DB)
						else:
							print "ExitCode:1"
							print "ExitDesc:Cleaning Tracefiles Failed for Database %s check log file for error"%(i)
							log.info("ExitCode:1")
							log.info("ExitDesc:Cleaning Tracefiles Failed for Database %s"%(i))
							Status="Cleaning Tracefiles Failed"
					else:
						print "ExitCode:10"
						print "ExitDesc:Error occured.. trace Directory %s and Database %s is not owned by the current %s user"%(output1,i,OSUser)
						log.info("ExitCode:1")
						log.info("ExitDesc:Error occured.. trace Directory %s and Database %s is not owned by the current %s user"%(output1,i,OSUser))
						Status1="Error occured.. trace Directory %s and Database %s is not owned by the current %s user"%(output1,i,OSUser)
						St=St+","+Status1
						
				else:
					print "ExitCode:10"
					print "ExitDesc:Error occured check log file"
					log.info("ExitCode:10")
					log.info("ExitDesc:Error occured ")
					Status="Error occured check log file"
					
		else:
			print "ExitCode:10"
			print "ExitDesc:Error occured check log file"
			log.info("ExitCode:10")
			log.info("ExitDesc:Error occured ")
			Status="Error occured check log file"
	except Exception, e:
			print "ExitCode: 10"
			print "ExitDesc: script failed due to: {0}".format(e)
			log.info('ExitCode: 10')
			log.info('ExitDesc: Error Occurred. Check Logs')
			Status="Error Occured"
else:
	print "ExitCode:10"
	print "Missing Arguments"
	Status="Missing Arguments"

############################### Mailing Part #####################################

now = datetime.now()
dt = now.strftime("%A,%d-%B-%y")
dt=str(dt)
FROM  = '%s'%frommail
TO = '%s'%tomail

SUBJECT = 'House Keeping for trace Files '
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
<TH> Success  Status </TH>

</TR>
<TR>
<TD>  %s  </TD>
<TD>  %s  </TD>
<TD>  %s  </TD>
</TR>
</TABLE>
</BODY>
</HTML>""" %(dt,Execution_Location,HostName,Status)
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
 
