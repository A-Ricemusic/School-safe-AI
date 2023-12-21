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
    messages = [{"role": msg["role"], "content": msg["content"]} for msg in history]
    # Append the system message from the "system_card.txt" file
    messages.append({"role": "system", "content": system})

    # Call the OpenAI API to generate a response using the gpt-3.5-turbo Turbo model
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1000,
        n=1,
        temperature=1,
    )
    # Extract the generated AI message from the response
    ai_message = response.choices[0].message.content
   
    # Return the AI message as a JSON response
    return jsonify(ai_message)


# Start the Flask application, listening on all interfaces and port 8080
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
