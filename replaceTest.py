#!/usr/bin/env python2

import re
from os import path

configList = []

def replaceText():
    print('Hello World')
    
    myFile = "myConfig.xml"
    reading_file = open(myFile, "r")

    new_file_content = ""
    for line in reading_file:
        #stripped_line = line.strip()
        new_line = line.replace("{config1}", "new string")
        new_file_content += new_line
    
    reading_file.close()

    writing_file = open(myFile, "w")
    writing_file.write(new_file_content)
    writing_file.close()

def getConfigurableKeywords(parsed_line_tokens):

    configurableKeywords = []
    pattern = '\{(.*?)\}'

    #parse the line and filter matching {X} pattern
    tokens = [token for token in parsed_line_tokens if re.match(pattern, token)]

    if not tokens:
        return None
        
    #remove { and }
    for configurableKeyword in tokens:
        tokens = re.split('{|}', configurableKeyword) 

        for token in tokens:
            if(len(token) > 2):
                configurableKeywords.append(token)  

    return configurableKeywords


def parseLine():

    myFile = "myConfig.xml"
    reading_file = open(myFile, "r")

    new_file_content = ""
    for line in reading_file:
        tokens = re.split('<|>', line) 
        list1 = getConfigurableKeywords(tokens)
        print(list1)
    
def createConfigurationKeyValueMap():

    configFilename = 'cws_config.csv'

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
            

    print(configList)

if __name__ == "__main__":
    createConfigurationKeyValueMap()