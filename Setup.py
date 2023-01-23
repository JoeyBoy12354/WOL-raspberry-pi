import os
  
def getModules(modules):
    outputlist = []
    # Iterate over all the modules in the list and install each module
    for module in modules:
        print(" ");
        print("Getting: ",module)
        response = os.system('pip install ' + module)
        print("Response: ",response)
        # get the output as a string
    return
  
if __name__ == '__main__': 
    
    # Get the list of modules from the text file
    modules = list(open('modules.txt'))
    # Iterate over all the modules that we read from the text file
    # and remove all the extra lines. This is just a preprocessing step
    # to make sure there aren't any unnecessary lines.
    for i in range(len(modules)):
        modules[i] = modules[i].strip('\n')
    getModules(modules) 
    
