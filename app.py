import os

from openai import OpenAI
from flask import Flask, jsonify, render_template, request, session



# Create a Flask application instance
app = Flask(__name__)
# Generate a random secret key for the Flask application
app.secret_key = os.urandom(24)
# Set the OpenAI API key from the environment variable
client = OpenAI(
api_key = ""
)
# Read the content of the "system_card.txt" file
with open("system_card.txt", "r") as file:
    system = file.read()

# Define the route for the root URL, rendering the index.html template
@app.route("/")
def index():
    return render_template("index.html")


# Define the route for generating a response using the OpenAI API
# The route accepts POST requests
@app.route("/generate", methods=["POST"])
def generate():
    # Get the data from the incoming request in JSON format
    data = request.get_json()
    # Extract the user message and conversation history from the request data
    user_message = data["message"]
    history = data["history"]

    # Create a list of message dictionaries for the OpenAI API
    messages = [{"role": "system", "content": system}]
    # Append the system message from the "system_card.txt" file
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})

    # Call the OpenAI API to generate a response using the gpt-4 
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=2000,
        n=1,
        temperature=0,
    )
    # Extract the generated AI message from the response
    ai_message = response.choices[0].message.content
   
    # Return the AI message as a JSON response
    return jsonify(ai_message)


# Start the Flask application, listening on all interfaces and port 8080
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
