#!/bin/sh
PY_DIR="share/pytomtom/src/pytomtom.py"

xgettext -k_ -kN_ -o "pytomtom.pot" $PY_DIR
msginit -i pytomtom.pot -o "pytomtom.po"




