#!/bin/sh
INSTALL_DIR="/usr/share/pytomtom"
MAN_DIR="/usr/share/man/pytomtom"
BIN_DIR="/usr/bin"
APP_DIR="/usr/share/applications"
LOC_DIR="/usr/share/locale"
ICO_DIR="/usr/share/pixmaps"
VERSION="0.4"

mkdir -p pytomtom/DEBIAN
cp control-install pytomtom/DEBIAN/control

mkdir -p "pytomtom"$ICO_DIR
cp share/pixmaps/pytomtom.png "pytomtom"$ICO_DIR

##mkdir -p "test"$MAN_DIR
##cp doc/test "test"$MAN_DIR

mkdir -p "pytomtom"$INSTALL_DIR
mkdir -p "pytomtom"$INSTALL_DIR"/src"
cp share/pytomtom/src/pytomtom.py "pytomtom"$INSTALL_DIR"/src"

##mkdir -p "test"$INSTALL_DIR"/res"
##cp res/*.glade "test"$INSTALL_DIR"/res/"

mkdir -p "pytomtom"$INSTALL_DIR
mkdir -p "pytomtom"$INSTALL_DIR"/pix"
cp share/pytomtom/pix/*.png "pytomtom"$INSTALL_DIR"/pix"

##mkdir -p "test"$INSTALL_DIR"/doc"
##cp doc/gpl.txt "test"$INSTALL_DIR"/doc/"
##cp doc/whatsnew.txt "test"$INSTALL_DIR"/doc/"

mkdir -p "pytomtom"$APP_DIR
cp share/applications/pytomtom.desktop "pytomtom"$APP_DIR

mkdir -p "pytomtom"$BIN_DIR
cp bin/pytomtom.sh "pytomtom"$BIN_DIR"/pytomtom"

#mkdir -p "pytomtom"$LOC_DIR
#cp -R locale/* "pytomtom"$LOC_DIR

dpkg-deb --build pytomtom pytomtom-$VERSION.deb
rm -rf pytomtom
