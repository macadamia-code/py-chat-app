const chatDiv = document.getElementById('chat');
const form = document.getElementById('chat-form');
const usernameInput = document.getElementById('username');
const contentInput = document.getElementById('content');
const reloadBtn = document.getElementById('reload-btn');

// メッセージを取得する
async function fetchMessages() {
    let url = '/api/get_messages';

    const res = await fetch(url);
    const data = await res.json();

    const html = data.map(msg => {
        const date = new Date(msg.created_at);
        const dateStr = date.toLocaleString('ja-JP', { timeZone: 'Asia/Tokyo' });
        return `<p>[${dateStr}] <b>${msg.username}</b>： ${msg.content}</p>`;
    }).join('');

    chatDiv.innerHTML = '';
    chatDiv.insertAdjacentHTML('afterbegin', html);
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const res = await fetch('/api/send_message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: usernameInput.value,
            content: contentInput.value,
        })
    });

    const data = await res.json();

    const html = data.map(msg => {
        const date = new Date(msg.created_at);
        const dateStr = date.toLocaleString('ja-JP', { timeZone: 'Asia/Tokyo' });
        return `<p>[${dateStr}] <b>${msg.username}</b>： ${msg.content}</p>`;
    }).join('');

    chatDiv.innerHTML = '';
    chatDiv.insertAdjacentHTML('afterbegin', html);

    contentInput.value = '';
});
  

// 手動リロードボタン
reloadBtn.addEventListener('click', fetchMessages);

// 初回読み込み時に1回だけ表示
(async () => {
    latestTime = null;
    await fetchMessages();
})();
