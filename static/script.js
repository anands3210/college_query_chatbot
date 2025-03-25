document.addEventListener("DOMContentLoaded", function () {
    const chatbox = document.getElementById("chatbox");
    const userInput = document.getElementById("userInput");
    let isVoiceInput = false;

    function sendMessage() {
        let userMessage = userInput.value.trim();
        if (userMessage === "") return;

        chatbox.innerHTML += `<p style="text-align: right; margin-left: 20%;"><strong>You:</strong> ${userMessage}</p>`;
        chatbox.scrollTop = chatbox.scrollHeight;
        userInput.value = "";

        fetch("/get_response", {
            method: "POST",
            body: new URLSearchParams({ "message": userMessage }),
            headers: { "Content-Type": "application/x-www-form-urlencoded" }
        })
        .then(response => response.json())
        .then(data => {
            chatbox.innerHTML += `<p style="text-align: left; margin-right: 20%;"><strong>Eva:</strong> ${data.response}</p>`;
            chatbox.scrollTop = chatbox.scrollHeight;
            if (isVoiceInput) {
                speakResponse(data.response);
            }
            isVoiceInput = false;
        })
        .catch(error => {
            console.error("Error:", error);
            chatbox.innerHTML += `<p style="text-align: left; margin-right: 20%;"><strong>Eva:</strong> Sorry, there was an error processing your request.</p>`;
        });
    }

    function startVoiceRecognition() {
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = "en-US";
        recognition.start();

        recognition.onresult = function (event) {
            const transcript = event.results[0][0].transcript;
            userInput.value = transcript;
            isVoiceInput = true;
            sendMessage();
        };

        recognition.onerror = function (event) {
            console.error("Speech recognition error:", event.error);
        };
    }

    function speakResponse(response) {
        const speech = new SpeechSynthesisUtterance(response);
        speech.lang = "en-US";

        // **Female voice select karne ka code**
        const voices = speechSynthesis.getVoices();
        const femaleVoice = voices.find(voice => voice.name.includes("Female") || voice.name.includes("Google UK English Female"));

        if (femaleVoice) {
            speech.voice = femaleVoice;
        }

        speechSynthesis.speak(speech);
    }

  
    speechSynthesis.onvoiceschanged = () => {
        speakResponse(""); // Just to trigger voice loading
    };

    userInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });

    document.querySelector("button").addEventListener("click", sendMessage);
    document.querySelector(".mic-button").addEventListener("click", startVoiceRecognition);
});
