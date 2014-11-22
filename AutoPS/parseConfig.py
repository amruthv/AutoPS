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

class FileNode(Node):
    def __init__(self, name):
        super(FileNode, self).__init__(name)
    def __str__(self):
        return "name: {0}, reads: {1}, writes: {2}, executes:{3}".format(self.name, ','.join(node.name for node in self.reads), ','.join(node.name for node in self.writes), ','.join(node.name for node in self.executes))


class ProcessNode(Node):
    def __init__(self, name, procNum):
        super(ProcessNode, self).__init__(name)
        self.processNumber = procNum
    def __hash__(self):
        return self.processNumber
    def __str__(self):
        return "name: {0}, processNumber: {1}, reads: {2}, writes: {3}, executes:{4}".format(self.name, self.processNumber, ','.join(node.name for node in self.reads), ','.join(node.name for node in self.writes), ','.join(node.name for node in self.executes))


def buildGraph(fileName):
    f = open(fileName, 'r')
    lines = [line.strip() for line in f.readlines() if line != '\n']
    fileChunks = [i for i, line in enumerate(lines) if line.startswith('Process:')]
    processMap = {}
    fileMap = {}
    for i, lineNum in enumerate(fileChunks):
        if i == len(fileChunks) - 1:
            linesForFile = lines[lineNum:]
        else:
            linesForFile = lines[lineNum:fileChunks[i+1]]
        processLinesForFile(linesForFile, processMap, fileMap)
    return processMap, fileMap

def processLinesForFile(linesForFile, processMap, fileMap):
    global processNumber

    fileName = None
    processName = None
    reads = []
    writes = []
    executes = []
    processPrefix = "Process: "
    readsPrefix = "Reads: "
    writesPrefix = "Writes: "
    executesPrefix = "Executes: "
    for line in linesForFile:
        if line.startswith(processPrefix):
            processName = line[len(processPrefix):]
        if line.startswith(readsPrefix):
            reads = [ln.strip() for ln in line[len(readsPrefix):].split(',')]
        if line.startswith(writesPrefix):
            writes = [ln.strip() for ln in line[len(writesPrefix):].split(',')]
        if line.startswith(executesPrefix):
            executes = [ln.strip() for ln in line[len(executesPrefix):].split(',')]
    processNode = ProcessNode(processName, processNumber)
    processNumber += 1
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
    processMap[processNode.processNumber] = processNode


processMap, fileMap =  buildGraph('config.txt')
for name in processMap.keys():
    print processMap[name]
