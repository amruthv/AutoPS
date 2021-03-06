processNumber = 61000
RESERVEDPROCESS = 60000

class ConfigInformation(object):
    def __init__(self, processMap, fileMap, whitelist, chroot):
        self.processMap = processMap
        self.fileMap = fileMap
        self.whitelist = whitelist
        self.chroot = chroot
class Node(object):
    def __init__(self, name):
        self.name = name
        self.reads = []
        self.writes = []
        self.executes = []
    def addToReads(self, node):
        self.reads.append(node)
    def addToWrites(self, node):
        self.writes.append(node)
    def addToExecutes(self, node):
        self.executes.append(node)
    def __hash__(self):
        return self.name.__hash__()
    def __repr__(self):
        return self.__str__()
class FileNode(Node):
    def __init__(self, name):
        super(FileNode, self).__init__(name)
    def __str__(self):
        return "name: {0}, reads: {1}, writes: {2}, executes:{3}".format(self.name, self.shouldStart, ','.join(node.name for node in self.reads), ','.join(node.name for node in self.writes), ','.join(node.name for node in self.executes))


class ProcessNode(Node):
    def __init__(self, name, procNum, args, shouldStart):
        super(ProcessNode, self).__init__(name)
        self.processNumber = procNum
        self.args = args
        self.shouldStart = shouldStart
    def __hash__(self):
        return self.processNumber
    def __str__(self):
        return "name: {0}, processNumber: {1}".format(self.name, self.processNumber)
        return "name: {0}, processNumber: {1}, args: {2} shouldStart: {3},  reads: {4}, writes: {5}, executes:{6}".format(self.name, self.processNumber, self.args, self.shouldStart, ','.join(node.name for node in self.reads), ','.join(node.name for node in self.writes), ','.join(node.name for node in self.executes))

def getChroot(lines):
    chrootPrefix = "Chroot: "
    chrootLines = [line.strip() for line in lines if line.startswith(chrootPrefix)]
    assert(len(chrootLines) == 0 or len(chrootLines) == 1)
    if len(chrootLines) == 0:
        return ''
    chroot = chrootLines[0][len(chrootPrefix):]
    return chroot

def getWhitelist(lines):
    whitelistPrefix = "Whitelist: "
    whitelistlines = [line.strip() for line in lines if line.startswith("Whitelist: ")]
    assert len(whitelistlines) == 0 or len(whitelistlines) == 1
    if len(whitelistlines) == 0:
        return []
    whitelist = [x.strip() for x in whitelistlines[0][len(whitelistPrefix):].split(',')]
    return whitelist

def processConfig(fileName):
    f = open(fileName, 'r')
    lines = [line.strip() for line in f.readlines() if line != '\n']
    whitelist = getWhitelist(lines)
    chroot = getChroot(lines)
    processMap, fileMap = processGroups(lines) 
    return ConfigInformation(processMap, fileMap, whitelist, chroot)

def processGroups(lines):
    groupChunks = [i for i, line in enumerate(lines) if line.startswith('Group')]
    processMap = {}
    fileMap = {}
    for i, lineNum in enumerate(groupChunks):
        if i == len(groupChunks) - 1:
            linesForGroup = lines[lineNum:]
        else:
            linesForGroup = lines[lineNum:groupChunks[i+1]]
        processLinesForGroup(linesForGroup, processMap, fileMap)
    return processMap, fileMap

# HACK HACK ASSUME THEY HAVE REQUESTED PROCESS NUMBERS ENTRIES BEFORE THE ONES THAT CAN BE ASSIGNED ANY VALUE THIS WAY WE ASSUME THERES NO COLLISION
def processLinesForGroup(linesForGroup, processMap, fileMap):
    global processNumber
    runAsPrefix = "Run as: "
    runAs = None
    if linesForGroup[1].startswith(runAsPrefix):
        runAs = int(linesForGroup[1][len(runAsPrefix):])
    fileChunks = [i for i, line in enumerate(linesForGroup) if line.startswith("Process:")]
    for i, lineNum in enumerate(fileChunks):
        if i == len(fileChunks) - 1:
            linesForFile = linesForGroup[lineNum:]
        else:
            linesForFile = linesForGroup[lineNum:fileChunks[i+1]]
        # increment global processNumber reference until it is not being used by some requested process
        while len([True for processNode in processMap.values() if processNode.processNumber == processNumber]) != 0:
            processNumber += 1
        processLinesForFile(linesForFile, processMap, fileMap)
    if runAs is None:
        processNumber += 1
    else:
        justAdded = [processNode for processNode in processMap.values() if processNode.processNumber == processNumber]
        for node in justAdded:
            del processMap[(node.processNumber, node.name)]
            node.processNumber = runAs
            processMap[(node.processNumber, node.name)] = node
def processLinesForFile(linesForFile, processMap, fileMap):
    global processNumber

    processName = None
    shouldStart = False
    args = []
    reads = []
    writes = []
    executes = []
    processPrefix = "Process: "
    argsPrefix = "Args: "
    readsPrefix = "Reads: "
    writesPrefix = "Writes: "
    executesPrefix = "Executes: "
    for line in linesForFile:
        if line.startswith(processPrefix):
            processName = line[len(processPrefix):]
        elif line.startswith(argsPrefix):
            # note this doesn't work with escaped spaces..
            args = line[len(argsPrefix):].strip().split(' ')
        elif line.startswith(readsPrefix):
            reads = [ln.strip() for ln in line[len(readsPrefix):].split(',')]
        elif line.startswith(writesPrefix):
            writes = [ln.strip() for ln in line[len(writesPrefix):].split(',')]
        elif line.startswith(executesPrefix):
            executes = [ln.strip() for ln in line[len(executesPrefix):].split(',')]
        elif line.strip() == "Start":
            shouldStart = True
    processNode = ProcessNode(processName, processNumber, args, shouldStart)
    for fileToRead in reads:
        readFileNode = fileMap.get(fileToRead, Node(fileToRead))
        readFileNode.addToReads(processNode)
        fileMap[fileToRead] = readFileNode
        processNode.addToReads(readFileNode)

    for fileToWrite in writes:
        writeFileNode = fileMap.get(fileToWrite, Node(fileToWrite))
        writeFileNode.addToWrites(processNode)
        fileMap[fileToWrite] = writeFileNode
        processNode.addToWrites(writeFileNode)
    for fileToExecute in executes:
        executeFileNode = fileMap.get(fileToExecute, Node(fileToExecute))
        executeFileNode.addToExecutes(processNode)
        fileMap[fileToExecute] = executeFileNode
        processNode.addToExecutes(executeFileNode)
    processMap[(processNode.processNumber, processNode.name)] = processNode

if __name__ == '__main__':
    configInfo =  processConfig('config.txt')
    print configInfo.chroot
    #processMap = configInfo.processMap
    #for name in processMap.keys():
    #    print processMap[name]
