#!/bin/bash

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

check_requirements(){
    python3 -m pip install --upgrade --quiet pip
    if [ -f "requirements.txt" ]; then
        pip install --upgrade -r requirements.txt
    else
        echo "Error: requirements.txt was not found."
        exit 1
    fi
}

cleanup(){
    echo "Terminating..."
    pkill -P $$ || true
    wait || true
}

trap cleanup EXIT SIGHUP SIGINT SIGTERM
check_requirements
python3 main.py &
wait