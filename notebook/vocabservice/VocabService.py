#!/anaconda/bin/python

from netCDF4 import Dataset
import csv
import re

vocabFile = 'data/eMAST_vocab_service.csv'

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
            if row['Short name'] == VarName:
                return row['Long definition']
        return "Variable not in schema."

def vocabLookup(VarName, Attribute):
    with open(vocabFile, 'rt') as csvfile:
        vocabulary = csv.DictReader(csvfile, dialect='excel', delimiter=',', quotechar='"')
        for row in vocabulary:
            if row['Short name'] == VarName:
                return row[Attribute]

def listVariables(VarName):
    list = [];
    with open(vocabFile, 'rt') as csvfile:
        vocabulary = csv.DictReader(csvfile, dialect='excel', delimiter=',', quotechar='"')
        for row in vocabulary:
            if row['Top-level category'] == VarName:
                list.append(row['Short name'])
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
            if row['Short name'] == VarName:
                list.append(row['Top-level category'])
    return list

def listLabels(VarName):
    with open(vocabFile, 'rt') as csvfile:
        vocabulary = csv.DictReader(csvfile, dialect='excel', delimiter=',', quotechar='"')
        for row in vocabulary:
            if row['Short name'] == VarName:
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
