#!/usr/bin/env python2
import re
import sys
import os
import time
from os import path

#default folder where config is copied and config values are applied
baseDirectory =  "./jenkins_workspace"

#Number of seconds of two days
# epochDiffLimit = 172800
epochDiffLimit = 1

def isFileNeedUpdate(filename):

    if filename is None:
        return False
        
    curTime = time.time()
    lastModTime = os.path.getmtime(filename)

    if(not filename.endswith('.xml')):
        print('Filename: {0}, File Extension is not xml.'.format(filename))
        return False

    if (curTime - lastModTime) < epochDiffLimit:
        print('Filename: {0}, Last Update: {1}.'.format(filename, time.ctime(lastModTime)))
        return False

    return True

def replaceConfig(fileList, applicableSettings):

    for filename in fileList:

        if isFileNeedUpdate(filename):
            replaceConfigInFile(filename, applicableSettings)
        else:
            print("Skipping file: {0}.".format(filename))

def replaceConfigInFile(fname, applicableSettings):

    reading_file = open(fname, "r")

    new_file_content = ""
    for file_line in reading_file:
        
        if '{' not in file_line or '}' not in file_line:
            new_file_content += file_line
            continue
        
        tokens = re.split('<|>', file_line.strip()) 
        configurableKeywords = getConfigurableKeywords(tokens)

        if(not configurableKeywords):
            new_file_content += file_line
        else:
            
            for keyword in configurableKeywords:
                keywordToBeReplaced = '${' + keyword + '}'
                keywordNewValue = applicableSettings[keyword]
                print('Replacing {0} with {1}.'.format(keywordToBeReplaced, keywordNewValue))
                new_line = file_line.replace(keywordToBeReplaced, keywordNewValue)

            new_file_content += new_line
    
    reading_file.close()

    writing_file = open(fname, "w")
    writing_file.write(new_file_content)
    writing_file.close()

def getConfigurableKeywords(parsed_line_tokens):

    configurableKeywords = []
    pattern = '\${(.*?)\}'

    #parse the line and filter matching {X} pattern
    tokens = [token for token in parsed_line_tokens if re.match(pattern, token)]

    if not tokens:
        return []
        
    #remove { and }
    for configurableKeyword in tokens:
        tokens = re.split('{|}', configurableKeyword) 

        for token in tokens:
            if(len(token) > 2):
                configurableKeywords.append(token)  

    return configurableKeywords
    
def createConfigurationKeyValueMap():

    configFilename = 'cws_config.csv'
    configList = []

    if(not path.exists(configFilename)):
        raise Exception("Unable to load CWS config file.")
    
    with open(configFilename, "r") as f:
        lineNumber = 2
        next(f)

        for line in f:
            tokens = line.split(",")
            
            if(len(tokens) != 3):
                raise Exception("Invalid Tuple Value at line: ", lineNumber)

            lineNumber += 1
            configList.append((tokens[0].strip(), tokens[1].strip(), tokens[2].strip()));
            
    return configList

def isNodeHasOtherDefineSettings(csvSettings, nodeId):
    return True if [setting for setting in csvSettings if setting[0] == nodeId] else False

def getNodeSettings(nodeId):

    applicableConfig = {}

    print('Reading csv configuration file..')
    csvSettings = createConfigurationKeyValueMap()

    #filter: get only applicable settings including 'all'
    csvSettings = [setting for setting in csvSettings if setting[0] == nodeId or setting[0] == 'all']

    if not isNodeHasOtherDefineSettings(csvSettings, nodeId):
        raise Exception('No settings found for nodeId: {0}.'.format(nodeId))

    #create a key/value pair of setting name/setting value
    applicableConfig = {sub[1]: sub[2] for sub in csvSettings}

    return applicableConfig

def validateNodeId(sysargs):
    
    # if(len(sysargs) <= 1):
    #     raise Exception('Invalid NodeId value')
    # return sysargs[1]

    return 'pluk-69'

def getTargetDirectoryContents():

    if(not path.exists(baseDirectory)):
        raise Exception('Unable to open target folder.')

    fname = []
    for root,d_names,f_names in os.walk(baseDirectory):
	    for f in f_names:
		    fname.append(os.path.join(root, f))

    return fname

if __name__ == "__main__":
    nodeId = validateNodeId(sys.argv)
    applicableSettings = getNodeSettings(nodeId)
    fileList = getTargetDirectoryContents()
    replaceConfig(fileList, applicableSettings)