#!/bin/sh
cd $(dirname $(readlink -f $0))/bin && python2 '../share/pytomtom/src/pytomtom.py'
