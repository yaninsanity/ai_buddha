#!/bin/bash

# Load the environment variables from the .env file
if [ -f .env ]; then
    export $(cat .env | xargs)
else
    echo ".env file not found. Please create one with your OpenAI API key."
    exit 1
fi

# Check if the OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "OPENAI_API_KEY is not set. Please check your .env file."
    exit 1
fi

# Create and activate a virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create a log directory if it doesn't exist
mkdir -p log

# Function to kill background processes on exit
cleanup() {
    echo "Stopping Flask and Gradio..."
    kill $FLASK_PID
    kill $GRADIO_PID
    exit 0
}

# Trap SIGINT (Ctrl+C) and SIGTERM to stop the background processes
trap cleanup SIGINT SIGTERM

# Start Flask application
echo "Starting Flask application..."
python app.py > log/flask_output.log 2> log/flask_error.log &
FLASK_PID=$!

# Start Gradio application (Assuming you have a Gradio interface in gradio_interface.py)
echo "Starting Gradio application..."
python gradio_interface.py > log/gradio_output.log 2> log/gradio_error.log &
GRADIO_PID=$!

# Wait a few seconds to give the processes time to start
sleep 5

# Check if Flask is running
if ps -p $FLASK_PID > /dev/null
then
    echo "Flask is running."
else
    echo "Flask failed to start. Check log/flask_error.log for details."
    kill $GRADIO_PID
    exit 1
fi

# Check if Gradio is running
if ps -p $GRADIO_PID > /dev/null
then
    echo "Gradio is running."
else
    echo "Gradio failed to start properly. Check log/gradio_error.log for details."
    kill $FLASK_PID
    exit 1
fi

# Keep the script running to allow Flask and Gradio to run
wait $FLASK_PID
wait $GRADIO_PID
