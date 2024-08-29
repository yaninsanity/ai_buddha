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
pip install -r requirements.txt

# Create a log directory if it doesn't exist
mkdir -p log

# Start Flask application
echo "Starting Flask application..."
nohup python app.py > log/flask_output.log 2> log/flask_error.log &

# Start Gradio application (Assuming you have a Gradio interface in gradio_interface.py)
echo "Starting Gradio application..."
nohup python gradio_interface.py > log/gradio_output.log 2> log/gradio_error.log &

echo "Both Flask and Gradio applications have been started."

# Wait a few seconds to give the processes time to start
sleep 5

# Check if Flask and Gradio are running
if pgrep -f "python app.py" > /dev/null
then
    echo "Flask is running."
else
    echo "Flask failed to start. Check log/flask_error.log for details."
fi

# Check Gradio status by looking for specific error patterns in the log
if ! tail -n 10 log/gradio_error.log | grep -q "Traceback\|ModuleNotFoundError"; then
    echo "Gradio is running."
else
    echo "Gradio failed to start properly. Check log/gradio_error.log for details."
fi