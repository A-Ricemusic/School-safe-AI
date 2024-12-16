// index.js (for chat functionality)
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
        displayWelcomeMessage();
    }
}

function clearHistory() {
    const chatContainer = document.getElementById("chat-container");
    chatContainer.innerHTML = '';
    conversationHistory = [];
    localStorage.removeItem("conversationHistory");
    displayWelcomeMessage();
}

function saveConversationHistory() {
    localStorage.setItem("conversationHistory", JSON.stringify(conversationHistory));
}

function addMessage(message, sender) {
    const chatContainer = document.getElementById("chat-container");
    const messageElement = document.createElement("div");
    messageElement.className = `message ${sender}-message`;

    const messageText = document.createElement("div");
    messageText.className = "message-text";
    messageText.innerHTML = message.replace(/\n/g, "<br>");

    messageElement.appendChild(messageText);
    chatContainer.appendChild(messageElement);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function displayWelcomeMessage() {
    const welcomeMessage = "Hello! I'm a k-12 school tutor. How can I help you today?";
    addMessage(welcomeMessage, "bot");
}

function displayGeneratingMessage() {
    const generatingMessage = "Generating response...";
    addMessage(generatingMessage, "bot");
    return generatingMessage;
}

function removeGeneratingMessage(generatingMessage) {
    const chatContainer = document.getElementById("chat-container");
    chatContainer.removeChild(chatContainer.lastChild);
}

document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById("chat-form");
    if (chatForm) {
        loadConversationHistory();

        chatForm.addEventListener("submit", function(event) {
            event.preventDefault();

            const input = document.getElementById("message");
            const message = input.value.trim();

            if (message.length === 0) return;

            addMessage(message, "user");
            conversationHistory.push({ role: "user", content: message });
            saveConversationHistory();

            input.value = "";
            input.focus();

            const generatingMessage = displayGeneratingMessage();

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
                removeGeneratingMessage(generatingMessage);
                addMessage(data, "bot");
                conversationHistory.push({ role: "assistant", content: data });
                saveConversationHistory();
            });
        });

        const clearHistoryButton = document.getElementById("clear-history");
        if (clearHistoryButton) {
            clearHistoryButton.addEventListener("click", clearHistory);
        }
    }
});