document.getElementById('questionForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const question = document.getElementById('question').value;
    
    const response = await fetch('/generate_response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
    });
    
    const data = await response.json();
    
    document.getElementById('response').textContent = data.response;
});
