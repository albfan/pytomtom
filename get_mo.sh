#!/bin/sh
LOCALE_DIR="share/locale/fr/LC_MESSAGES"
PY_DIR="share/pytomtom/src/pytomtom.py"


msgfmt $LOCALE_DIR"/pytomtom.po" -o $LOCALE_DIR"/pytomtom.mo"
##rm -f $LOCALE_DIR"/pytomtom.po"




