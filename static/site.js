// Grab elements from the page
const outputBox = document.querySelector(".text-area");
const inputBox = document.querySelector(".input-box");
const enterButton = document.querySelector(".input-button");

// Disable input until intro finishes
inputBox.disabled = true;
enterButton.disabled = true;

// Append text to output
function writeToOutput(text) {
    outputBox.value += text + "\n\n";
    outputBox.scrollTop = outputBox.scrollHeight;
}

// Play chunks one at a time with a delay
async function playChunks(chunks, delay = 5000) {
    for (const chunk of chunks) {
        outputBox.value += chunk.trim() + ".\n\n";
        outputBox.scrollTop = outputBox.scrollHeight;
        await new Promise(resolve => setTimeout(resolve, delay));
    }
}

// Submit user input (turn)
async function submitInput() {
    const text = inputBox.value.trim();
    if (!text) return;

    let ended = false;

    inputBox.value = "";
    inputBox.disabled = true;
    enterButton.disabled = true;

    try {
        const response = await fetch("/input", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });

        const data = await response.json();

        if (!Array.isArray(data.chunks)) {
            throw new Error("Invalid chunk data from /input");
        }

        await playChunks(data.chunks);

        ended = !!data.is_over;
        if (ended) {
            writeToOutput("— The End —");
        }

    } catch (err) {
        console.error(err);
        writeToOutput("⚠️ Something went wrong sending your input.");
    } finally {
        if (!ended) {
            inputBox.disabled = false;
            enterButton.disabled = false;
            inputBox.focus();
        } else {
            inputBox.disabled = true;
            enterButton.disabled = true;
        }
    }
}

// Hook up input events
enterButton.addEventListener("click", submitInput);
inputBox.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        e.preventDefault();
        submitInput();
    }
});

// Start the game (intro)
async function startGame() {
    try {
        const response = await fetch("/start");
        const data = await response.json();

        if (!Array.isArray(data.chunks)) {
            throw new Error("Invalid chunk data from /start");
        }

        await playChunks(data.chunks);

    } catch (err) {
        console.error(err);
        writeToOutput("⚠️ Failed to start the game.");
    } finally {
        inputBox.disabled = false;
        enterButton.disabled = false;
        inputBox.focus();
    }
}

startGame();
