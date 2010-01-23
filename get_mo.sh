#!/bin/sh
LANG_PO="fr"
LOC_DIR="share/locale/"$LANG_PO"/LC_MESSAGES"
PY_DIR="share/pytomtom/src/pytomtom.py"

msgfmt "po/"$LANG_PO".po" -o $LOC_DIR"/pytomtom.mo"




