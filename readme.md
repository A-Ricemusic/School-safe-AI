# School-Safe Tutoring AI

A dedicated, school-safe AI tutor designed to help students understand their coursework rather than just providing the final answers. Using this AI, learners receive detailed explanations, clarifications, and gentle nudges in the right direction, all tailored to improve critical thinking and problem-solving skills.

## Table of Contents
- [About the AI](#about-the-ai)
- [Features](#features)
- [Getting Started](#getting-started)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## About the AI
This AI serves as an educational assistant that supports students by guiding them through their questions. It does not simply provide the finished solution; instead, it explains concepts, offers hints, and encourages the student to arrive at their own understanding. The result is a stronger grasp of the material and greater confidence in their ability to tackle academic challenges.

### Objective
- Promote Understanding: Offer thorough, step-by-step explanations and clarifications.
- Encourage Independence: Provide hints and insights rather than completing the work for the student.

## Features
- Contextual Assistance: Guidance tailored to the student’s current question or topic.
- Non-Solution Answers: Constructive hints and reasoning without handing over the final answer.
- Clear, Age-Appropriate Language: Accessible explanations suitable for various educational levels.
- Interactive Support: Encourages follow-up questions for deeper exploration and comprehension.
- Respectful and Inclusive: Maintains a positive, respectful tone suitable for a school environment.

## Getting Started

### Prerequisites
- Python 3.8+ installed on your system
- pip (included with most Python installations)
- An OpenAI API Key (required to access the model’s capabilities)
- Flask (a Python microframework for serving the application)

### Installation & Run
1. Clone the repository:
   `git clone https://github.com/your-username/school-safe-tutoring-ai.git`
   `cd school-safe-tutoring-ai`

2. Install dependencies:
   `pip install -r requirements.txt`

3. Set your OpenAI API Key:
   `export OPENAI_API_KEY=your_openai_api_key`

4. Run the Flask app:
   `flask run`

After starting the server, open your browser and navigate to:
`http://localhost:5000`

## Technologies Used
- Python & Flask: Serving the application and managing routing
- OpenAI API: Powering the language understanding and response generation
- HTML/CSS/JavaScript: Delivering a clean, accessible web interface

## Contributing
Contributions are always welcome! To contribute:
1. Fork this repository on GitHub.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with a clear, descriptive message.
4. Push to your fork and open a Pull Request, explaining your changes.

Your input helps make the tutoring experience more effective and engaging.

## License
This project is licensed under the MIT License. Please review the license for details on permitted usage and distribution.

---

The app was created using the Flask API. It was mainly built in Python and leverages the OpenAI API for its intelligent responses.


### Open AI Set up Documentation provided for more instructions/clarity

# ChatGPT Web Application

This is a simple web application that uses OpenAI's ChatGPT to generate responses based on user input. The application is built using Flask (Python) as the backend and JavaScript for the frontend.


## Requirements

- Python 3.7 or higher
- Flask
- OpenAI Python library


## Installation

1. Clone the repository:

        git clone https://github.com/hopthings/chatgpt_webapp.git
        cd chatgpt_webapp


2. Install the required packages:

        pip install -r requirements.txt


## API Key

Before running the application, you need to set up your OpenAI API key as an environment variable. Replace `your_api_key_here` with your actual OpenAI API key.

For Unix-based systems (Linux and macOS):

    ```bash
    export OPENAI_API_KEY="your_api_key_here"

## System card

You can modify the behaviour of chatGPT with a system card. It sets the context, tone, or behavior for the AI assistant throughout the conversation. By providing a system card at the beginning of a conversation, users can give high-level guidance to the AI model about how they want the interaction to proceed.

e.g.

    You are a helpful assistant that speaks like Shakespeare.

The example used in the source code is for "chatSEO" a digital marketing expert.  Feel free to modify as meets your own needs. (Note you should also change the title/H1 header in the templates/index.html to match your needs)

To modify the system card, simply change the contents of "system_card.txt"

## Running the Application

After setting the API key environment variable, run the application using the following command:

    python app.py

The application will start on http://0.0.0.0:8080/. Open the link in your browser to interact with the ChatGPT web application.


## Deployment on a Unix server

To deploy the application on a Unix server and make sure it loads on boot, follow these steps:

1. Set up a virtual environment and install the required packages:

        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt

2. Create a systemd service file:

        sudo nano /etc/systemd/system/chatgpt_webapp.service

3. Add the following content to the service file, replacing your_api_key_here with your actual OpenAI API key and /path/to/chatgpt-webapp with the absolute path to the application directory:

        [Unit]
        Description=ChatGPT Web Application
        After=network.target

        [Service]
        User=your_unix_username
        Environment=OPENAI_API_KEY="your_api_key_here"
        WorkingDirectory=/path/to/chatgpt_webapp
        ExecStart=/path/to/chatgpt_webapp/venv/bin/python app.py
        Restart=always

        [Install]
        WantedBy=multi-user.target

4. Save and close the file.
5. Reload the systemd manager configuration:

        sudo systemctl daemon-reload

6. Enable and start the service:

        sudo systemctl enable chatgpt_webapp
        sudo systemctl start chatgpt_webapp


The ChatGPT web application is now running as a service on your Unix server and will automatically start on boot.
