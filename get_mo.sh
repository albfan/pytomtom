#!/bin/sh
LANG_PO="fr"
LOC_DIR="share/locale/"$LANG_PO"/LC_MESSAGES"
mkdir "share/locale/"$LANG_PO
mkdir $LOC_DIR
msgfmt "po/"$LANG_PO".po" -o $LOC_DIR"/pytomtom.mo"

LANG_PO="it"
LOC_DIR="share/locale/"$LANG_PO"/LC_MESSAGES"
mkdir "share/locale/"$LANG_PO
mkdir $LOC_DIR
msgfmt "po/"$LANG_PO".po" -o $LOC_DIR"/pytomtom.mo"

LANG_PO="de"
LOC_DIR="share/locale/"$LANG_PO"/LC_MESSAGES"
mkdir "share/locale/"$LANG_PO
mkdir $LOC_DIR
msgfmt "po/"$LANG_PO".po" -o $LOC_DIR"/pytomtom.mo"





