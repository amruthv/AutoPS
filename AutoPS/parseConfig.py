processNumber = 61000
RESERVEDPROCESS = 60000


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


def buildGraph(fileName):
    f = open(fileName, 'r')
    lines = [line.strip() for line in f.readlines() if line != '\n']
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
        #print justAdded
        #print len(justAdded)
        for node in justAdded:
            #print 'before setting to runAs', node.processNumber
            del processMap[(node.processNumber, node.name)]
            node.processNumber = runAs
            processMap[(node.processNumber, node.name)] = node
            #print 'after setting to runAs', node.processNumber
    print processMap 
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


processMap, fileMap =  buildGraph('config.txt')
for name in processMap.keys():
    print processMap[name]
