// Setup user ID if not already present
(function setupUserId() {
    let userId = localStorage.getItem("chatbot_user_id");
    if (!userId) {
        userId = "user_" + Math.random().toString(36).substring(2, 10);
        localStorage.setItem("chatbot_user_id", userId);
    }
})();

// Handle chat form submit
document.getElementById("chat-form").addEventListener("submit", async function (event) {
    event.preventDefault();

    const inputField = document.getElementById("user_input");
    const message = inputField.value.trim();
    if (!message) return;

    const chatBox = document.getElementById("chat-box");

    const userMsg = document.createElement("div");
    userMsg.classList.add("message", "user");
    userMsg.innerHTML = `<strong>User:</strong> ${message}`;
    chatBox.appendChild(userMsg);

    inputField.value = "";

    const response = await fetch("/send_message", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            user_input: message,
            user_id: localStorage.getItem("chatbot_user_id")
        })
    });

    const data = await response.json();

    const aiMsg = document.createElement("div");
    aiMsg.classList.add("message", "assistant");
    aiMsg.innerHTML = `<strong>Assistant:</strong> ${data.reply}`;
    chatBox.appendChild(aiMsg);

    chatBox.scrollTop = chatBox.scrollHeight;
});

// Handle reset button click
document.getElementById("reset-btn").addEventListener("click", async function () {
    const confirmed = confirm("Are you sure you want to reset the conversation?");
    if (!confirmed) return;

    const response = await fetch("/reset", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            user_id: localStorage.getItem("chatbot_user_id")
        })
    });

    if (response.ok) {
        const chatBox = document.getElementById("chat-box");
        chatBox.innerHTML = "";
        const systemMsg = document.createElement("div");
        systemMsg.classList.add("message", "system");
        systemMsg.innerHTML = `<strong>System:</strong> Ahoy! Start a new conversation.`;
        chatBox.appendChild(systemMsg);
    }
});
