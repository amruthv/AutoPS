import os
import parseConfig
import subprocess

RESERVEDPROCESS = 60000

def chrootIntoDir(path):
    os.chroot(path)

def matchesWhitelist(prefix, whitelist, toCheck):
    return any(map(lambda whitelisted: toCheck.startswith(prefix + whitelisted), whitelist))
  
def nullPermissions(prefix, whitelist):
    for root, dirs, files in os.walk(prefix):
        if matchesWhitelist(prefix, whitelist, root + "/"):
            continue 
        if root != prefix:
            os.chmod(root, 0o000)
        for f in files:
            if matchesWhitelist(prefix, whitelist, root + "/" + f):
                continue
            os.chmod(root + "/" + f, 0o000)

def setDefaultOwnerAndGroup(prefix, whitelist):
    for root, dirs, files in os.walk(prefix):
        if matchesWhitelist(prefix, whitelist, root + "/"):
            continue  
        os.chown(root, RESERVEDPROCESS, RESERVEDPROCESS)
        for f in files:
            if matchesWhitelist(prefix, whitelist, root + "/" + f):
                continue
            os.chown(root + "/" + f, RESERVEDPROCESS, RESERVEDPROCESS)

def setPermissions(configInfo):
    processMap, fileMap, whitelist, chroot = configInfo.processMap, configInfo.fileMap, configInfo.whitelist, configInfo.chroot
    processIds = set()
    # add reserved value for group and user
    subprocess.call(["useradd", "-u", str(RESERVEDPROCESS), str(RESERVEDPROCESS)])
    subprocess.call(["groupadd", "-g", str(RESERVEDPROCESS), str(RESERVEDPROCESS)])

    # add users and groups of the processes
    for processNode in processMap.values():
        processIds.add(processNode.processNumber)
    for processId in processIds:
        subprocess.call(["useradd", "-u", str(processId), str(processId)])
        subprocess.call(["groupadd", "-g", str(processId), str(processId)])

    if chroot != '':
        prefix = chroot
    else:
        # if no chroot go up one directory for nulling out permissions since we are in AutoPS directory
        prefix = './../'

    nullPermissions(prefix, whitelist)
    setDefaultOwnerAndGroup(prefix, whitelist)

    # go through and set acls for everything
    for fileNode in fileMap.values():
        setFilePermissions(prefix, fileNode)

    #chroot
    chrootIntoDir(chroot)
    
    if chroot != '':
        os.chdir('/')
    else:
        os.chdir('./..')
    
    # spawn the processes
    for processNode in processMap.values():
        startProcess(processNode)        

def setFilePermissions(prefix, fileNode):
    #aggregate permissions by calling process (process p might be in reads and writes) 
    processPermissions = {}
    for readingProcess in fileNode.reads:
        processPermissions[readingProcess.processNumber] = 'r'
    for writingProcess in fileNode.writes:
        currPermissions = processPermissions.get(writingProcess.processNumber, '')
        processPermissions[writingProcess.processNumber] = currPermissions + 'w'
    for executingProcess in fileNode.executes:
        currPermissions = processPermissions.get(executingProcess.processNumber, '')
        processPermissions[executingProcess.processNumber] = currPermissions + 'x'
    
    # actually invoke acl
    for processNum, permissions in processPermissions.items():
        subprocess.call(["sudo", "setfacl", "-m" "user:{0}:{1}".format(processNum, permissions), prefix + fileNode.name])

def startProcess(processNode):
    if processNode.shouldStart:
        pid = os.fork()
        if not pid == 0:
            return
        os.setgid(processNode.processNumber)
        os.setuid(processNode.processNumber)
        os.execv(processNode.name, [processNode.name] + processNode.args)

configInfo = parseConfig.processConfig('config.txt')
setPermissions(configInfo)
