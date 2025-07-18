#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" || exit ; pwd -P )"
export SCRIPTPATH
python3 "$SCRIPTPATH/src/main.py"
