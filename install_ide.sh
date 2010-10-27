#!/bin/bash

ARDUINO="arduino-0021"
VIRTUALWIRE="VirtualWire-1.5"
DHCP="Arduino-DHCPv0.4"
TIME="Time"
WEBDUINO="webduino-1.4.1"

USER_BASE=`readlink -f \`dirname $0\``
FILES_BASE=$USER_BASE/embedded

pushd $FILES_BASE
rm -rf bin
mkdir bin
cd bin
tar xvf $FILES_BASE/toolkits/$ARDUINO.tgz
cd $ARDUINO/libraries
unzip $FILES_BASE/toolkits/$VIRTUALWIRE.zip
unzip $FILES_BASE/toolkits/$DHCP.zip
unzip $FILES_BASE/toolkits/$TIME.zip
unzip $FILES_BASE/toolkits/$WEBDUINO.zip

cd $USER_BASE
rm run_ide.sh
echo "#!/bin/bash" >> run_ide.sh
echo "" >> run_ide.sh
echo "$FILES_BASE/bin/$ARDUINO/arduino &" >> run_ide.sh
chmod +x run_ide.sh

popd
