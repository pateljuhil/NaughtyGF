let username = localStorage.getItem("username");

if (!username) {
    username = prompt("Enter your name to visit website:");
    if (!username || username.trim() === "") {
        username = "Anonymous";
    }
    localStorage.setItem("username", username);
}


function sendMessage() {
    const input = document.getElementById("user-input");
    const message = input.value.trim();
    if (!message) return;

    const chatBox = document.getElementById("chat-box");

    // Add user message bubble
    const userBubble = document.createElement("div");
    userBubble.className = "message user";
    userBubble.innerHTML = `<b>You:</b><br>${message}`;
    chatBox.appendChild(userBubble);

    // Scroll to bottom
    chatBox.scrollTop = chatBox.scrollHeight;
    input.value = "";

    // Send to backend
    fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
            message: message, 
            username: username })
    })
    .then(res => res.json())
    .then(data => {
        const botBubble = document.createElement("div");
        botBubble.className = "message bot";
        botBubble.innerHTML = `<b>Sweety:</b><br>${data.reply}`;
        chatBox.appendChild(botBubble);
        chatBox.scrollTop = chatBox.scrollHeight;
    });
}
