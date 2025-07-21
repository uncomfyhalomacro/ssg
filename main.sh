#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" || exit ; pwd -P )"
export SCRIPTPATH
python3 "$SCRIPTPATH/src/main.py"
cd "$SCRIPTPATH/public" && python3 -m http.server 8888

