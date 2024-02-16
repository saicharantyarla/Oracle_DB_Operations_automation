"""
	Name: MainMenu.py
	Description: Contains the list of process and use to trigger the process on the target server
	Team: Software Service Automation
	Author: Saicharan Tyarla(sai-charan.thyarla@capgemini.com)
	Inputs: Arguments will be taken at run time
	Output: ExitCode, ExitDesc(Log File)
"""

#!/usr/bin/env python
import os
from Logger import Logger
from os import system, getcwd, path, makedirs
import sys
import getpass

############# PRECHECKS and inputs ##########
try:

	def common_input():
			
		Hostname=raw_input("Enter the hostname/IPaddress of the server:")
		if os.name == 'nt':
			output=os.popen("ping -n 1 %s"%Hostname).read()
		else:
			output=os.popen("ping -c 1 %s"%Hostname).read()
		if "ERROR" in output or "100% packet loss" in output or "Destination host unreachable" in output or "unknown host" in output or "100% loss" in output or "Request timed out." in output or "could not find host" in output:
			print "ExitDesc:Ping Failed, Server is unknown or un-reachable"
			exit()
		else:
			print "server %s is reachable"%Hostname
			OSUsername=raw_input("Enter the username:")
			OSPassword=getpass.getpass("Enter the password for the user %s:"%OSUsername)
			if os.name == 'nt':
				host=os.popen("hostname").read()
				ip=os.popen("ipconfig").read()
				dir12 = os.getcwd()+"\scripts"
			if os.name == 'posix':
				host=os.popen("hostname").read()
				ip=os.popen("ifconfig").read()
				dir12 = os.getcwd()+"/scripts"
			if Hostname in ip or Hostname in host:
				Exec_location="Local"
			else:
				Exec_location="REMOTE"
			values=Exec_location+" "+Hostname+" "+OSUsername+" "+OSPassword
			#print dir12
			return values,dir12
			#return dir12
	def Input_DB():
		DBName=raw_input("Enter the Database name:")
		return DBName
			
	def default():
		print("Invalid option")
		


	print(""" 				Welcome to Automation...!!
				 _______________________________________________
				|                                               |
				|                Main  Menu                     |
				|_______________________________________________|
				|                                               |
				|       A.Monitoring and Reporting              |
				|       B.Database Administration               |
				|       C.Database Maintenance                  |
				|       D.Database User Management              |
				|_______________________________________________|   """)

				
	process=raw_input("Please Select the Process to run. Eg. A<ENTER>:")			
	process=process.upper()

	def Schema_Object_details():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()
		values=values+" "+DBName
		if os.name == 'nt':
			Final_result=os.system("python %s\Schema_obj_details.py %s"%(dir12,values))	#Execution_Location,HostName,OSUser,OSPassword,Sid
			return Final_result
		else:
			Final_result=os.system("python %s/Schema_obj_details.py %s"%(dir12,values))	#Execution_Location,HostName,OSUser,OSPassword,Sid
			return Final_result
	def Archive_Space_Check():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()
		Fra_Used=input("Enter TRUE if the DB is using Flash recovery area else FALSE:")
		Fra_Used=Fra_Used.upper()
		values=values+" "+DBName+" "+Fra_Used
		if os.name == 'nt':
			Final_result=os.system("python %s\Archive_Space_Check.py %s"%(dir12,values))	#Execution_Location,HostName,OSUser,OSPassword,Sid,FRA_USED
			return Final_result
		else:
			Final_result=os.system("python %s/Archive_Space_Check.py %s"%(dir12,values))	#Execution_Location,HostName,OSUser,OSPassword,Sid,FRA_USED
			return Final_result
	def ASM_Disk_Space():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()
		values=values+" "+DBName
		if os.name == 'nt':
			Final_result=os.system("python %s\ASM_DiskSpace_check.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid
			return Final_result
		else:	
			Final_result=os.system("python %s/ASM_DiskSpace_check.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid
			return Final_result
			
	def ASM_RAC_Cluster_Status():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()
		values=values+" "+DBName
		if os.name == 'nt':
			Final_result=os.system("python %s\ASM_RAC_Cluster_Status_Without_Sudo_Brakes.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid
			return Final_result
		else:
			Final_result=os.system("python %s/ASM_RAC_Cluster_Status_Without_Sudo_Brakes.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid
			return Final_result
			
	def Dataguard_Status():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()
		values=values+" "+DBName
		if os.name == 'nt': 
			Final_result=os.system("python %s\Dataguard_Status.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid
			return Final_result
		else:
			Final_result=os.system("python %s/Dataguard_Status.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid
			return Final_result
			
	def Capacity_Planning():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
	#	print values1
	#	print dir123
		DBName=Input_DB()
		values=values+" "+DBName
		if os.name == 'nt':
			Final_result=os.system("python %s\Capacity_Planning.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid
			return Final_result
		else:
			scriptname="python %s/Capacity_Planning.py %s"%(dir12,values)
			print scriptname
			Final_result=os.system(scriptname)    #Execution_Location,HostName,OSUser,OSPassword,Sid
			return Final_result
		
	def exit_script():
		print("Thank you for using Automation!! Bye.")
		exit()
	def zero():
		print(""" 
					________________________________________________
					|                                               |
					|       A.Monitoring and Reporting              |
					|_______________________________________________|
					|                                               |
					|       1.Schema Object details in a Tablespace |
					|       2.ASM Disk Space Report                 |
					|       3.ASM and RAC Cluster Status            |
					|       4.DATAGUARD STATUS                      |
					|       5.Archive Destination Report            |
					|       6.Capacity Planning Report              |
					|_______________________________________________|		""")
		sub_process=int(input("Please select the task no. to execute. Eg. 1<ENTER>:"))
		sub_switch = {
					1:Schema_Object_details,
					2:Archive_Space_Check,
					3:ASM_Disk_Space,
					4:ASM_RAC_Cluster_Status,
					5:Dataguard_Status,
					6:Capacity_Planning,
					0:exit_script
					}
					
		Final=sub_switch.get(sub_process,default)()
		return Final
	def Create_Redo_Logfile():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()
		Log_grp_location=raw_input("Please enter Log group location with file:")
		Log_grp_Size=raw_input("Please enter the Log group size:")
		values=values+" "+DBName+" "+Log_grp_location+" "+Log_grp_Size
		if os.name == 'nt':
			Final_result=os.system("python %s\Create_Redo_Logfile_Without_Sudo_Brakes.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid,Log grouplocation,log groupsize
			return Final_result
		else:
			Final_result=os.system("python %s/Create_Redo_Logfile_Without_Sudo_Brakes.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid,Log grouplocation,log groupsize
			return Final_result			
	def Add_Member_To_Redo_Loggroup():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()
		Log_file_location=raw_input("Please enter Log file location")
		Log_grp_No=raw_input("Please enter Log group No.:")
		Log_grp_Size=raw_input("Please enter the Log group size:")
		values=values+" "+DBName+" "+Log_file_location+" "+Log_grp_No+" "+Log_grp_Size
		if os.name == 'nt':
			Final_result=os.system("python %s\Add_Member_To_Redo_Log_Group_Without_Sudo.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid,Log_file_location,Log_grp_No,Log_grp_Size
			return Final_result
		else:
			Final_result=os.system("python %s/Add_Member_To_Redo_Log_Group_Without_Sudo.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid,Log_file_location,Log_grp_No,Log_grp_Size
			return Final_result
		
	def Drop_Redo_Logfile():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()
		Log_grp_No=raw_input("Please enter Log group No.:")
		values=values+" "+DBName+" "+Log_grp_No
		if os.name == 'nt':
			Final_result=os.system("python %s\Drop_Redo_Log_File.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid,Log_grp_No
			return Final_result
		else:
			Final_result=os.system("python %s/Drop_Redo_Log_File.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid,Log_grp_No
			return Final_result
			
	def SPfile_Creation():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()
		values=values+" "+DBName
		if os.name == 'nt':
			Final_result=os.system("python %s\SPfile_Without_Sudo.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid	
			return Final_result
		else:
			Final_result=os.system("python %s/SPfile_Without_Sudo.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid	
			return Final_result
	def Pfile_Creation():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()
		Flag=raw_input("If you want to create Pfile in Deafult Location Enter TRUE or else FALSE:")
		if os.name == 'nt':
			Final_result=os.system("python %s\Pfile_Test_Without_Sudo_Brakes_new.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid
			return Final_result
		else:
			Final_result=os.system("python %s/Pfile_Test_Without_Sudo_Brakes_new.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid
			return Final_result	
	def Enable_Archive_Log():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()
		values=values+" "+DBName
		if os.name == 'nt':
			Final_result=os.system("python %s\Enable_Archive_Log_Test_Without_Sudo_Brakes.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid
			return Final_result
		else:
			Final_result=os.system("python %s/Enable_Archive_Log_Test_Without_Sudo_Brakes.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid
			return Final_result
		
	def Disable_Archive_log():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()
		values=values+" "+DBName
		if os.name == 'nt':
			Final_result=os.system("python %s\Disable_Archive_Log_Test_Without_Sudo_Brakes.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid
			return Final_result
		else:
			Final_result=os.system("python %s/Disable_Archive_Log_Test_Without_Sudo_Brakes.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid
			return Final_result
		
	def Multiplex_ctlfile():
			print("Currently this option is not available")
	def Recreating_ctlfile():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()
		ctlfile_path=raw_input("Please enter Control file path for backup:")
		values=values+" "+DBName+" "+ctlfile_path
		if os.name == 'nt':
			Final_result=os.system("python %s\Recreating_Controlfile_Without_Sudo_Brakes.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid,controlfile_path
			return Final_result
		else:
			Final_result=os.system("python %s/Recreating_Controlfile_Without_Sudo_Brakes.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid,controlfile_path
			return Final_result
		
	def Start_DB():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()
		values=values+" "+DBName
		if os.name == 'nt':
			Final_result=os.system("python %s\Start_DB_Without_Sudo_Brakes.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid
			return Final_result
		else:
			Final_result=os.system("python %s/Start_DB_Without_Sudo_Brakes.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid
			return Final_result
		
	def Stop_DB():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()
		values=values+" "+DBName
		if os.name == 'nt':
			Final_result=os.system("python %s\Stop_DB_Without_Sudo_Brakes.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid
			return Final_result
		else:
			Final_result=os.system("python %s/Stop_DB_Without_Sudo_Brakes.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid
			return Final_result
		
	def Table_shrink():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()
		Table_name=raw_input("Please enter valid Table name:")
		values=values+" "+DBName+" "+Table_name
		if os.name == 'nt':
			Final_result=os.system("python %s\Shrink_Reorg_Without_Sudo_Brakes.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid,Tablename
			return Final_result
		else:
			Final_result=os.system("python %s/Shrink_Reorg_Without_Sudo_Brakes.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid,Tablename
			return Final_result
		
	def ORA_errors():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()
		values=values+" "+DBName
		if os.name == 'nt':
			Final_result=os.system("python %s\Analysing_ORA_Errors_Without_Sudo_Brakes.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid
			return Final_result
		else:
			Final_result=os.system("python %s/Analysing_ORA_Errors_Without_Sudo_Brakes.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid
			return Final_result
		
	def Clean_auditfiles():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		if os.name == 'nt':
			Final_result=os.system("python %s\Cleaning_AuditFiles.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword
			return Final_result
		else:
			Final_result=os.system("python %s/Cleaning_AuditFiles.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword
			return Final_result	
		
	def Clean_tracefiles():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		if os.name == 'nt':
			Final_result=os.system("python %s\Cleaning_Tracefiles_new_13July2018.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword
			return Final_result
		else:
			Final_result=os.system("python %s/Cleaning_Tracefiles_new_13July2018.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword
			return Final_result
		
	def Add_datafile():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()
		Tablespace_name=raw_input("Please enter valid Tablespace name:")
		values=values+" "+DBName+" "+Tablespace_name
		if os.name == 'nt':
			Final_result=os.system("python %s\Add_Datafile_Without_Sudo_Brakes.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid,Tablespacename
			return Final_result
		else:
			Final_result=os.system("python %s/Add_Datafile_Without_Sudo_Brakes.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid,Tablespacename
			return Final_result
			
	def Add_tempfile():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()
		Datafilename=raw_input("Please enter valid Datafile name/full path:")
		Tablespace_name=raw_input("Please enter valid Tablespace name:")
		Datafile_size=raw_input("Please enter the size of the datafile $datafilename in MB:")
		Auto_extend=raw_input("Please enter the option for Autoextend [True/False]:")
		values=values+" "+DBName+" "+Datafilename+" "+Tablespace_name+" "+Datafile_size+" "+Auto_extend
		if os.name == 'nt':
			Final_result=os.system("python %s\Add_Tempfile_Without_Sudo_Brakes.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid,datafilename,Tablespacename,,DatafileSize,Autoextend
			return Final_result
		else:
			Final_result=os.system("python %s/Add_Tempfile_Without_Sudo_Brakes.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid,datafilename,Tablespacename,,DatafileSize,Autoextend
			return Final_result
			
	def Datafile_rename():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()	
		Datafilename=raw_input("Please enter the Datafile name/full path to rename:")
		New_datafilename=raw_input("Please enter the new name/path for the datafile %s:"%Datafilename)
		Tablespace_type=raw_input("Please enter the Tablespace Type[PERMANENT/TEMP/UNDO]:")
		Tablespace_name=raw_input("Please enter valid Tablespace name:")
		values=values+" "+DBName+" "+Datafilename+" "+New_datafilename+" "+Tablespace_type+" "+Tablespace_name
		if os.name == 'nt':
		
			Final_result=os.system("python %s\Rename_Datafile_Without_Sudo_Brakes.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid,OldDatafilename,New_datafilename,Tablespace Type,Tablespace name
			return Final_result
		else:
			Final_result=os.system("python %s/Rename_Datafile_Without_Sudo_Brakes.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid,OldDatafilename,New_datafilename,Tablespace Type,Tablespace name
			return Final_result		
	def Datafile_Resize():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()
		Datafilename=raw_input("Please enter valid Datafile name/full path:")
		Datafile_Resize=raw_input("Please enter the new size of the datafile %s in MB:"%Datafilename)
		Tablespace_type=raw_input("Please enter the Tablespace Type[PERMANENT/TEMP/UNDO]:")
		Tablespace_name=raw_input("Please enter valid Tablespace name:")
		values=values+" "+DBName+" "+Datafilename+" "+Datafile_Resize
		+" "+Tablespace_type+" "+Tablespace_name
		if os.name == 'nt':
			Final_result=os.system("python %s\Resize_Datafile_Without_Sudo_Brakes.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid,datafilename,newsizeof datafile,Tablespace Type,Tablespacename
			return Final_result
		else:
			Final_result=os.system("python %s/Resize_Datafile_Without_Sudo_Brakes.py %s"%(dir12,values))    #Execution_Location,HostName,OSUser,OSPassword,Sid,datafilename,newsizeof datafile,Tablespace Type,Tablespacename
			return Final_result
			
	def one():
		print("""  
					________________________________________________
					|                                               |
					|       B.Database Administration               |
					|_______________________________________________|
					|                                               |
					|       1.Create Redo log group                 |
					|       2.Add Redo log                          |
					|       3.Drop Redo log group                   |
					|       4.Create SPfile                         |
					|       5.Create Pfile                          |
					|       6.Enable Archive Log                    |
					|       7.Disable Archive Log                   |
					|       8.Multiplex Controlfile                 |
					|       9.Recreating Controlfile                |
					|       10.Start Database                       |
					|       11.Stop Database                        |
					|       12.Shrink Table                         |
					|       13.Analyzing ORA-600 Errors             |
					|       14.House Keeping Trace files            |
					|       15.House Keeping Log files              |
					|       16.Add Datafile                         |
					|       17.Add Temp Datafile                    |
					|       18.Rename Datafile                      |
					|       19.Resize Datafile                      |
					|_______________________________________________| """)
		sub_process=int(input("Please select the task no. to execute. Eg. 1<ENTER>"))
		sub_switch = {
						1:Create_Redo_Logfile,
						2:Add_Member_To_Redo_Loggroup,
						3:Drop_Redo_Logfile,
						4:SPfile_Creation,
						5:Pfile_Creation,
						6:Enable_Archive_Log,
						7:Disable_Archive_log,
						8:Multiplex_ctlfile,
						9:Recreating_ctlfile,
						10:Start_DB,
						11:Stop_DB,
						12:Table_shrink,
						13:ORA_errors,
						14:Clean_auditfiles,
						15:Clean_tracefiles,
						16:Add_datafile,
						17:Add_tempfile,
						18:Datafile_rename,
						19:Datafile_Resize,
										}

		Final=sub_switch.get(sub_process,default)()
		return Final
		
		
		
		
		
	def Start_cluster():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		if os.name == 'nt':
			Final_result=os.system("python %s\Start_Cluster_Without_Sudo_Brakes.py %s"%(dir12,values))	#Execution_Location,HostName,OSUser,OSPassword
			return Final_result
		else:
			Final_result=os.system("python %s/Start_Cluster_Without_Sudo_Brakes.py %s"%(dir12,values))	#Execution_Location,HostName,OSUser,OSPassword
			return Final_result
		
	def Stop_cluster():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		if os.name == 'nt':
			Final_result=os.system("python %s\Stop_Cluster_Without_Sudo_Brakes.py %s"%(dir12,values))	#Execution_Location,HostName,OSUser,OSPassword
			return Final_result
		else:
			Final_result=os.system("python %s/Stop_Cluster_Without_Sudo_Brakes.py %s"%(dir12,values))	#Execution_Location,HostName,OSUser,OSPassword
			return Final_result	
	def Start_instance():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()
		values=values+" "+DBName
		if os.name == 'nt':
			Final_result=os.system("python %s\Start_Instance_Without_Sudo_Brakes.py %s"%(dir12,values))	#Execution_Location,HostName,OSUser,OSPassword,Sid	
			
			return Final_result
		else:
			Final_result=os.system("python %s/Start_Instance_Without_Sudo_Brakes.py %s"%(dir12,values))	#Execution_Location,HostName,OSUser,OSPassword,Sid	

			return Final_result	
	def Stop_instance():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()
		values=values+" "+DBName
		if os.name == 'nt':
			Final_result=os.system("python %s\Stop_Instance_Without_Sudo_Brakes.py %s"%(dir12,values))	#Execution_Location,HostName,OSUser,OSPassword,Sid	
			
			return Final_result
		else:
			Final_result=os.system("python %s\Stop_Instance_Without_Sudo_Brakes.py %s"%(dir12,values))	#Execution_Location,HostName,OSUser,OSPassword,Sid			
			
			return Final_result
	def Registering_DB():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()
		values=values+" "+DBName
		if os.name == 'nt':
		
			Final_result=os.system("python %s\Registering _Database_RC_Without_Sudo_Brakes.py %s"%(dir12,values))	#Execution_Location,HostName,OSUser,OSPassword,Sid
			
			return Final_result
		else:
			Final_result=os.system("python %s/Registering _Database_RC_Without_Sudo_Brakes.py %s"%(dir12,values))	#Execution_Location,HostName,OSUser,OSPassword,Sid
			
			return Final_result
			
	def Unregister_DB():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()
		values=values+" "+DBName
		if os.name == 'nt':
			Final_result=os.system("python %s\Unregister_DB_Without_Sudo_Brakes.py %s"%(dir12,values))	#Execution_Location,HostName,OSUser,OSPassword,Sid	
			
			return Final_result
		else:
			Final_result=os.system("python %s/Unregister_DB_Without_Sudo_Brakes.py %s"%(dir12,values))	#Execution_Location,HostName,OSUser,OSPassword,Sid		
			
			return Final_result
	def Start_listener():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()
		Listener_name=raw_input("Please enter valid Listner name to Start:")
		values=values+" "+Listener_name+" "+DBName
		if os.name == 'nt':
			Final_result=os.system("python %s\Start_Listener_test_Without_Sudo_Brakes.py %s"%(dir12,values))	#Execution_Location,HostName,OSUser,OSPassword,Sid	
			
			return Final_result
		else:
			Final_result=os.system("python %s/Start_Listener_test_Without_Sudo_Brakes.py %s"%(dir12,values))	#Execution_Location,HostName,OSUser,OSPassword,Sid		
			
			return Final_result
	def Stop_listener():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()
		Listener_name=raw_input("Please enter valid Listner name to Stop:")
		values=values+" "+Listener_name+" "+DBName
		if os.name == 'nt':
			Final_result=os.system("python %s\Stop_Listener_test_Without_Sudo_Brakes.py %s"%(dir12,values))	#Execution_Location,HostName,OSUser,OSPassword,Sid	
			
			return Final_result
		else:
			Final_result=os.system("python %s/Stop_Listener_test_Without_Sudo_Brakes.py %s"%(dir12,values))	#Execution_Location,HostName,OSUser,OSPassword,Sid
			
			return Final_result
	def Rebuilding_indexes():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()
		User_name=raw_input("Please enter the Database username  associated with index:")
		values=values+" "+DBName+" "+User_name
		if os.name == 'nt':
			Final_result=os.system("python %s\Rebuild_index_Without_Sudo_Brakes.py %s"%(dir12,values))	#Execution_Location,HostName,OSUser,OSPassword,Sid
			
			return Final_result
		else:
			Final_result=os.system("python %s/Rebuild_index_Without_Sudo_Brakes.py %s"%(dir12,values))	#Execution_Location,HostName,OSUser,OSPassword,Sid	
			
			return Final_result
	def Performing_reorg():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()
		Table_name=raw_input("Please enter the table to be shrunk:")
		values=values+" "+DBName+" "+Table_name
		if os.name == 'nt':
			Final_result=os.system("python %s\Shrink_Reorg_Without_Sudo_Brakes.py %s"%(dir12,values))	#Execution_Location,HostName,OSUser,OSPassword,Sid
			return Final_result
		else:
			Final_result=os.system("python %s/Shrink_Reorg_Without_Sudo_Brakes.py %s"%(dir12,values))	#Execution_Location,HostName,OSUser,OSPassword,Sid		
			return Final_result
			

	def two():
		print("""
					 _______________________________________________________
					|                                                       |
					|       C.Database Maintainance                         |
					|_______________________________________________________|
					|                                                       |
					|       1.Start Cluster                                 |
					|       2.Stop Cluster                                  |
					|       3.Start Instance                                |
					|       4.Stop Instance                                 |
					|       5.Registering Database in Recovery catalog      |
					|       6.Unregistering Database in Recovery catalog    |
					|       7.Start Listener                                |
					|       8.Stop Listener                                 |
					|       9.Rebuilding Indexes                            |
					|       10.Performing Re-org                            |
					|_______________________________________________________|	""")

		sub_process=int(input("Please select the task no. to execute. Eg. 1<ENTER>"))
		sub_switch = {
						1:Start_cluster,
						2:Stop_cluster,
						3:Start_instance,
						4:Stop_instance,
						5:Registering_DB,
						6:Unregister_DB,
						7:Start_listener,
						8:Stop_listener,
						11:Rebuilding_indexes,
						10:Performing_reorg,
						}
						
		Final=sub_switch.get(sub_process,default)()
		return Final
	def Create_user():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()
		DBusername=raw_input("Enter valid username to create:")
		DBuserpasswd=raw_input("Enter the password for the given DB user %s:"%DBusername)
		Tablespace_name=raw_input("Enter the valid Tablespacename:")
		values=values+" "+DBName+" "+DBusername+" "+DBuserpasswd+" "+Tablespace_name
		if os.name == 'nt':
			Final_result=os.system("python %s\Create_User_Without_Sudo_Brakes.py %s"%(dir12,values))	#Execution_Location,HostName,OSUser,OSPassword,Sid,Dbusername,password,Tablespacename
			return Final_result
		else:
			Final_result=os.system("python %s/Create_User_Without_Sudo_Brakes.py %s"%(dir12,values))	#Execution_Location,HostName,OSUser,OSPassword,Sid,Dbusername,password,Tablespacename	
			return Final_result
	def Drop_user():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()
		DBusername=raw_input("Enter valid username to delete:")
		Tablespace_name=raw_input("Enter the valid Tablespacename:")
		values=values+" "+DBName+" "+DBusername+" "+Tablespace_name
		if os.name == 'nt':
			Final_result=os.system("python %s\Drop_User_Without_Sudo_Brakes.py %s"%(dir12,values))	#Execution_Location,HostName,OSUser,OSPassword,Sid,Dbusername,password,Tablespacename
			return Final_result
		else:
			Final_result=os.system("python %s\Drop_User_Without_Sudo_Brakes.py %s"%(dir12,values))	#Execution_Location,HostName,OSUser,OSPassword,Sid,Dbusername,password,Tablespacename
			return Final_result
	def Create_profile():
		print("This sub_process is currently not integrated with Mainmenu")
	def Drop_profile():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()
		Profilename=raw_input("Please enter valid Profile name to delete:")
		values=values+" "+DBName+" "+Profilename
		if os.name == 'nt':
			Final_result=os.system("python %s\Drop_Profile_Without_Sudo_Brakes.py %s"%(dir12,values))	#Execution_Location,HostName,OSUser,OSPassword,Sid,profilename
			return Final_result
		else:
			Final_result=os.system("python %s\Drop_Profile_Without_Sudo_Brakes.py %s"%(dir12,values))	#Execution_Location,HostName,OSUser,OSPassword,Sid,profilename	
			return Final_result
	def Alter_privileges():
		values,dir12=common_input() #This contains (Hostname,Osusername,Ospassword,Exec_location)
		DBName=Input_DB()
		Privilege_type=raw_input("Please enter valid Privilage type [GRANT/REVOKE] :")
		Privilege_name=raw_input("Please enter valid Privilage name [Select/Insert/update/alter]:")
		Schema_name=raw_input("please enter valid Schema Name [Owner of the Object]")
		object_name=raw_input("Please enter valid Object name [Table/Schema/index] :")
		dbuser=raw_input("Please enter valid username to %s:"%Privilege_type)
		values=values+" "+DBName+" "+Privilege_type+" "+Privilege_name+" "+Schema_name+" "+Schema_name+" "+object_name+" "+dbuser
		if os.name == 'nt':
			Final_result=os.system("python %s\Alter_Previlages_Without_Sudo_Brakes.py %s"%(dir12,values))	#Execution_Location,HostName,OSUser,OSPassword,Sid,profilename	
			return Final_result
		else:
			Final_result=os.system("python %s\Alter_Previlages_Without_Sudo_Brakes.py %s"%(dir12,values))	#Execution_Location,HostName,OSUser,OSPassword,Sid,profilename	
			return Final_result
		
	def three():
		
		print(""" 
					 _______________________________________________
					|                                               |
					|       D.Database User Management              |
					|_______________________________________________|
					|                                               |
					|       1.Create User                           |
					|       2.Drop User                             |
					|       3.Create Profile                        |
					|       4.Drop Profile                          |
					|       5.Alter Privileges                      |
					|_______________________________________________|	""")
			
		sub_process=int(input("Please select the task no. to execute. Eg. 1<ENTER>"))
		sub_switch = {
						1:Create_user,
						2:Drop_user,
						3:Create_profile,
						4:Drop_profile,
						5:Alter_privileges,
						}
						
		Final=sub_switch.get(sub_process,default)()	
		return Final
			
			
			
			
	options = {"A":zero,
			   "B" : one,
			   "C" : two,
			   "D" : three}
	 

	print(options.get(process,default)())
except Exception, e:
	print "ExitCode: 10"
	print "ExitDesc: script failed due to: {0}".format(e)	
