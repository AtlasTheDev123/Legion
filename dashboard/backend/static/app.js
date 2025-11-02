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
        appendMessage('System', JSON.stringify(j));
      }catch(err){
        appendMessage('System', 'Error: '+err.message);
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

    document.getElementById('tg_call_btn').addEventListener('click', async ()=>{
      const phone = document.getElementById('telegram_chat_id').value.trim();
      const input = document.getElementById('chat_input').value.trim() || 'Test call from dashboard';
      if(!phone){ appendMessage('System','Provide phone number to call'); return }
      try{
        const r = await fetch('/api/telegram/call',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({phone:phone,message:input})});
        const j = await r.json(); appendMessage('Call', JSON.stringify(j));
      }catch(err){ appendMessage('Call','Error: '+err.message) }
    });
  } catch (err) {
    document.getElementById('summary').textContent = 'Error loading functions';
    console.error(err);
  }
});
