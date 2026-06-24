#!/usr/bin/env bash
# Make sure python3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is required to run the bootstrapping script."
    exit 1
fi

# Run the python script with all passed arguments
python3 "$(dirname "$0")/bootstrap.py" "$@"
