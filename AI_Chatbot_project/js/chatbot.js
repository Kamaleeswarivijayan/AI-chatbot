function appendMessage(message, sender) {
    const chatBox = document.getElementById("chatBox");
    const messageElement = document.createElement("div");
    messageElement.classList.add("message");
    messageElement.classList.add(sender.toLowerCase());
    messageElement.textContent = `${sender}: ${message}`;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage() {
    const userInput = document.getElementById("userInput").value;
    if (userInput.trim() === "") return;

    appendMessage(userInput, "Customer");
    document.getElementById("userInput").value = "";

    // Send user input to the backend via a POST request
    fetch("http://127.0.0.1:5000/ask", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userInput }),
    })
    .then(response => response.json())
    .then(data => {
        appendMessage(data.response, "Bot");
    })
    .catch(error => console.error("Error:", error));
}

// Allow the user to press Enter to send a message
function checkEnter(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}
