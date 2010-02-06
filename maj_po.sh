#!/bin/sh
PY_DIR="share/pytomtom/src/pytomtom.py"
rm po/pytomtom.pot
xgettext -k_ -kN_ -o "po/pytomtom.pot" $PY_DIR

PO_LANG="en"
msgmerge -U "po/"$PO_LANG".po" "po/pytomtom.pot"

PO_LANG="fr"
msgmerge -U "po/"$PO_LANG".po" "po/pytomtom.pot"

PO_LANG="it"
msgmerge -U "po/"$PO_LANG".po" "po/pytomtom.pot"

PO_LANG="de"
msgmerge -U "po/"$PO_LANG".po" "po/pytomtom.pot"



