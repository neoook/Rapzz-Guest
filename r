#!/bin/bash

# --- CONFIG ---
APP_NAME="neobox-app"

echo "🔥 Memulai kuli digital... Membangun $APP_NAME"

# 1. Create Folder Structure
mkdir -p $APP_NAME/api
mkdir -p $APP_NAME/public

cd $APP_NAME

# 2. Generate package.json
cat <<EOF > package.json
{
  "name": "neobox-app",
  "version": "1.0.0",
  "main": "api/index.js",
  "dependencies": {
    "axios": "^1.6.0"
  }
}
EOF

# 3. Generate api/index.js (Logic Gabungan)
cat <<EOF > api/index.js
import axios from 'axios';

const BASE_URL = "https://sapi.dramaboxdb.com";

const getToken = async () => {
    const res = await axios.get("https://dramabox-token.vercel.app/token");
    return res.data;
};

const getHeaders = (tokenData, cid = "DRA1000042") => ({
    "User-Agent": "okhttp/4.10.0",
    "Content-Type": "application/json",
    "tn": \`Bearer \${tokenData.token}\`,
    "device-id": tokenData.deviceid,
    "package-name": "com.storymatrix.drama"
});

export default async function handler(req, res) {
    const { type, q, id, page = 1, ep = 1 } = req.query;
    try {
        const auth = await getToken();
        if (type === 'latest') {
            const result = await axios.post(\`\${BASE_URL}/drama-box/he001/theater\`, {
                newChannelStyle: 1, isNeedRank: 1, pageNo: parseInt(page), index: 1, channelId: 43
            }, { headers: getHeaders(auth) });
            return res.status(200).json(result.data.data.newTheaterList.records);
        }
        if (type === 'search') {
            const result = await axios.post(\`\${BASE_URL}/drama-box/search/suggest\`, { keyword: q }, { headers: getHeaders(auth) });
            return res.status(200).json(result.data.data.suggestList);
        }
        if (type === 'play') {
            const result = await axios.post(\`\${BASE_URL}/drama-box/chapterv2/batch/load\`, {
                index: parseInt(ep), bookId: id, boundaryIndex: 0, loadDirection: 0
            }, { headers: getHeaders(auth, "DRA1000000") });
            const stream = result.data.data.chapterList[0]?.cdnList[0];
            return res.status(200).json({ url: stream });
        }
        res.status(400).json({ error: "Invalid type" });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
}
EOF

# 4. Generate public/index.html (UI & Auto-Scroll)
cat <<EOF > public/index.html
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NeoBox</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background: #0b0f19; color: #f8fafc; }
        .card { background: #1e293b; border-radius: 12px; overflow: hidden; transition: 0.3s; cursor: pointer; border: 1px solid #334155; }
        .card:hover { border-color: #3b82f6; transform: translateY(-5px); }
    </style>
</head>
<body class="p-6">
    <div class="max-w-6xl mx-auto">
        <div class="flex flex-col md:flex-row justify-between items-center mb-10 gap-4">
            <h1 class="text-4xl font-black text-blue-500 italic">NEOBOX</h1>
            <input id="search" type="text" placeholder="Search drama..." class="w-full md:w-80 p-3 rounded-lg bg-slate-800 outline-none focus:ring-2 focus:ring-blue-500 border-none text-white">
        </div>
        <div id="grid" class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-5"></div>
        <div id="loader" class="text-center py-10 opacity-0">Loading moar drama...</div>
    </div>
    <div id="pWrap" class="fixed inset-0 bg-black/90 hidden flex flex-col items-center justify-center z-50 p-4">
        <button onclick="closeV()" class="absolute top-5 right-5 text-white text-xl">✕ Close</button>
        <video id="vid" controls class="w-full max-w-4xl rounded-lg border border-white/10"></video>
    </div>
    <script>
        let page = 1; let loading = false;
        const grid = document.getElementById('grid');
        const search = document.getElementById('search');

        async function load(isSearch = false) {
            if (loading) return; loading = true;
            document.getElementById('loader').style.opacity = 1;
            const q = search.value;
            const url = isSearch ? \`/api?type=search&q=\${q}\` : \`/api?type=latest&page=\${page}\`;
            try {
                const r = await fetch(url); const data = await r.json();
                if (page === 1 || isSearch) grid.innerHTML = '';
                data.forEach(d => {
                    const el = document.createElement('div'); el.className = 'card p-2';
                    el.onclick = () => play(d.bookId);
                    el.innerHTML = \`<img src="\${d.cover}" class="w-full aspect-[3/4] object-cover rounded-lg mb-2"><p class="text-sm font-bold truncate">\${d.title}</p>\`;
                    grid.appendChild(el);
                });
            } catch (e) {}
            loading = false; document.getElementById('loader').style.opacity = 0;
        }

        async function play(id) {
            const r = await fetch(\`/api?type=play&id=\${id}\`); const data = await r.json();
            if(data.url) { 
                document.getElementById('vid').src = data.url; 
                document.getElementById('pWrap').classList.remove('hidden'); 
                document.getElementById('vid').play();
            } else { alert("Can't play this one, boss."); }
        }

        function closeV() { document.getElementById('vid').pause(); document.getElementById('pWrap').classList.add('hidden'); }
        
        window.onscroll = () => { if(window.innerHeight + window.scrollY >= document.body.offsetHeight - 700 && !search.value) { page++; load(); } };
        search.oninput = () => { page = 1; load(!!search.value); };
        load();
    </script>
</body>
</html>
EOF

# 5. Install Dependencies
echo "📦 Installing axios via npm..."
npm install

echo "✅ SELESAI! Folder '$APP_NAME' sudah siap."
echo "💡 Tinggal push ke GitHub terus konek ke Vercel, atau jalankan 'vercel' di dalem folder."
