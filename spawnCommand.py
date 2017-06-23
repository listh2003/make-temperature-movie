#!/usr/bin/env python
'''
Created on Jul 18, 2013

@author: jeremy.walton@metoffice.gov.uk
'''

import subprocess
    
class SpawnCommand():
    
    ''' Spawns a shell command and prints any output, if requested (the default is not to).  
    If a remote machine name is supplied, the command is executed via an ssh connection, 
    otherwise, (the default), the command is executed on the local machine. '''

    def __init__(self, cmd, machine = 'local', printOutput = False):
        
        ''' Spawn a command, and print any output, if requested.'''
    
        if machine != 'local':
            cmd = 'ssh ' + machine + ' ' + cmd
            
        # The command will be executed using the bash shell.  
        command = ['bash', '-c', cmd]

        try:
            # Execute the subprocess, then buffer all the output and error messages.                
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (stdout, stderr) = proc.communicate()
            
            if proc.wait() != 0:
                raise UserWarning("Unable to execute:\n"+cmd+"\nError code = "+str(proc.wait()))
            
            if printOutput:
                # Print all the output, suitably delineated.
                if stderr:
                    for err in stderr.split("\n"):
                        if len(err) > 0:
                            print err
                            
                if stdout: 
                    print "-----"
                    for line in stdout.split("\n"):
                        if len(line) > 0:
                            print line
        
        except OSError as exception:
            raise UserWarning("Unable to execute:\n"+cmd+"\nError code = "+str(exception))   
 
 
if __name__ == "__main__":
    
    SpawnCommand("ls")
    SpawnCommand("ls", machine="puma.nerc.ac.uk")
