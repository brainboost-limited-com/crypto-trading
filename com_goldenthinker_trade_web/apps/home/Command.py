import subprocess

class Command():
    
    def execute(command):
    	try:
		    batcmd=command
		    return str(subprocess.check_output(batcmd, shell=True,text=True))
	    except:
		    Logger.log("Error executing commmand :" + str(command),telegram=True)