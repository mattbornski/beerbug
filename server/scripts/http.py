#!/usr/bin/env python

import ConfigParser
import datetime
import gdata.spreadsheet.text_db
import getpass
import glob
import os.path
import serial
import sys
import time
import traceback

def readSample(port):
    # Not the most efficient way to communicate over the port,
    # but I'm not exactly I/O limited here.
    try:
        temp = float(port.readline().split()[0])
        return temp
    except (ValueError, IndexError):
        # Format was unexpected.  This can occur as communications can be
        # disrupted.
        pass

class service:
    schema = {'Beerbug Testing':['time', 'temperature']}
    now = datetime.datetime.now().strftime(
      '%m/%d/%Y %H:%M:%S')
    sample = readSample(port)
    if sample is not None:
        table.AddRecord(
          {'time':now, 'temperature':str(sample)},
        )

def serve_forever():
    username = None
    password = None
    # Read the username and password from a config file.
    # If not present, prompt the user for their credentials.
    parser = ConfigParser.SafeConfigParser()
    path = os.path.expanduser('~/.beerbug/beerbug.ini')
    parser.read(path)
    if parser is not None:
        try:
            try:
                username = parser.get('beerbug', 'username')
            except ConfigParser.NoOptionError:
                pass
            try:
                password = parser.get('beerbug', 'password')
            except ConfigParser.NoOptionError:
                pass
        except ConfigParser.NoSectionError:
            pass
    if username is None:
        username = raw_input('Enter Google Docs username [' \
          + getpass.getuser() + ']: ')
        if username.strip() == '':
            username = getpass.getuser()
    if password is None:
        password = getpass.getpass('Enter Google Docs password: ')
    serve(username, password)

if __name__ == '__main__':
    serve_forever()
