#!/bin/bash

ENV_NAME=whisplit
REQ_FILE=requirements.txt
SCRIPT=main.py

# Check if environment exists
if conda env list | grep -q "$ENV_NAME"; then
    echo "Environment $ENV_NAME already exists"
else
    echo "Creating environment $ENV_NAME"
    conda create --name "$ENV_NAME" --file "$REQ_FILE"
fi

# Activate environment and run script
conda activate "$ENV_NAME"
streamlit run "$SCRIPT"