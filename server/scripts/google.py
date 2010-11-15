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

class service(dict):
    username = None
    password = None
    client = None
    def __init__(self, username = None, password = None):
        # Read the username and password from a config file.
        # If not present, prompt the user for their credentials.
        paths = [
          os.path.expanduser('~/.beerbug/beerbug.ini'),
          os.path.join(os.path.dirname(__file__), 'beerbug.ini'),
          os.path.abspath('beerbug.ini'),
        ]
        for path in paths:
            parser = ConfigParser.SafeConfigParser()
            parser.read(path)
            if parser is not None:
                try:
                    try:
                        username = parser.get('google', 'username')
                    except ConfigParser.NoOptionError:
                        pass
                    try:
                        password = parser.get('google', 'password')
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
        if username is not None:
            self.username = username
        if password is not None:
            self.password = password
        # Connect
        self.client = self.connect()
        # Populate
        self._index()
    def connect(self):
        # Read username and password from config files if not set.
        
        # Connect to Google
        return gdata.spreadsheet.text_db.DatabaseClient(
          username = self.username, password = self.password)
    def _index(self):
        for db in self.client.GetDatabases(name = ''):
            self[db.entry.title.text] = spreadsheet(db)

class spreadsheet(dict):
    def __init__(self, db):
        tables = db.GetTables()
        for table in tables:
            self[table.name] = page(table)

class page(dict):
    def __init__(self, table):
        print table
        print dir(table)
        print table.fields
        print table.entry
        print table.LookupFields()
        print table.GetRecords()
#            try:
#                while True:
#                    now = datetime.datetime.now().strftime(
#                      '%m/%d/%Y %H:%M:%S')
#                    try:
#                        sample = readSample(port)
#                    except KeyboardInterrupt:
#                        # Do not handle, pass up to outside handler.
#                        raise KeyboardInterrupt
#                    except:
#                        # Throw the error and then attempt to continue.
#                        print >> sys.stderr, 'Problem reading sample.'
#                        traceback.print_exc(file=sys.stderr)
#                    if sample is not None:
#                        table.AddRecord(
#                          {'time':now, 'temperature':str(sample)},
#                        )
#            except KeyboardInterrupt:
#                # Do not handle, pass up to outside handler.
#                raise KeyboardInterrupt
#            except:
#                # Throw the error and then attempt to continue.
#                print >> sys.stderr, 'Problem uploading sample'
#                traceback.print_exc(file=sys.stderr)
#        else:
#            # Notify user and attempt to continue later.
#            print >> sys.stderr, 'Unable to locate Arduino on a USB port.'
#            # Unlike some of the other errors, this one most likely
#            # requires human interaction to fix, so give them some time.
#            time.sleep(30)
#    except KeyboardInterrupt:
#        pass

def serve_forever():
    service()

if __name__ == '__main__':
    serve_forever()
