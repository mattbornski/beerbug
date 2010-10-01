#!/bin/bash

ARDUINO="arduino-0019"
VIRTUALWIRE="VirtualWire-1.5"

BASE=`readlink -f \`dirname $0\``

pushd $BASE
mkdir bin
cd bin
tar xvf $BASE/toolkits/$ARDUINO.tgz
cd $ARDUINO/libraries
unzip $BASE/toolkis/$VIRTUALWIRE.zip
cd $BASE

ln -s bin/$ARDUINO/arduino run_ide

popd
