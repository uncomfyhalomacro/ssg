#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" || exit ; pwd -P )"
export SCRIPTPATH
python3 -m unittest discover -s "$SCRIPTPATH/src"
python3 -m unittest discover -s "$SCRIPTPATH/src/markdown"
