#!/bin/bash
input(){
green=`tput setaf 2`
red=`tput setaf 1`
reset=`tput sgr0`
process="
				Welcome to Automation!!
		________________________________________________
		|						|
		|		\e[30;48;5;82m Main \e[30;48;5;82m Menu \e[0m			|
		|_______________________________________________|
		|						|
		|	A.Monitoring and Reporting 		|
		|	B.Database Administration		|
		|	C.Database Maintenance			|
		|	D.Database User Management		|
		|_______________________________________________|
"


echo -e "$process"
echo -n "Please Select the Process to run. Eg. A<ENTER>:"
read proc_code
proc_code="${proc_code,,}"




if [ $proc_code == "a" ]; then
  tasks_menu="
		________________________________________________
		|						|
		|	A.Monitoring and Reporting		|
		|_______________________________________________|
		|						|
		|	1.Schema Object details in a Tablespace	|
		|	${red}2.ASM Disk Space Report${reset}			|
		|	3.ASM and RAC Cluster Status		|
		|	4.DATAGUARD STATUS 			|
		|	5.Archive Destination Report 		|
		|	6.Capacity Planning Report		|
                |       7.ASM Disk Space Report        |
		|_______________________________________________|
"
    echo -e "$tasks_menu"
	echo "Type 0 and <ENTER> for Main Menu or Type exit and <ENTER> to exit the Automation script or"
    echo -n "Please select the task no. to execute. Eg. 1<ENTER>: "
    read task_code
    if [ $task_code -eq 1  ]; then
      common_input
	  #python $PWD/scripts/PRECHECKS_FRAMEWORK.py $ip $username $password $local_remote $dbname
      python $PWD/scripts/Schema_obj_details.py $local_remote $ip $username $password $dbname
    elif [ $task_code -eq 2  ]; then
      common_input
	  #python $PWD/scripts/PRECHECKS_FRAMEWORK.py $ip $username $password $local_remote $dbname
      python $PWD/scripts/ASM_Disk_Space.py $local_remote $ip $username $password $dbname
    elif [ $task_code -eq 3  ]; then
      common_input
	  #python $PWD/scripts/PRECHECKS_FRAMEWORK.py $ip $username $password $local_remote $dbname
      python $PWD/scripts/ASM_RAC_Cluster_Status_Without_Sudo_Brakes.py $local_remote $ip $username $password $dbname
    elif [ $task_code -eq 4  ]; then
      common_input
	  #python $PWD/scripts/PRECHECKS_FRAMEWORK.py $ip $username $password $local_remote $dbname
      python $PWD/scripts/Dataguard_Status.py $local_remote $ip $username $password $dbname

    elif [ $task_code -eq 5  ]; then
      common_input
	  echo -n "Please enter TRUE/FALSE for the FRA(Flash Recovery Area):"
      read FRA_Used
	  #python $PWD/scripts/PRECHECKS_FRAMEWORK.py $ip $username $password $local_remote $dbname
	  python $PWD/scripts/Archive_Space_Check.py $local_remote $ip $username $password $dbname $FRA_Used
    elif [ $task_code -eq 6  ]; then
      common_input
	  python $PWD/scripts/Capacity_Planning.py $local_remote $ip $username $password $dbname
    elif [ $task_code -eq 7  ]; then
	common_input
	 python $PWD/scripts/ASM_DiskSpace_check.py $local_remote $ip $username $password $dbname
    elif [ $task_code == "exit" ] || [ $task_code == "quit" ]; then
      exit_script
    else
     input
    fi






elif [ $proc_code == "b" ]; then
  tasks_menu="
		________________________________________________
		|						|
		|	B.Database Administration		|
		|_______________________________________________|
		|						|
		|	1.Create Redo log group			|
		|	2.Add Redo log				|
		|	3.Drop Redo log group			|
		|	4.Create SPfile				|
		|	5.Create Pfile				|
		|	6.Enable Archive Log			|
		|	7.Disable Archive Log			|
		|	8.Multiplex Controlfile			|
		|	9.Recreating Controlfile		|
		|	10.Start Database			|
		|	11.Stop Database			|
		|	12.Shrink Table				|
		|	13.Analyzing ORA-600 Errors		|
		|	14.House Keeping Audit files		|
		|	15.House Keeping Trace files		|
		|	16.Add Datafile				|
		|	17.Add Temp Datafile			|
		|	18.Rename Datafile			|
		|	19.Resize Datafile			|
		|_______________________________________________|
"
    echo -e "$tasks_menu"
	echo "Type 0 and <ENTER> for Main Menu or Type exit and <ENTER> to exit the Automation script or"
    echo -n "Please select the task no. to execute. Eg. 1<ENTER>: "
    read task_code
    if [ $task_code -eq 1  ]; then
      common_input
	  echo -n "Please enter Log group location with file:"
      read Log_grp_location_with_file
	  echo -n "Please enter the Log group size:"
      read Log_group_size
	  #python $PWD/scripts/PRECHECKS_FRAMEWORK.py $ip $username $password $local_remote $dbname
	  python $PWD/scripts/Create_Redo_Logfile_Without_Sudo_Brakes.py $local_remote $ip $username $password $dbname $Log_grp_location_with_file $Log_group_size
    elif [ $task_code -eq 2  ]; then
      common_input
	  echo -n "Please enter Log file location:"
      read Log_file_location
	  echo -n "Please enter Log group No.:"
      read Group_No
	  echo -n "Please enter the Log group size:"
      read Group_Size
	  #python $PWD/scripts/PRECHECKS_FRAMEWORK.py $ip $username $password $local_remote $dbname
	  python $PWD/scripts/Add_Member_To_Redo_Log_Group_Without_Sudo.py $local_remote $ip $username $password $dbname $Log_file_location $Group_No $Group_Size
    elif [ $task_code -eq 3  ]; then
      common_input
	  echo -n "Please enter Log group No.:"
      read Group_No
	  #python $PWD/scripts/PRECHECKS_FRAMEWORK.py $ip $username $password $local_remote $dbname
	  python $PWD/scripts/Drop_Redo_Log_File.py $local_remote $ip $username $password $dbname $Group_No
    elif [ $task_code -eq 4  ]; then
      common_input
	  #python $PWD/scripts/PRECHECKS_FRAMEWORK.py $ip $username $password $local_remote $dbname
	  python $PWD/scripts/SPfile_Without_Sudo.py $local_remote $ip $username $password $dbname
    elif [ $task_code -eq 5  ]; then
      common_input
	echo -n "If you want to create Pfile in Deafult Location Enter TRUE or else FALSE:"
	read defaultcase
	  #python $PWD/scripts/PRECHECKS_FRAMEWORK.py $ip $username $password $local_remote $dbname
	  python $PWD/scripts/Pfile_Test_Without_Sudo_Brakes_new.py $local_remote $ip $username $password $dbname $defaultcase
    elif [ $task_code -eq 6  ]; then
      common_input
	  #python $PWD/scripts/PRECHECKS_FRAMEWORK.py $ip $username $password $local_remote $dbname
	  python $PWD/scripts/Enable_Archive_Log_Test_Without_Sudo_Brakes.py $local_remote $ip $username $password $dbname
    elif [ $task_code -eq 7  ]; then
      common_input
	  #python $PWD/scripts/PRECHECKS_FRAMEWORK.py $ip $username $password $local_remote $dbname
	  python $PWD/scripts/Disable_Archive_Log_Test_Without_Sudo_Brakes.py $local_remote $ip $username $password $dbname
    elif [ $task_code -eq 8  ]; then
      common_input
	  echo -n "Please enter Control file path:"
      read ctl_file_path
	  #python $PWD/scripts/PRECHECKS_FRAMEWORK.py $ip $username $password $local_remote $dbname
	  python $PWD/scripts/Multiplexing_Controlfile_Without_Sudo_Brakes.py $local_remote $ip $username $password $dbname $ctl_file_path
    elif [ $task_code -eq 9  ]; then
      common_input
	  echo -n "Please enter Control file path for backup:"
      read ctl_file_path
	  #python $PWD/scripts/PRECHECKS_FRAMEWORK.py $ip $username $password $local_remote $dbname
	  python $PWD/scripts/Recreating_Controlfile_Without_Sudo_Brakes.py $local_remote $ip $username $password $dbname $ctl_file_path
    elif [ $task_code -eq 10  ]; then
      common_input
	  #python $PWD/scripts/PRECHECKS_FRAMEWORK.py $ip $username $password $local_remote $dbname
	  python $PWD/scripts/Start_DB_Without_Sudo_Brakes.py $local_remote $ip $username $password $dbname
    elif [ $task_code -eq 11  ]; then
      common_input
	  #python $PWD/scripts/PRECHECKS_FRAMEWORK.py $ip $username $password $local_remote $dbname
	  python $PWD/scripts/Stop_DB_Without_Sudo_Brakes.py $local_remote $ip $username $password $dbname

    elif [ $task_code -eq 12  ]; then
      common_input
	  echo -n "Please enter valid Table name:"
      read tablespacename
	  #python $PWD/scripts/PRECHECKS_FRAMEWORK.py $ip $username $password $local_remote $dbname
	  python $PWD/scripts/Shrink_Reorg_Without_Sudo_Brakes.py $local_remote $ip $username $password $dbname $tablespacename
    elif [ $task_code -eq 13  ]; then
      common_input
	  #python $PWD/scripts/PRECHECKS_FRAMEWORK.py $ip $username $password $local_remote $dbname
	  python $PWD/scripts/Analysing_ORA_Errors_Without_Sudo_Brakes.py $local_remote $ip $username $password $dbname
    elif [ $task_code -eq 14  ]; then
#      echo "This option is currently not available. Please select another option from Main Menu"
	 common_input
	python $PWD/scripts/Cleaning_AuditFiles.py $local_remote $ip $username $password
    elif [ $task_code -eq 15  ]; then
      echo " Enter the IPaddress:"
	read hostname
      echo "Enter Execution Location:"
	read Exec_loc
      echo "Enter OS username:"
	read OSuser
      echo "Enter the password for user $OSuser:"
	read OSpass
	python $PWD/scripts/Cleaning_Tracefiles_new_13July2018.py $Exec_loc $hostname $OSuser $OSpass

    elif [ $task_code -eq 16  ]; then
      common_input

	#  echo -n "Please enter valid Datafile name:"
  #    read datafilename
	  echo -n "Please enter valid Tablespace name:"
      read tablespacename
#	  echo -n "Please enter the size of the datafile $datafilename in MB:"
 #     read size
#	  echo -n "Please enter the option for Autoextend [True/False]:"
 #     read autoextend
	  #python $PWD/scripts/PRECHECKS_FRAMEWORK.py $ip $username $password $local_remote $dbname 
	  python $PWD/scripts/Add_Datafile_Without_Sudo_Brakes.py $local_remote $ip $username $password $dbname $tablespacename 

    elif [ $task_code -eq 17  ]; then
      common_input
	  echo -n "Please enter valid Datafile name/full path:"
      read datafilename
	  echo -n "Please enter valid Tablespace name:"
      read tablespacename
	  echo -n "Please enter the size of the datafile $datafilename in MB:"
      read size
	  echo -n "Please enter the option for Autoextend [True/False]:"
      read autoextend
	  #python $PWD/scripts/PRECHECKS_FRAMEWORK.py $ip $username $password $local_remote $dbname
	  python $PWD/scripts/Add_Tempfile_Without_Sudo_Brakes.py $local_remote $ip $username $password $dbname $datafilename $tablespacename $size $autoextend
    elif [ $task_code -eq 18  ]; then
      common_input
	  echo -n "Please enter the Datafile name/full path to rename:"
      read OldDatafile
	  echo -n "Please enter the new name/path for the datafile $datafilename:"
      read NewDatafilePath
	  echo -n "Please enter the Tablespace Type[PERMANENT/TEMP/UNDO]:"
      read TBSType
	  echo -n "Please enter valid Tablespace name:"
      read tablespacename
	  #python $PWD/scripts/PRECHECKS_FRAMEWORK.py $ip $username $password $local_remote $dbname
	  python $PWD/scripts/Rename_Datafile_Without_Sudo_Brakes.py $local_remote $ip $username $password $dbname $OldDatafile $NewDatafilePath $TBSType $tablespacename
    elif [ $task_code -eq 19  ]; then
      common_input
	  echo -n "Please enter valid Datafile name/full path:"
      read datafilename
	  echo -n "Please enter the size of the datafile $datafilename in MB:"
      read size
	  echo -n "Please enter the Tablespace Type[PERMANENT/TEMP/UNDO]:"
      read TBSType
	  echo -n "Please enter valid Tablespace name:"
      read tablespacename
	  #python $PWD/scripts/PRECHECKS_FRAMEWORK.py $ip $username $password $local_remote $dbname
	  python $PWD/scripts/Resize_Datafile_Without_Sudo_Brakes.py $local_remote $ip $username $password $dbname $datafilename $size $TBSType $tablespacename 


    elif [ $task_code == "exit" ] || [ $task_code == "quit" ]; then
      exit_script

    else
     input
    fi




elif [ $proc_code == "c" ]; then
  tasks_menu="
		________________________________________________________
		|							|
		|	C.Database Maintainance				|
		|_______________________________________________________|
		|							|
		|	1.Start Cluster					|
		|	2.Stop Cluster					|
		|	3.Start Database				|
		|	4.Stop Database				|
		|	5.Start Instance				|
		|	6.Stop Instance					|
		|	${red}7.Registering Database in Recovery catalog${reset}	|
		|	8.Unregistering Database in Recovery catalog	|
		|	9.Start Listener				|
		|	10.Stop Listener				|
		|	11.Rebuilding Indexes				|
		|	12.Performing Re-org				|
		|_______________________________________________________|
"
    echo -e "$tasks_menu"
	echo "Type 0 and <ENTER> for Main Menu or Type exit and <ENTER> to exit the Automation script or"
    echo -n "Please select the task no. to execute. Eg. 1<ENTER>: "
    read task_code
    if [ $task_code -eq 1  ]; then
      common_input
	  python $PWD/scripts/Start_Cluster_Without_Sudo_Brakes.py $local_remote $ip $username $password
    elif [ $task_code -eq 2  ]; then
      common_input
	  python $PWD/scripts/Stop_Cluster_Without_Sudo_Brakes.py $local_remote $ip $username $password
    elif [ $task_code -eq 3  ]; then
      common_input
	  #python $PWD/scripts/PRECHECKS_FRAMEWORK.py $ip $username $password $local_remote $dbname 
	  python $PWD/scripts/Start_DB_Without_Sudo_Brakes.py $local_remote $ip $username $password $dbname

    elif [ $task_code -eq 4  ]; then
      common_input
	  #python $PWD/scripts/PRECHECKS_FRAMEWORK.py $ip $username $password $local_remote $dbname 
	  python $PWD/scripts/Stop_DB_Without_Sudo_Brakes.py $local_remote $ip $username $password $dbname
    elif [ $task_code -eq 5  ]; then
      common_input
	  echo -n "Please enter valid Database Instance name to Start:"
      read InstanceName
	  python $PWD/scripts/Start_Instance_Without_Sudo_Brakes.py $local_remote $ip $username $password $InstanceName $dbname
    elif [ $task_code -eq 6  ]; then
      common_input
	  echo -n "Please enter valid Database Instance name to Stop:"
      read InstanceName
	  python $PWD/scripts/Stop_Instance_Without_Sudo_Brakes.py $local_remote $ip $username $password $InstanceName $dbname
    elif [ $task_code -eq 7  ]; then
      common_input
	  python $PWD/scripts/Registering _Database_RC_Without_Sudo_Brakes.py $local_remote $ip $username $password $dbname
    elif [ $task_code -eq 8  ]; then
      common_input
	  python $PWD/scripts/Unregister_DB_Without_Sudo_Brakes.py $local_remote $ip $username $password $dbname
    elif [ $task_code -eq 9  ]; then
      common_input
	  
	  echo -n "Please enter valid Listner name to Start:"
      read listner
	  #python $PWD/scripts/PRECHECKS_FRAMEWORK.py $ip $username $password $local_remote $dbname 
	  python $PWD/scripts/Start_Listener_test_Without_Sudo_Brakes.py $local_remote $ip $username $password $listner $dbname
	  
    elif [ $task_code -eq 10  ]; then
      common_input

	  echo -n "Please enter valid Listner name to Stop:"
      read listner
	  #python $PWD/scripts/PRECHECKS_FRAMEWORK.py $ip $username $password $local_remote $dbname 
	  python $PWD/scripts/Stop_Listener_test_Without_Sudo_Brakes.py $local_remote $ip $username $password $listner $dbname

    elif [ $task_code -eq 11  ]; then
      common_input
	echo -n "Please enter the Database username  associated with index"
     read dbusername
	  python $PWD/scripts/Rebuild_index_Without_Sudo_Brakes.py $local_remote $ip $username $password $dbname $dbusername
    elif [ $task_code -eq 12  ]; then
      common_input
	echo -n "Please enter the table to be shrunk"
     read tablename
#	  python $PWD/scripts/Shrink_Reorg_Without_Sudo_Brakes.py $local_remote $ip $username $password $dbname
	  python $PWD/scripts/Shrink_Reorg_Without_Sudo_Brakes.py $local_remote $ip $username $password $dbname $tablename
	
    elif [ $task_code == "exit" ] || [ $task_code == "quit" ]; then
      exit_script
    else
     input
    fi





elif [ $proc_code == "d" ]; then
  tasks_menu="
		________________________________________________
		|						|
		|	D.Database User Management		|
		|_______________________________________________|
		|						|
		|	1.Create User				|
		|	2.Drop User				|
		|	3.Create Profile			|
		|	4.Drop Profile				|
		|	5.Alter Privileges			|
		|_______________________________________________|
"
    echo -e "$tasks_menu"
	echo "Type 0 and <ENTER> for Main Menu or Type exit and <ENTER> to exit the Automation script or"
    echo -n "Please select the task no. to execute. Eg. 1<ENTER>: "
    read task_code

    if [ $task_code -eq 1  ]; then
      common_input
	  echo -n "Please enter valid User name to create:"
      read dbuser
	  echo -n "Please enter password for the given Database user $dbuser:"
	  read -s dbuserpass
	  echo
	  echo -n "Please enter valid Tablespace name:"
      read tablespacename
	  python $PWD/scripts/Create_User_Without_Sudo_Brakes.py $local_remote $ip $username $password $dbname $dbuser $dbuserpass $tablespacename
	  
    elif [ $task_code -eq 2  ]; then
      common_input
	  echo -n "Please enter valid User name to delete:"
      read dbuser
	  echo -n "Please enter valid Tablespace name:"
      read tablespacename
	  python $PWD/scripts/Drop_User_Without_Sudo_Brakes.py $local_remote $ip $username $password $dbname $dbuser $tablespacename
    elif [ $task_code -eq 3  ]; then
      common_input
    elif [ $task_code -eq 4  ]; then
      common_input
	  echo -n "Please enter valid Profile name to delete:"
      read dbprofile_name
	  python $PWD/scripts/Drop_Profile_Without_Sudo_Brakes.py $local_remote $ip $username $password $dbname $dbprofile_name
    elif [ $task_code -eq 5  ]; then
      common_input
	 echo -n "Please enter valid Privilage type [GRANT/REVOKE] :"
      read priv_type
	 echo -n "Please enter valid Privilage name [Select/Insert/update/alter] :"
      read priv_name
	 echo -n "Please enter valid Schema Name [Owner of the Object] :"
      read schema_name
	 echo -n "Please enter valid Object name [Table/Schema/index] :"
      read object_name
	 echo -n "Please enter valid name to $priv_type :"
      read dbuser
	  python $PWD/scripts/Alter_Previlages_Without_Sudo_Brakes.py $local_remote $ip $username $password $dbname $priv_type $priv_name $schema_name $object_name $dbuser
    elif [ $task_code == "exit" ] || [ $task_code == "quit" ]; then
      exit_script
    else
     input
    fi



elif [ $proc_code == "exit" ] || [ $proc_code == "quit" ]; then
exit_script
else
input
fi
}

function valid_ip()
{
    local  ip=$1
    local  stat=1

    if [[ $ip =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        OIFS=$IFS
        IFS='.'
        ip=($ip)
        IFS=$OIFS
        [[ ${ip[0]} -le 255 && ${ip[1]} -le 255 \
            && ${ip[2]} -le 255 && ${ip[3]} -le 255 ]]
        stat=$?
    fi
    return $stat
}



common_input(){
ip_input
check_local $ip
dbname_input
#orahome_input
username_inputs
input_password
}

ip_input(){
echo -n "Please enter valid IP Address(s) or Hostname(s) to connect:"

read ip

if [ $ip == "exit" ] || [ $ip == "quit" ]; then
  exit_script
  
elif [ $ip == "0" ]; then
    input

elif [ ${#ip} -ge 3 ]; then
  if [[ $ip = *"."* ]]; then
    if valid_ip $ip; then
      return $?
    else
	  echo "Invalid IP or Hostname"
      ip_input
    fi
  else

    if [[ $ip =~ [^(a-zA-Z_0-9\s)] ]]; then
      ip_input
    fi
  fi


else
  echo "Invalid IP or Hostname"
  ip_input
fi



}

dbname_input(){
echo -n "Please enter valid Database name to connect:"
read dbname
if [ $dbname == "exit" ] || [ $dbname == "quit" ]; then
  exit_script
  
elif [ $dbname == "0" ]; then
    input
	
elif [[ $dbname =~ [^(a-zA-Z_0-9\s)] ]]; then
  dbname_input

fi

}

orahome_input(){
echo -n "Please enter valid ORA_HOME for the given Database name (Absolute Path):"
read orahome

if [ $orahome == "exit" ] || [ $orahome == "quit" ]; then
  exit_script
  
elif [ $orahome == "0" ]; then
    input

elif [[ $orahome = /* ]]; then
  return $?
else
  echo "Invalid path"
  orahome_input
fi
}

username_inputs(){

echo -n "Please enter valid Username to connect:"
read username

if [ $username == "exit" ] || [ $username == "quit" ]; then
  exit_script
  
elif [ $username == "0" ]; then
    input

elif [[ $username =~ [^(a-zA-Z_0-9\s)] ]]; then
  username_inputs
#else
  #echo -n "User $username is a sudo user. [Yes or No]:"
  #read yes_no
  #yes_no="${yes_no,,}"
  #if [ $yes_no != "yes" ] || [ $yes_no != "y" ]; then
  #  sudo_login="TRUE"
  #else
  #  sudo_login="FALSE"
  #fi
  

fi

}
input_password(){

echo -n "Please enter password for the given Username $username:"
read -s password

echo

}

check_local(){
local_ip="$(ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1')"
local_hostname=hostname
if [ $local_ip == $1 ]; then
    local_remote="LOCAL"
elif [ $local_hostname == $1 ]; then
    local_remote="LOCAL"
else
    local_remote="REMOTE"
fi

}

exit_script(){
echo "Thank you for using Automation!! Bye."
exit 0
}


input

