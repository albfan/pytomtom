#!/bin/sh
INSTALL_DIR="/share/pytomtom"
MAN_DIR="/share/man/pytomtom"
BIN_DIR="/bin"
LOC_DIR="/share/locale"
APP_DIR="/share/applications"
LOC_DIR="/share/locale"
ICO_DIR="/share/pixmaps"
VERSION="0.4.1"

mkdir -p "pytomtom"$ICO_DIR
cp share/pixmaps/pytomtom.png "pytomtom"$ICO_DIR

mkdir -p "pytomtom"$INSTALL_DIR"/src"
cp share/pytomtom/src/pytomtom.py "pytomtom"$INSTALL_DIR"/src"

mkdir -p "pytomtom"$INSTALL_DIR"/pix"
cp share/pytomtom/pix/*.png "pytomtom"$INSTALL_DIR"/pix"

mkdir -p "pytomtom"$LOC_DIR
cp -R share/locale/* "pytomtom"$LOC_DIR


mkdir -p "pytomtom"$APP_DIR
cp share/applications/pytomtom.desktop "pytomtom"$APP_DIR

mkdir -p "pytomtom"$BIN_DIR
cp bin/pytomtom.sh "pytomtom"$BIN_DIR"/pytomtom"

cp pytomtom.sh "pytomtom"
cp COPYING "pytomtom"
cp README "pytomtom"

tar czfv pytomtom-$VERSION.tar.gz pytomtom/
rm -rf pytomtom
