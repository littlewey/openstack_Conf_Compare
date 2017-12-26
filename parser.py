from oslo_config import iniparser
from dictdiffer import diff
from difflib import Differ
import sys

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
'''

folderAPath, folderBPath = sys.argv[1], sys.argv[2]

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

diff, A, B = diffConf(confA,confB)

def diffConfWithPath(pathAconf,pathBconf):
    with open (pathAconf,'r') as aConf, open (pathBconf, 'r') as bConf:
        return diffConf(aConf,bConf)
