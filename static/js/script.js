function sendMessage() {
    const message = document.getElementById("userInput").value;

    fetch("/assistant", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerText = data.response;
    });
}
