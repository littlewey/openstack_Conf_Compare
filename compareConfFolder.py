from oslo_config import iniparser
from dictdiffer import diff
from difflib import Differ

import sys

from filecmp import dircmp

'''
TEST loadConfLocally


confA_file_path = "./testA.conf"
confB_file_path = "./testB.conf"
confA_file_path = "IMO-sort-filter-cic-nova.conf"
confB_file_path = "PCE-sort-filter-cic-nova.conf"
confA_file = open(confA_file_path,'r')
confB_file = open(confB_file_path,'r')
confA = confA_file.read()
confB = confB_file.read()
diff, A, B = diffConf(confA,confB)
'''

folderAPath, folderBPath = sys.argv[1], sys.argv[2]
report = []

def diffConf(confA,confB):
    def listConf(inputString):
        return inputString.strip().split("\n")

    class ConfigParser(iniparser.BaseParser):
        comment_called = False
        values = None
        section = ''

        def __init__(self):
            self.values = {}

        def assignment(self, key, value):
            self.values.setdefault(self.section, {})
            self.values[self.section][key] = value

        def new_section(self, section):
            self.section = section

        def comment(self, section):
            self.comment_called = True

    parserA = ConfigParser()
    parserA.parse(listConf(confA))
    #print "parserA.values \n" 
    #print parserA.values

    parserB = ConfigParser()
    parserB.parse(listConf(confB))
    #print "parserB.values \n" 
    #print parserB.values

    diffList = list(diff(parserA.values,parserB.values))
    #print "diff \n"
    #print diffList
    return [diffList,parserA.values,parserB.values]



def diffConfWithPath(pathAconf,pathBconf):
    with open (pathAconf,'r') as aConf, open (pathBconf, 'r') as bConf:
        return diffConf(aConf.read(),bConf.read())

def _compareFolder(dcmp):
    for name in dcmp.diff_files:
        # print "Different file %s found in %s and %s" % (name, dcmp.left,dcmp.right)
        title = "Different file %s found in %s and %s" % (name, dcmp.left,dcmp.right)

        filePathLeft, filePathRight = dcmp.left + "/" + name, dcmp.right + "/" + name
        diffConfList = diffConfWithPath(filePathLeft, filePathRight)
        report.append(title)
        reportContent = generateDiffReport(diffConfList[0])
        report.extend(reportContent)
        # print str(diffConfList[0])
    for name in dcmp.left_only:
        title = "Left only file %s found only in %s " % (name, dcmp.left)
        report.append(title)
    for name in dcmp.right_only:
        title = "Right only file %s found only in %s " % (name, dcmp.right)
        report.append(title)
    for sub_dcmp in dcmp.subdirs.values():
        _compareFolder(sub_dcmp)

def getDeltaValue(valueA, valueB):
    valueA = valueA + ","
    valueB = valueB + ","
    diffMarkList = list(Differ().compare(valueA, valueB))
    # test print str(diffMarkList)
    deltaValueA = str()
    deltaValueB = str()
    propertyA = str()
    propertyB = str()
    deltaFlag = False
    for eachChar in diffMarkList:
        # eachChar[-1] is the current char
        # eachChar[:1] is the diff mark, + means value from A, - means value from B, space means common part
        if eachChar[-1] == ",":
            if deltaFlag:
                # fixing bugs that add a comma even when propertyA or *B is ""
                deltaValueA = (deltaValueA + propertyA + ",") if propertyA else deltaValueA
                deltaValueB = (deltaValueB + propertyB + ",") if propertyB else deltaValueB
            propertyA = ""
            propertyB = ""
            deltaFlag = False
        else:
            diffState   = eachChar[:1]
            currentChar = eachChar[-1]
            if diffState == " ":
                propertyA = propertyA + currentChar
                propertyB = propertyB + currentChar
            if diffState == "+":
                propertyA = propertyA + currentChar
                deltaFlag = True
            if diffState == "-":
                propertyB = propertyB + currentChar
                deltaFlag = True
    return dict(A = deltaValueA, B = deltaValueB )

def buildResultRow(result,paraName,aFileValue,bFileValue):
    return [result,paraName,aFileValue,bFileValue]

def generateDiffReport(diffList):
    data = []
    for line in diffList:
        if line[0] == "change":
            # improved result in values, show only delta part
            valueA = str(line[2][0])
            #print "valueA" + valueA
            valueB = str(line[2][1])
            #print "valueB" + valueB
            diffValue = getDeltaValue(valueA,valueB)
            # improved result in values, show only delta part
            row = buildResultRow("diff",str(line[1]),diffValue["A"], diffValue["B"])
            #appendItem = buildTableItem(row)
            #items.append(appendItem)
            data.append([eachCell for eachCell in row])
        if line[0] == "add":
            for item in line[2]:
                row = buildResultRow("leftMiss",str(item[0]) ,"NOTHING HERE",str(item[1]) )
                #appendItem = buildTableItem(row)
                #items.append(appendItem)
                data.append([eachCell for eachCell in row])
        if line[0] == "remove":
            for item in line[2]:
                row = buildResultRow("rightMiss",str(item[0]) ,str(item[1]),"NOTHING HERE")
                #appendItem = buildTableItem(row)
                #items.append(appendItem)
                data.append([eachCell for eachCell in row])
    return data




def compareFolder(A,B):
    # compare folder with dircmp
    dcmp = dircmp(A,B)
    # do deeper print
    _compareFolder(dcmp) 



compareFolder(folderAPath, folderBPath)

print "\n".join(str(item) for item in report)