#!/bin/bash

ARDUINO="arduino-0019"
VIRTUALWIRE="VirtualWire-1.5"

BASE=`readlink -f \`dirname $0\``

pushd $BASE
rm -rf bin
mkdir bin
cd bin
tar xvf $BASE/toolkits/$ARDUINO.tgz
cd $ARDUINO/libraries
unzip $BASE/toolkits/$VIRTUALWIRE.zip
cd $BASE

rm run_ide.sh
echo "#!/bin/bash" >> run_ide.sh
echo "" >> run_ide.sh
echo "$BASE/bin/$ARDUINO/arduino" >> run_ide.sh
chmod +x run_ide.sh

popd
