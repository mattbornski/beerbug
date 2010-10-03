#!/usr/bin/env python

import daemonize
import gdata.docs
import gdata.docs.service
import glob
import serial
import sys
import time
import traceback

class service(daemonize.Daemon):
    def __init__(self, *args, **kwargs):
        daemonize.Daemon.__init__(self, *args, **kwargs)
    def run(self):
        while True:
            port = None
            # Detect which USB device the Arduino lives on.
            for device in glob.glob('/dev/ttyUSB*'):
                try:
                    port = serial.Serial(device)
                except:
                    pass
            if port is not None:
                client = gdata.docs.service.DocsService(source='beerbug')
                client.ClientLogin()
                while True:
                    # Not the most efficient way to communicate over the port,
                    # but I'm not exactly I/O limited here.
                    try:
                        sample = int(port.readline().split()[0])
                    except:
                        print >> sys.stderr, 'Error reading sample.'
                        traceback.print_exc(file=sys.stderr)
                        break
                    try:
                        pass
                    except:
                        print >> sys.stderr, 'Error uploading sample.'
                        traceback.print_exc(file=sys.stderr)
                        break
            else:
                time.sleep(30)

def serve_forever(*args, **kwargs):
    service(*args, **kwargs).restart()
