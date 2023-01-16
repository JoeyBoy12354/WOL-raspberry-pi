import subprocess  
  
def ping(modules):
    
    # The command you want to execute   
    cmd = 'python -m pip install'
  
    # send one packet of data to the host 
    # this is specified by '-c 1' in the argument list 
    outputlist = []
    # Iterate over all the modules in the list and ping each module
    for module in modules:
        temp = subprocess.Popen([cmd, '-c 1', module], stdout = subprocess.PIPE) 
        # get the output as a string
        output = str(temp.communicate()) 
    # store the output in the list
        outputlist.append(output)
    return outputlist
  
if __name__ == '__main__': 
    
    # Get the list of modules from the text file
    modules = list(open('modules.txt'))
    # Iterate over all the modules that we read from the text file
    # and remove all the extra lines. This is just a preprocessing step
    # to make sure there aren't any unnecessary lines.
    for i in range(len(modules)):
        modules[i] = modules[i].strip('\n')
    outputlist = ping(modules) 
    
    # Uncomment the following lines to print the output of successful modules
    # print(outputlist)