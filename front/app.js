const API_URL = "http://localhost:8000";

const fileInput = document.getElementById("fileInput");
const documentsList = document.getElementById("documentsList");

const sendButton = document.getElementById("sendButton");
const messageInput = document.getElementById("messageInput");
const messages = document.getElementById("messages");


function renderDocuments(documents) {

    document.getElementById(
        "documentsTitle"
    ).textContent =
        `📂 Documentos (${documents.length})`;

    documentsList.innerHTML = "";

    documents.forEach(doc => {

        const card = document.createElement("div");

        card.className = "document-card";

        card.innerHTML = `
            <div class="document-name">
                📄 ${doc.filename}
            </div>

            <button
                class="delete-btn"
                onclick="deleteDocument(${doc.id})"
            >
                Eliminar
            </button>
        `;

        documentsList.appendChild(card);
    });

}

async function loadDocuments() {

    try {

        const response = await fetch(
            `${API_URL}/documents`
        );

        const documents = await response.json();

        renderDocuments(documents);

    } catch (error) {

        console.error(error);

    }

}

fileInput.addEventListener(
    "change",
    async () => {

        const file = fileInput.files[0];

        if (!file) {
            return;
        }

        const formData = new FormData();

        formData.append(
            "file",
            file
        );

        try {

            const response = await fetch(
                `${API_URL}/upload`,
                {
                    method: "POST",
                    body: formData
                }
            );

            if (!response.ok) {

                throw new Error(
                    "Error al subir archivo"
                );

            }

            await loadDocuments();

            fileInput.value = "";

        } catch (error) {
            console.error(error);
            alert(error.message);
        }
    }
);

async function deleteDocument(id) {

    try {

        const response = await fetch(
            `${API_URL}/documents/${id}`,
            {
                method: "DELETE"
            }
        );

        if (!response.ok) {

            throw new Error(
                "Error al eliminar documento"
            );

        }

        await loadDocuments();

    } catch (error) {

        console.error(error);

        alert(
            "No se pudo eliminar el documento"
        );

    }

}

/*Chat*/

sendButton.addEventListener(
    "click",
    sendMessage
);

messageInput.addEventListener(
    "keydown",
    (event) => {

        if (event.key === "Enter") {
            sendMessage();
        }
    }
);

async function sendMessage() {

    const text = messageInput.value.trim();

    if (!text) {
        return;
    }

    addMessage(
        text,
        "user"
    );

    messageInput.value = "";

    addMessage(
        "Pensando...",
        "bot"
    );

    const loadingMessage =
        messages.lastElementChild;

    try {
        sendButton.disabled = true;
        const response = await fetch(
            `${API_URL}/chat`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    question: text
                })
            }
        );

        const data = await response.json();
        loadingMessage.remove();

        addMessage(
            data.response,
            "bot"
        );

    } catch (error) {
        loadingMessage.remove();
        console.error(error);

        addMessage(
            "Error al consultar el chatbot.",
            "bot"
        );
    } finally {
        sendButton.disabled = false;
    }
}

function addMessage(text, type) {

    const div =
        document.createElement("div");

    div.classList.add(
        "message"
    );

    div.classList.add(
        type
    );

    div.innerHTML = marked.parse(text);

    messages.appendChild(div);

    messages.scrollTop = messages.scrollHeight;

}

/* Inicio*/

window.addEventListener(
    "load",
    () => {

        loadDocuments();

    }
);