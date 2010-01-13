#!/bin/sh
LOCALE_DIR="share/locale/en/LC_MESSAGES"
PY_DIR="share/pytomtom/src/pytomtom.py"

xgettext -k_ -kN_ -o "pytomtom.pot" $PY_DIR
mkdir -p $LOCALE_DIR
msginit -i pytomtom.pot -o "pytomtom.po"

##msgfmt $LOCALE_DIR"/pytomtom.po" -o $LOCALE_DIR"/pytomtom.mo"
##rm -f $LOCALE_DIR"/pytomtom.po"




