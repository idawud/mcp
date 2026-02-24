#!/bin/bash

# Configuration
VENV_DIR=".venv"
SERVER_FILE=$2

# Function to activate or create venv
prepare_venv() {
    if [ ! -d "$VENV_DIR" ]; then
        echo "🌐 Creating virtual environment..."
        python3 -m venv "$VENV_DIR"
    fi
    source "$VENV_DIR"/bin/activate
}

# Function to build the environment and install dependencies
build() {
    prepare_venv
    if [ -f "requirements.txt" ]; then
        echo "📦 Installing dependencies..."
        pip install --upgrade pip
        pip install -r requirements.txt
    else
        echo "⚠️  requirements.txt not found. Installing base mcp library..."
        pip install mcp
    fi
    echo "✅ Build complete."
}

# Function to inspect a server file with MCP Inspector
inspect() {
    if [ -z "$SERVER_FILE" ]; then
            echo "❌ Error: Please provide a server file. Usage: ./setup.sh inspect server.py"
            exit 1
        fi
        prepare_venv
        echo "🔍 Starting MCP Inspector for $SERVER_FILE..."
        npx @modelcontextprotocol/inspector python3 "$SERVER_FILE"
}

# Function to run a specific python client script
run() {
    if [ -z "$SERVER_FILE" ]; then
        echo "❌ Error: Please provide a client script. Usage: ./setup.sh run client.py"
        exit 1
    fi
    prepare_venv
    echo "🚀 Running MCP Client: $SERVER_FILE..."
    python3 "$SERVER_FILE"
}

# Function to display usage information
default() {
    echo "Usage: $0 {build|inspect|run} [file]"
    echo "  build   - Setup venv and install requirements"
    echo "  inspect - Debug a server file with MCP Inspector"
    echo "  run     - Run a specific python client script"
    exit 1
}

# Main entry point
case "$1" in
    build) build ;;
    inspect) inspect ;;
    run) run ;;
    *) default ;;
esac