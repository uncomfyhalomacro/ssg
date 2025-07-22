#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" || exit ; pwd -P )"
export SCRIPTPATH
cd $SCRIPTPATH
python3 -m "ssg"
cd "$SCRIPTPATH/public" && python3 -m http.server 8888

