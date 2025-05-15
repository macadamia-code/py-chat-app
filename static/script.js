const chatDiv = document.getElementById('chat');
const form = document.getElementById('chat-form');
const usernameInput = document.getElementById('username');
const contentInput = document.getElementById('content');
const reloadBtn = document.getElementById('reload-btn');

let latestTime = null; // 最新のメッセージ時刻

// メッセージを取得する
async function fetchMessages() {
    let url = '/api/get_messages';
    if (latestTime) {
        url += `?after=${encodeURIComponent(latestTime)}`;
    }

    const res = await fetch(url);
    const data = await res.json();

    if (data.length > 0) {
        // 新着メッセージが存在する場合、追加で表示する
        const html = data.map(msg => {
            const date = new Date(msg.created_at);
            const dateStr = date.toLocaleString('ja-JP', { timeZone: 'Asia/Tokyo' });
            return `<p>[${dateStr}] <b>${msg.username}</b>： ${msg.content}</p>`;
        }).join('');
        chatDiv.insertAdjacentHTML('afterbegin', html);

        // 最新メッセージの書込み日時を更新する
        latestTime = data[0].created_at;
    }
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const res = await fetch('/api/send_message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: usernameInput.value,
            content: contentInput.value,
            after: latestTime,
        })
    });

    const data = await res.json();
    if (data.length > 0) {
        const html = data.map(msg => {
            const date = new Date(msg.created_at);
            const dateStr = date.toLocaleString('ja-JP', { timeZone: 'Asia/Tokyo' });
            return `<p>[${dateStr}] <b>${msg.username}</b>： ${msg.content}</p>`;
        }).join('');
        chatDiv.insertAdjacentHTML('afterbegin', html);

        latestTime = data[0].created_at;
    }

    contentInput.value = '';
});
  

// 手動リロードボタン
reloadBtn.addEventListener('click', fetchMessages);

// 初回読み込み時に1回だけ表示
(async () => {
    latestTime = null;
    await fetchMessages();
})();
