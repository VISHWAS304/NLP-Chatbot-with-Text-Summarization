const toggleChatbotButton = document.getElementById('toggle-chatbot');
const chatbotFrame = document.getElementById('chatbot-frame');
const minimizedChatbotImage = document.getElementById('minimized-chatbot-image');

let chatbotVisible = true;

toggleChatbotButton.addEventListener('click', () => {
    if (chatbotVisible) {
        chatbotFrame.style.display = 'none';
        minimizedChatbotImage.style.display = 'block';
        toggleChatbotButton.textContent = 'Show Chat';
    } else {
        chatbotFrame.style.display = 'block';
        minimizedChatbotImage.style.display = 'none';
        toggleChatbotButton.textContent = 'Hide Chat';
    }
    chatbotVisible = !chatbotVisible;
});