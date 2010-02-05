#!/bin/sh
INSTALL_DIR="/share/pytomtom"
MAN_DIR="/share/man/pytomtom"
BIN_DIR="/bin"
LOC_DIR="/share/locale"
APP_DIR="/share/applications"
LOC_DIR="/share/locale"
ICO_DIR="/share/pixmaps"
VERSION="0.4.2"

## CREATION TAR.GZ
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

mkdir -p "tel/"$VERSION
tar czfv tel/$VERSION/pytomtom-$VERSION.tar.gz pytomtom/
rm -rf pytomtom
cp tel/$VERSION/pytomtom-$VERSION.tar.gz tel/pytomtom.tar.gz
cp tel/$VERSION/pytomtom-$VERSION.tar.gz tel/pytomtom-current.tar.gz

## CREATION DEB
mkdir -p pytomtom/DEBIAN
cp control-install pytomtom/DEBIAN/control
mkdir -p "pytomtom/usr"$ICO_DIR
cp share/pixmaps/pytomtom.png "pytomtom/usr"$ICO_DIR
mkdir -p "pytomtom/usr"$INSTALL_DIR
mkdir -p "pytomtom/usr"$INSTALL_DIR"/src"
cp share/pytomtom/src/pytomtom.py "pytomtom/usr"$INSTALL_DIR"/src"
mkdir -p "pytomtom/usr"$INSTALL_DIR
mkdir -p "pytomtom/usr"$INSTALL_DIR"/pix"
cp share/pytomtom/pix/*.png "pytomtom"$INSTALL_DIR"/pix"
mkdir -p "pytomtom/usr"$APP_DIR
cp share/applications/pytomtom.desktop "pytomtom/usr"$APP_DIR
mkdir -p "pytomtom/usr"$BIN_DIR
cp bin/pytomtom.sh "pytomtom/usr"$BIN_DIR"/pytomtom"
mkdir -p "pytomtom/usr"$LOC_DIR
cp -R share/locale/* "pytomtom/usr"$LOC_DIR

mkdir -p "tel/"$VERSION
dpkg-deb --build pytomtom tel/$VERSION/pytomtom-$VERSION.deb
rm -rf pytomtom
cp tel/$VERSION/pytomtom-$VERSION.deb tel/pytomtom-current.deb
cd tel/$VERSION/ && alien --to-rpm pytomtom-$VERSION.deb
rm -rf ~/rpmbuild
