import os
import parseConfig
import subprocess

RESERVEDPROCESS = 60000

def chroot(path):
    os.chroot(path)

def matchesWhitelist(prefix, whitelist, toCheck):
    return any(map(lambda whitelisted: toCheck.startswith(prefix + whitelisted), whitelist))
  
def nullPermissions(prefix, whitelist):
    print whitelist
    for root, dirs, files in os.walk(prefix):
        print root + '/'
        if matchesWhitelist(prefix, whitelist, root + "/"):
            continue 
        os.chmod(root, 0o000)
        for f in files:
            if matchesWhitelist(prefix, whitelist, root + "/" + f):
                continue
            if f == 'zook.conf':
                os.chmod(root + "/" + f, 0o777)
            else:
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

def setPermissions(configName, prefix):
    configInfo = parseConfig.processConfig(configName)
    processMap, fileMap, whitelist = configInfo.processMap, configInfo.fileMap, configInfo.whitelist
    processIds = set()
    # add reserved value for group and user
    subprocess.call(["useradd", str(RESERVEDPROCESS)])
    subprocess.call(["groupadd", str(RESERVEDPROCESS)])

    # add users and groups of the processes
    for processNode in processMap.values():
        processIds.add(processNode.processNumber)
    for processId in processIds:
        subprocess.call(["useradd", str(processId)])
        subprocess.call(["groupadd", str(processId)])

    nullPermissions(prefix, whitelist)
    setDefaultOwnerAndGroup(prefix, whitelist)

    # go through and set acls for everything
    for fileNode in fileMap.values():
        setFilePermissions(prefix, fileNode)
    
    #chroot
    chroot(prefix)
    
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
        print 'pid=',pid
        os.chmod(processNode.name, 0o100)
        os.setgid(processNode.processNumber)
        os.setuid(processNode.processNumber)
        print 'uid of process:', os.getuid()
        print "trying to run: " + processNode.name 
        os.execv(processNode.name, [processNode.name] + processNode.args)
prefix = "/jail/"
setPermissions(prefix + "AutoPS/config.txt", prefix)
