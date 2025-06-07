// frontend/script.js

document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    // FIX: Pointing to the correct server port
    const apiEndpoint = 'http://localhost:5001/chat';

    const sendMessage = async () => {
        const userMessage = userInput.value.trim();
        if (userMessage === '') return;

        // Display user message
        addMessage(userMessage, 'user-message');
        userInput.value = '';

        // Show loading indicator
        const loadingIndicator = addMessage('', 'bot-message loading-message');
        const dotFlashing = document.createElement('div');
        dotFlashing.className = 'dot-flashing';
        loadingIndicator.appendChild(dotFlashing);

        // Send message to backend
        try {
            const response = await fetch(apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userMessage }),
            });

            if (!response.ok) {
                // Try to get a more specific error from the backend if possible
                const errorData = await response.json().catch(() => null);
                const errorMessage = errorData ? errorData.error : `HTTP error! status: ${response.status}`;
                throw new Error(errorMessage);
            }

            const data = await response.json();
            const botResponse = data.response;
            
            // Remove loading indicator
            chatBox.removeChild(loadingIndicator);
            
            // Display bot response
            addMessage(botResponse, 'bot-message');

        } catch (error) {
            console.error('Error fetching chat response:', error);
             // Remove loading indicator
            chatBox.removeChild(loadingIndicator);
            addMessage(`Sorry, an error occurred: ${error.message}. Please check the console and ensure the backend server is running correctly.`, 'bot-message');
        }
    };

    const addMessage = (text, className) => {
        const messageContainer = document.createElement('div');
        messageContainer.className = `message ${className}`;
        
        if (!text && className.includes('loading-message')) {
            chatBox.appendChild(messageContainer);
            chatBox.scrollTop = chatBox.scrollHeight;
            return messageContainer;
        }

        const messageText = document.createElement('p');
        messageText.textContent = text;
        messageContainer.appendChild(messageText);
        chatBox.appendChild(messageContainer);
        
        // Scroll to the bottom of the chat box
        chatBox.scrollTop = chatBox.scrollHeight;
        return messageContainer;
    };

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});
