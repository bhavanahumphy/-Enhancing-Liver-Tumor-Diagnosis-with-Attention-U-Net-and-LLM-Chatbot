class ChatApp {
    constructor() {
        this.chatMessages = document.getElementById('chatMessages');
        this.userInput = document.getElementById('userInput');
        this.sendButton = document.getElementById('sendButton');
        this.clearButton = document.getElementById('clearHistory');
        this.chatHistory = [];
        
        // Configure marked options
        marked.setOptions({
            breaks: true,
            gfm: true,
            headerIds: false,
            mangle: false
        });
        
        this.initialize();
    }

    initialize() {
        this.loadChatHistory();
        
        this.sendButton.addEventListener('click', () => this.handleUserMessage());
        this.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.handleUserMessage();
        });
        this.clearButton.addEventListener('click', () => this.clearHistory());
    }

    loadChatHistory() {
        const savedHistory = localStorage.getItem('chatHistory');
        if (savedHistory) {
            this.chatHistory = JSON.parse(savedHistory);
            this.chatHistory.forEach(msg => this.displayMessage(msg.text, msg.sender, msg.isMarkdown));
        }
    }

    saveChatHistory() {
        localStorage.setItem('chatHistory', JSON.stringify(this.chatHistory));
    }

    clearHistory() {
        if (confirm('Are you sure you want to clear the chat history?')) {
            this.chatHistory = [];
            localStorage.removeItem('chatHistory');
            this.chatMessages.innerHTML = '';
            this.displayMessage('Chat history has been cleared.', 'assistant', false);
        }
    }

    markdownToSafeHTML(markdown) {
        // Convert markdown to HTML
        const rawHtml = marked.parse(markdown);
        // Sanitize the HTML
        return DOMPurify.sanitize(rawHtml);
    }

    async handleUserMessage() {
        const userMessage = this.userInput.value.trim();
        if (!userMessage) return;

        this.userInput.value = '';

        this.displayMessage(userMessage, 'user', false);
        this.chatHistory.push({ text: userMessage, sender: 'user', isMarkdown: false });

        try {
            const loadingId = this.displayLoadingMessage();

            const response = await fetch('http://127.0.0.1:8000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    query: userMessage,
                    chat_history: this.chatHistory
                })
            });

            this.removeLoadingMessage(loadingId);

            if (!response.ok) throw new Error('API request failed');

            const data = await response.json();
            
            this.displayMessage(data.data, 'assistant', true);
            this.chatHistory.push({ text: data.data, sender: 'assistant', isMarkdown: true });
            
            this.saveChatHistory();
            this.scrollToBottom();
        } catch (error) {
            console.error('Error:', error);
            this.displayMessage('I apologize, but I encountered an error. Please try again.', 'assistant', false);
        }
    }

    displayMessage(message, sender, isMarkdown) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);
        
        if (isMarkdown) {
            messageDiv.innerHTML = this.markdownToSafeHTML(message);
        } else {
            messageDiv.textContent = message;
        }
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    displayLoadingMessage() {
        const loadingDiv = document.createElement('div');
        loadingDiv.classList.add('message', 'assistant-message');
        loadingDiv.textContent = 'Thinking...';
        this.chatMessages.appendChild(loadingDiv);
        this.scrollToBottom();
        return loadingDiv;
    }

    removeLoadingMessage(loadingDiv) {
        loadingDiv.remove();
    }

    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
}

const chatApp = new ChatApp();