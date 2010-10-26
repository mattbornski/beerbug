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

def serve(username, password):
    try:
        while True:
            port = None
            # Detect which USB device the Arduino lives on.
            for device in glob.glob('/dev/ttyUSB*'):
                try:
                    # TODO: Figure out how to determine if this is our
                    # device or another device.
                    port = serial.Serial(device)
                except KeyboardInterrupt:
                    # Do not handle, pass up to outside handler.
                    raise KeyboardInterrupt
                except:
                    # Errors are to be expected while randomly probing
                    # ports.
                    pass
            if port is not None:
                client = gdata.spreadsheet.text_db.DatabaseClient(
                  username = username, password = password)
                db = client.GetDatabases(name = 'Beerbug Testing')[0]
                table = db.GetTables()[0]
                try:
                    while True:
                        now = datetime.datetime.now().strftime(
                          '%m/%d/%Y %H:%M:%S')
                        try:
                            sample = readSample(port)
                        except KeyboardInterrupt:
                            # Do not handle, pass up to outside handler.
                            raise KeyboardInterrupt
                        except:
                            # Throw the error and then attempt to continue.
                            print >> sys.stderr, 'Problem reading sample.'
                            traceback.print_exc(file=sys.stderr)
                        if sample is not None:
                            table.AddRecord(
                              {'time':now, 'temperature':str(sample)},
                            )
                except KeyboardInterrupt:
                    # Do not handle, pass up to outside handler.
                    raise KeyboardInterrupt
                except:
                    # Throw the error and then attempt to continue.
                    print >> sys.stderr, 'Problem uploading sample'
                    traceback.print_exc(file=sys.stderr)
            else:
                # Notify user and attempt to continue later.
                print >> sys.stderr, 'Unable to locate Arduino on a USB port.'
                # Unlike some of the other errors, this one most likely
                # requires human interaction to fix, so give them some time.
                time.sleep(30)
    except KeyboardInterrupt:
        pass

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
