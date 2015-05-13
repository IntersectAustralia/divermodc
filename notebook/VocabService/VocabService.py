#!/anaconda/bin/python

from netCDF4 import Dataset
import csv
import re

vocabFile = 'data/eMAST_vocab_service.csv'

def standardNames():
    list = []

    with open(vocabFile, 'rt') as csvfile:
        vocabulary = csv.DictReader(csvfile, dialect='excel', delimiter=',', quotechar='"')
        for row in vocabulary:
            if row['Standard_Name'] not in list:
                 list.append(row['Standard_Name'])

    return list
 	    
def variablesIn(Filename):
    short_names = []
    rootgrp = Dataset(Filename, 'r')
    variables = rootgrp.variables.keys()
    for key in variables:
        short_names.append(key)
    rootgrp.close()
    return short_names

def variableDefine(VarName):
    with open(vocabFile, 'rt') as csvfile:
        vocabulary = csv.DictReader(csvfile, dialect='excel', delimiter=',', quotechar='"')
        for row in vocabulary:
            if row['Variable_Name'] == VarName:
                return row['Definition_Variable_Name']
        return "Variable " + VarName + " not in schema."

def Lookup(VarName, Attribute):
    with open(vocabFile, 'rt') as csvfile:
        vocabulary = csv.DictReader(csvfile, dialect='excel', delimiter=',', quotechar='"')
        for row in vocabulary:
            if row['Short_Name'] == VarName:
                return row[Attribute]

def listVariables(VarName):
    list = [];
    with open(vocabFile, 'rt') as csvfile:
        vocabulary = csv.DictReader(csvfile, dialect='excel', delimiter=',', quotechar='"')
        for row in vocabulary:
            if row['Short_Name'] == VarName:
                list.append(row['Variable_Name'])
    return list

def listShortNames(VarName):
    list = [];
    with open(vocabFile, 'rt') as csvfile:
        vocabulary = csv.DictReader(csvfile, dialect='excel', delimiter=',', quotechar='"')
        for row in vocabulary:
            if row['Standard_Name'] == VarName:
                list.append(row['Short_Name'])
    return list

def vocabList(VarName):
    list = [];
    with open(vocabFile, 'rt') as csvfile:
        vocabulary = csv.DictReader(csvfile, dialect='excel', delimiter=',', quotechar='"')
        for row in vocabulary:
            list.append(row[VarName])
    return list

def variableCategories(VarName):
    list = [];
    with open(vocabFile, 'rt') as csvfile:
        vocabulary = csv.DictReader(csvfile, dialect='excel', delimiter=',', quotechar='"')
        for row in vocabulary:
            #print ("'" + row['Variable_Name'] + "' = " + VarName)
            if row['Variable_Name'] == VarName:
                list.append(row['Standard_Name'])
    return list

def listLabels(VarName):
    with open(vocabFile, 'rt') as csvfile:
        vocabulary = csv.DictReader(csvfile, dialect='excel', delimiter=',', quotechar='"')
        for row in vocabulary:
            if row['Variable_Name'] == VarName:
                return row['Label'].split(',')
    return ["Not found"]
    
def variablesWithLabel(VarName):
    list = [];
    with open(vocabFile, 'rt') as csvfile:
        vocabulary = csv.DictReader(csvfile, dialect='excel', delimiter=',', quotechar='"')
        for row in vocabulary:
            if VarName in row['Label'].split(','):
                list.append(row['Short name'])
    return list

def variablesDefinedWith(Term):
    list = [];
    with open(vocabFile, 'rt') as csvfile:
        vocabulary = csv.DictReader(csvfile, dialect='excel', delimiter=',', quotechar='"')
        for row in vocabulary:
            if Term in row['Long definition']:
                list.append(row['Short name'])

    return list

KEY_EXPERIMENT = "experiment_id"
KEY_FACILITY = "facility_id"
KEYLIST = [KEY_EXPERIMENT, KEY_FACILITY]

def getKey(var_list_json, key, quiet=False):
    if key not in KEYLIST:
        print ('No such key: ' + key)
        print ('Try one of these:')
        print (KEYLIST)
        return
    var_set = set()
    for var in var_list_json:
        if key in var and var[key]:
          var_set.add(var[key])
    # print if not quiet
    if not quiet:
        print ('\nAll "' + key + '" variables:\n')
        for var in var_set:
            print (var)
    return var_set
