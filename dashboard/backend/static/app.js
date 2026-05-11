async function fetchFunctions() {
  const resp = await fetch('/api/functions');
  if (!resp.ok) throw new Error('Failed to load functions');
  return resp.json();
}

function renderList(list) {
  const ul = document.getElementById('functions');
  ul.innerHTML = '';
  for (const fn of list) {
    const li = document.createElement('li');
    const h = document.createElement('h3');
    h.textContent = fn.name;
    const p = document.createElement('p');
    p.textContent = fn.description || '';
    li.appendChild(h);
    li.appendChild(p);
    ul.appendChild(li);
  }
}

function applyFilter(items) {
  const q = document.getElementById('filter').value.toLowerCase().trim();
  if (!q) return items;
  return items.filter(fn => (fn.name||'').toLowerCase().includes(q) || (fn.description||'').toLowerCase().includes(q));
}

document.addEventListener('DOMContentLoaded', async () => {
  try {
    const data = await fetchFunctions();
    const summary = document.getElementById('summary');
    summary.textContent = `Loaded ${data.length} functions.`;
    renderList(data);

    document.getElementById('filter').addEventListener('input', (e) => {
      const filtered = applyFilter(data);
      renderList(filtered);
      document.getElementById('summary').textContent = `Showing ${filtered.length} of ${data.length} functions.`;
    });
    // Chat UI wiring
    const messages = document.getElementById('messages');
    function appendMessage(author, text){
      const d = document.createElement('div');
      d.style.padding='6px'; d.style.marginBottom='6px';
      d.innerHTML = `<strong>${author}:</strong> ${text}`;
      messages.appendChild(d);
      messages.scrollTop = messages.scrollHeight;
    }

    document.getElementById('send_btn').addEventListener('click', async ()=>{
      const input = document.getElementById('chat_input');
      const text = input.value.trim();
      if(!text) return;
      appendMessage('You', text);
      // If text looks like a function name (no spaces) call simulate
      const payload = { message: text };
      if(!text.includes(' ')){
        payload.function = text;
        payload.params = {};
      }
      try{
        const r = await fetch('/api/chat', {method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(payload)});
        const j = await r.json();
        const responseText = JSON.stringify(j);
        appendMessage('System', responseText);
        speakText(responseText);
      }catch(err){
        const errorText = 'Error: '+err.message;
        appendMessage('System', errorText);
        speakText(errorText);
      }
      input.value='';
    });

    document.getElementById('tg_send_btn').addEventListener('click', async ()=>{
      const chatId = document.getElementById('telegram_chat_id').value.trim();
      const input = document.getElementById('chat_input').value.trim() || 'Test message from dashboard';
      if(!chatId){ appendMessage('System','Provide telegram chat id to send'); return }
      try{
        const r = await fetch('/api/telegram/send',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({chat_id:chatId,message:input})});
        const j = await r.json(); appendMessage('Telegram', JSON.stringify(j));
      }catch(err){ appendMessage('Telegram','Error: '+err.message) }
    });

    document.getElementById('voice_btn').addEventListener('click', startVoiceInput);

    // Voice functions
    function startVoiceInput() {
      const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
      recognition.lang = 'en-US';
      recognition.interimResults = false;
      recognition.maxAlternatives = 1;

      recognition.onstart = () => {
        appendMessage('System', 'Listening...');
      };

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        document.getElementById('chat_input').value = transcript;
        appendMessage('You (voice)', transcript);
        // Automatically send
        document.getElementById('send_btn').click();
      };

      recognition.onerror = (event) => {
        appendMessage('System', 'Voice recognition error: ' + event.error);
      };

      recognition.start();
    }

    function speakText(text) {
      const utterance = new SpeechSynthesisUtterance(text);
      window.speechSynthesis.speak(utterance);
    }
  } catch (err) {
    document.getElementById('summary').textContent = 'Error loading functions';
    console.error(err);
  }
});
