"""
	Name: Add_Member_To_Redo_Log_Group_Without_Sudo.py
	Team: Software Service Automation
	Author: Gaurav Pandey(gaurav.a.pandey@capgemini.com)
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


try:
    
    if len(sys.argv) == 9:
        Execution_Location=sys.argv[1]
        HostName = sys.argv[2] 
        OSUser = sys.argv[3] 
        OSPassword = sys.argv[4]
        Sid=sys.argv[5]
        Log_file_location=sys.argv[6]
        Group_No=sys.argv[7]
        Group_size=sys.argv[8]
        ################################### Creating Log File ###############################
        try:
            if os.name == 'nt':
                logdir = os.getcwd()+"\\logs"
            if os.name == 'posix':
                logdir = os.getcwd()+"/logs"
			
            logfile = "Add_Member_TO RedologGroup_%s.log"%(HostName)
            log = Logger(logdir,logfile)

            log.info('*************************************************************************')
			#print "Log file created"
            log.info('Started Script Execution')
			
        except Exception, e:
            print "ExitCode: 10"
            print "ExitDesc: Unable to create Logfile {0} {1}".format(logfile,e)

		################################### END OF LOG FILE CREARION ######################################
		
		
        log.info('*************************************************************************')
        log.info('Started Script Execution')
        if "," in Log_file_location:
                a=Log_file_location.split(",")
                b=[]
                for i in a:
                    j=i.strip()
                    b.append(j)
                Log_file_location=b
                Log_file_location=str(Log_file_location)
                Log_file_location=Log_file_location.strip("[ ]")
        if Execution_Location=="REMOTE":
            log.info('Started Script Execution in remote location')
            loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid
            #loginline=". ~/.bash_profile\nsqlplus -S / as sysdbA"
            #loginline="sqlplus -s / as sysdba"
            dssh = paramiko.SSHClient()
            dssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            dssh.connect(HostName, username=OSUser, password=OSPassword)
			
            if "," in Log_file_location:
                command="ALTER DATABASE ADD LOGFILE MEMBER (%s) to group %s ;"%(Log_file_location,Group_No)
            else:
                command="ALTER DATABASE ADD LOGFILE MEMBER '%s' to group %s ;"%(Log_file_location,Group_No)
            
            ucommand = "%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(loginline,command)
            log.info('Command for script Execution:%s'%ucommand)
            #print ucommand
            stdin, stdout, stderr = dssh.exec_command(ucommand)
            output = stdout.read()
            log.info('Output: %s'%output)
            error=stderr.read()
            if error:
                log.info("ExitCode:10")
                log.info("ExitDesc: Error Occured:%s"%error)
                print "ExitCode:10"
                print "ExitDesc: Error Occured check log file "
                Status="Log Group Creation Failed. Error"
            else:				
                if "ERROR" not in output and "ORA-" not in output and "SP-" not in output:
                    log.info("0: ExitDesc:  Log member Added Successfully")
                    print "ExitCode0"
                    print "ExitDesc:  Log member Added Successfully"
                    Status="Log Member Added Successfully"
                else:
                    log.info("10: ExitDesc: Error Occured:%s"%output)
                    print "ExitCode:10"
                    print "ExitDesc: Error Occured:%s"%output
                    Status="Error Occurred. Check Logs"
        else:
            log.info("Started Command Execution in Local machine")
            loginline="export ORACLE_SID=%s\nexport ORAENV_ASK=NO\n. oraenv > /dev/null 2>&1\nsqlplus -s / as sysdba"%Sid
            #loginline="sqlplus -s / as sysdba"
            #loginline=". ~/.bash_profile\nsqlplus -s / as sysdba"
            if "," in Log_file_location:
                command="ALTER DATABASE ADD LOGFILE MEMBER (%s) to group %s ;"%(Log_file_location,Group_No)
            else:
                command="ALTER DATABASE ADD LOGFILE MEMBER '%s' to group %s ;"%(Log_file_location,Group_No)
            ucommand = "%s\n%s/bin/%s << EOF\nset heading off;\nset feedback off;\n%s\nexit;\nEOF" %(env_var,Ora_home,loginline,command)
            log.info("Main Command for execution:%s"%ucommand)
            output = os.popen(ucommand).read()
            log.info("Command got executed:%s"%output)
            if "ERROR" not in output and "ORA-" not in output and "SP-" not in output:
                log.info("0: ExitDesc: Log member Added Successfully")
                print "ExitCode:0"
                print "ExitDesc:  Log member Added Successfully"
                Status="Log Member Added Successfully"
            else:
                log.info("10: ExitDesc: Error Occured:%s"%output)
                print "ExitCode:10"
                print "ExitDesc: Error Occured:%s"%output
                Status="Log Member Addition Failed. Error Occurred. Check Logs"
	
    else:

        print "10"
        print "ExitDesc: Missing Arguments"
        Status="Error Occurred. Check Logs"
		
except Exception, e:

    print "1"
    print "ExitDesc: script failed due to: {0}".format(e)
    Status="Error Occurred. Check Logs"
	
################################ Mail part ##################################

now = datetime.now()
dt = now.strftime("%A,%d-%B-%y")
dt=str(dt)
FROM  = '%s'%frommail
TO = '%s'%tomail

SUBJECT = 'Add_Member_To_Redo_Log_Group '
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
<TH>  Log_file_location  </TH>
<TH>  Group_No  </TH>
<TH>  Group_size  </TH>
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
</TR> 
</TABLE>
</BODY>
</HTML>""" %(dt,Execution_Location,HostName,Sid,Log_file_location,Group_No,Group_size,Status)
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
