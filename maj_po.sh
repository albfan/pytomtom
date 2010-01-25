#!/bin/sh
PY_DIR="share/pytomtom/src/pytomtom.py"
PO_LANG="en"

rm po/pytomtom.pot
xgettext -k_ -kN_ -o "po/pytomtom.pot" $PY_DIR
msgmerge -U "po/"$PO_LANG".po" "po/pytomtom.pot"




