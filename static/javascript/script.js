document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const inputSubmit = document.getElementById("inputSubmit");

    chatForm.addEventListener('submit', (event) => {
        if (userInput.value.trim() === '') {
            event.preventDefault(); // Empêche la soumission du formulaire
        }
    });

   userInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            if (userInput.value.trim() === '') {
                event.preventDefault(); // Empêche la soumission du formulaire
            } else {
                chatForm.submit();
            }
        }
    });


    userInput.focus();
});
