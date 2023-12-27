// Initialize an array to store the conversation history
let conversationHistory = [];

// Function to load the conversation history from localStorage
function loadConversationHistory() {
    const storedHistory = localStorage.getItem("conversationHistory");
    if (storedHistory) {
        conversationHistory = JSON.parse(storedHistory);
        conversationHistory.forEach(message => {
            addMessage(message.content, message.role === "user" ? "user" : "bot");
        });
    } else {
        // Display the welcome message if there's no stored history
        displayWelcomeMessage();
    }
}

function clearHistory() {
    // Clear the chat container
    const chatContainer = document.getElementById("chat-container");
    chatContainer.innerHTML = '';

    // Clear the conversation history array
    conversationHistory = [];

    // Clear the conversation history from localStorage
    localStorage.removeItem("conversationHistory");

    // Display the welcome message again
    displayWelcomeMessage();
}



// Function to save the conversation history to localStorage
function saveConversationHistory() {
    localStorage.setItem("conversationHistory", JSON.stringify(conversationHistory));
}

// Function to add a message to the chat container
function addMessage(message, sender) {
    const chatContainer = document.getElementById("chat-container");
    const messageElement = document.createElement("div");
    messageElement.className = `message ${sender}-message`;

    const messageText = document.createElement("div");
    messageText.className = "message-text";
    messageText.innerHTML = message.replace(/\n/g, "<br>");

    messageElement.appendChild(messageText);
    chatContainer.appendChild(messageElement);

    // Scroll to the bottom of the chat container
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Function to display the welcome message from the bot
function displayWelcomeMessage() {
    const welcomeMessage = "Hello! I'm a math tutor. How can I help you today?";
    addMessage(welcomeMessage, "bot");
}

// Function to display a temporary "Generating response..." message from the bot
function displayGeneratingMessage() {
    const generatingMessage = "Generating response...";
    addMessage(generatingMessage, "bot");
    return generatingMessage;
}

// Function to remove the "Generating response..." message from the chat container
function removeGeneratingMessage(generatingMessage) {
    const chatContainer = document.getElementById("chat-container");
    chatContainer.removeChild(chatContainer.lastChild);
}

// Event listener for the form submission
document.getElementById("chat-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const input = document.getElementById("message");
    const message = input.value.trim();

    // Do not proceed if the message is empty
    if (message.length === 0) {
        return;
    }

    // Display the user's message and update the conversation history
    addMessage(message, "user");
    conversationHistory.push({ role: "user", content: message });
    saveConversationHistory(); // Save the updated conversation history to localStorage

    input.value = "";
    input.focus();

    // Display the "Generating response..." message
    const generatingMessage = displayGeneratingMessage();

    // Send a request to the server to generate a response
    fetch("/generate", {
        method: "POST",
        body: JSON.stringify({ message: message, history: conversationHistory }),
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => {
        // Remove the "Generating response..." message and display the bot's response
        removeGeneratingMessage(generatingMessage);
        addMessage(data, "bot");
        conversationHistory.push({ role: "assistant", content: data });
        saveConversationHistory(); // Save the updated conversation history to localStorage
    });
});

// Event listener for the "Clear History" button
document.getElementById("clear-history").addEventListener("click", function() {
    clearHistory();
});



// Load the conversation history when the page loads
loadConversationHistory();