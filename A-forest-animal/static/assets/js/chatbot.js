(function () {

var socket = new WebSocket("ws://localhost:5000/echo");
var form = document.getElementById("chat-form");
var messageField = document.getElementById('chat-message');
var diaogs = document.getElementById('chat-dialogs');

socket.onopen = function () {
  showMessage('안녕하세요! 저는 애완견 건강 상담을 담당하는 AI 상담사입니다. 무슨 도움을 드릴까요?', 'bot');
};

socket.onmessage = function (event) {
  showMessage(event.data, 'bot');
};

form.onsubmit = handleFormSubmit;
messageField.onkeydown = handleTextareaKeyDown;

function handleFormSubmit(event) {
  event.preventDefault();
  const message = messageField.value;
  socket.send(message);
  showMessage(message, 'user');
  messageField.value = "";
}

function handleTextareaKeyDown(event) {
  if (event.keyCode === 13 && !event.shiftKey) {
    event.preventDefault();
    handleFormSubmit(event);
  }
}

function showMessage(message, speaker) {
  var label = (speaker == 'user') ? '나' : '봇';
  var dialog = document.createElement('p');
  dialog.classList.add(`chat-dialog-${speaker}`);
  dialog.classList.add('chat-dialog');
  dialog.innerHTML = `<span class="chat-speaker-${speaker} chat-speaker">${label}: </span>`;
  dialog.appendChild(document.createTextNode(message));
  diaogs.appendChild(dialog);
  window.scrollTo(0, document.body.scrollHeight);
}

})();
