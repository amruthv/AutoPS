import os
import parseConfig
import subprocess

RESERVEDPROCESS = 60000

def nullPermissions(d):
    for root, dirs, files in os.walk(d):
        os.chmod(root, 0o000)
        for f in files:
            os.chmod(root + "/" + f, 0o000)

def setDefaultOwnerAndGroup(d):
    for root, dirs, files in os.walk(d):
        os.chown(root, RESERVEDPROCESS, RESERVEDPROCESS)
        for f in files:
            os.chown(root + "/" + f, RESERVEDPROCESS, RESERVEDPROCESS)

def setPermissions(configName, dirName):
    processMap, fileMap = parseConfig.buildGraph(configName)
    processIds = set()
    # add reserved value for group and user
    subprocess.call("useradd", str(RESERVEDPROCESS))
    subprocess.call("groupadd", str(RESERVEDPROCESS))

    # add users and groups of the processes
    for processNode in processMap.items():
        processIds.add(processNode.processNumber)
    for processId in processIds:
        subprocess.call("useradd", str(processId))
        subprocess.call("groupadd", str(processId))

    nullPermissions(dirName)
    setDefaultOwnerAndGroup(dirname)

    # go through and set acls for everything
    for fileName in fileMap:
        setPermissions(fileMap[fileName])

def setFilePermissions(fileNode):
    #aggregate permissions by calling process (process p might be in reads and writes) 
    processPermissions = {}
    for readingProcess in fileNode.reads:
        processPermissions[readingProcess.processNumber] = 'r'
    for writingProcess in fileNode.writes:
        currPermissions = processPermissions.get(writingProcess.processNumber. '')
        processPermissions[writingProcess.processNumber] = currPermissions + 'w'
    for executingProcess in fileNode.executes:
        currPermissions = processPermissions.get(executingProcess.processNumber. '')
        processPermissions[executingProcess.processNumber] = currPermissions + 'x'
    
    # actually invoke acl
    for processNum, permissions in processPermissions.items():
        subprocess.call("setfacl", "-m" "user:{0}:{1}".format(processNumber, permissions), fileNode.name)


setPermissions("config.txt", "/jail")


    


# nullPermissions('/Users/amruthvenkatraman/Dropbox/MIT/Senior Year/6.858')

#setPermissions('config.txt')
