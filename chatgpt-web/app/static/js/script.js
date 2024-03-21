$(document).ready(function() {
    $('#send-button').click(function() {
        let userInput = $('#user-input').val();
        if (userInput.trim() !== '') {
            appendMessage(userInput, 'right');
            $('#user-input').val('');

            $.ajax({
                url: '/ask',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ message: userInput }),
                success: function(response) {
                    appendMessage(response.answer, 'left');
                },
                error: function(error) {
                    console.error("Error:", error);
                }
            });
        }
    });
});

function appendMessage(message, side) {
    let alignClass = side === 'right' ? 'text-right' : '';
    let messageElement = `<div class="mb-2 ${alignClass}">${message}</div>`;
    $('#chat-area').append(messageElement);
    $('#chat-area').scrollTop($('#chat-area')[0].scrollHeight);
}
