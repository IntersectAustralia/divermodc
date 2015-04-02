!/usr/bin/python

import hiev
import os, sys, getopt

# The user generated token from DIVER
TOKEN='LyVwmbv5tXDXNoeSdG28'

# This is the eWATCH experiment ID, under facility EWATCH
EWATCH_EXP_ID = 4

def usage():
    print('usage: python ingest.py <directory_containing_files>')

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"h")
        if len(argv) < 1:
            usage()
            sys.exit(2)
        elif len(argv) > 1:
            print("Please specify just ONE directory")
            usage()
            sys.exit(2)
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
    in_dir = argv[0]
    upload_files(in_dir)

def upload_files(dirpath):
    hiev.set_token(TOKEN)
    hiev.set_host('https://rdsi-emast4-vm.intersect.org.au')

    print("Iterating through all the files in %s") % dirpath
    for root, subdirs, files in os.walk(dirpath):
      print(root)
      for filename in files:
          filepath = os.path.join(root, filename)
          print("Trying %s..") % filepath
          response = hiev.upload(filepath, EWATCH_EXP_ID, 'CLEANSED')
          if response:
            print(response.text)
