

/* ---------------- API HELPER ---------------- */
async function api(path, opts = {}) {
  const res = await fetch('/api/' + path, opts);
  return res.json();
}

/* ---------- CLOTHING TYPES ---------- */
const CLOTHING_TYPES = [
  'top','shirt','t-shirt','blouse',
  'pants','jeans','trousers','shorts',
  'skirt','frock','dress','gown',
  'kurti','chudidhar','saree','lehenga',
  'jacket','sweater','coat','outer',
  'dupatta','shawl',
  'shoes','heels','flats','sandals',
  'unknown'
];

/* ---------------- PAGE SWITCH ---------------- */
function showPage(page) {
  document.getElementById('homePage').style.display = 'none';
  document.getElementById('wardrobePage').style.display = 'none';
  document.getElementById('outfitsPage').style.display = 'none';
  document.getElementById('historyPage').style.display = 'none';

  if (page === 'home') {
    document.getElementById('homePage').style.display = 'block';
  }
  if (page === 'wardrobe') {
    document.getElementById('wardrobePage').style.display = 'block';
  }
  if (page === 'outfits') {
    document.getElementById('outfitsPage').style.display = 'block';
  }
  if (page === 'history') {
    document.getElementById('historyPage').style.display = 'block';
    loadHistory();   // 🔥 Load only when clicked
  }
}


/* ---------------- UPLOAD ---------------- */
document.getElementById('uploadBtn').onclick = async () => {
  const f = document.getElementById('imageInput').files[0];
  if (!f) return alert('Choose an image first');

  const fd = new FormData();
  fd.append('image', f);

  await fetch('/api/upload', { method: 'POST', body: fd });
  document.getElementById('imageInput').value = '';
  loadItems();
};

/* ---------------- LOAD WARDROBE ---------------- */
async function loadItems() {
  const items = await api('items');
  const div = document.getElementById('items');
  div.innerHTML = '';

  items.forEach(it => {
    const card = document.createElement('div');
    card.className = 'card';

    const img = document.createElement('img');
    img.src = it.url;

    const meta = document.createElement('div');
    meta.className = 'meta';
    meta.innerText = `${it.category} • worn: ${it.times_worn}`;

    const select = document.createElement('select');
    CLOTHING_TYPES.forEach(t => {
      const o = document.createElement('option');
      o.value = t;
      o.innerText = t;
      if (t === it.category) o.selected = true;
      select.appendChild(o);
    });

    select.onchange = async () => {
      await api('update_category', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ item_id: it.id, category: select.value })
      });
      loadItems();
    };

    const wornBtn = document.createElement('button');
    wornBtn.innerText = '👣 Worn +1';
    wornBtn.onclick = async () => {
      await api('mark_worn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ item_id: it.id })
      });
      loadItems();
    };

    const favBtn = document.createElement('button');
    favBtn.innerText = it.favorited ? '⭐ Favorited' : '☆ Favorite';
    favBtn.onclick = async () => {
      await api('favorite', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ item_id: it.id })
      });
      loadItems();
    };

    const delBtn = document.createElement('button');
    delBtn.innerText = '🗑 Delete';
    delBtn.onclick = async () => {
      if (!confirm('Delete this item?')) return;
      await api('delete_item', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ item_id: it.id })
      });
      loadItems();
    };

    card.append(img, meta, select, wornBtn, favBtn, delBtn);
    div.appendChild(card);
  });
}

/* ---------------- GENERATE OUTFITS ---------------- */
document.getElementById('recommendBtn').onclick = async () => {
  const event = document.getElementById('eventSelect').value;
  const weather = document.getElementById('weatherSelect').value;
  const div = document.getElementById('outfits');

  div.innerHTML = '';

  const data = await api('recommend', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ event, weather })
  });

  showPage('outfits');

  if (!data.outfits || data.outfits.length === 0) {
    div.innerHTML = `<div class="notice">❌ ${data.message}</div>`;
    return;
  }

  data.outfits.forEach((o, idx) => {
    const card = document.createElement('div');
    card.className = 'card outfit';

    const title = document.createElement('div');
    title.className = 'meta';
    title.innerText = `Outfit ${idx + 1}`;
    card.appendChild(title);

    const imagesWrap = document.createElement('div');
    imagesWrap.className = 'outfit-images';

    o.items.forEach(it => {
      const img = document.createElement('img');
      img.src = `/image/${it.id}`;
      imagesWrap.appendChild(img);
    });

    card.appendChild(imagesWrap);

    const why = document.createElement('div');
    why.className = 'outfit-why';
    why.innerText = o.justification;
    card.appendChild(why);

    div.appendChild(card);
  });

     // 🔥 Refresh history after generating
};

/* ---------------- LOAD HISTORY ---------------- */
/* ---------------- LOAD HISTORY ---------------- */
async function loadHistory() {
  const history = await api('history');
  const div = document.getElementById('history');

  if (!div) return;

  div.innerHTML = '';

  if (!history || history.length === 0) {
    div.innerHTML = `<div class="notice">No outfit history yet.</div>`;
    return;
  }

  history.forEach(entry => {
    const card = document.createElement('div');
    card.className = 'card';

    const meta = document.createElement('div');
    meta.className = 'meta';
    meta.innerText = `${entry.event} • ${entry.weather} • ${entry.created_at}`;
    card.appendChild(meta);

    const imagesWrap = document.createElement('div');
    imagesWrap.className = 'outfit-images';

    entry.items.forEach(it => {
      const img = document.createElement('img');
      img.src = it.url;
      imagesWrap.appendChild(img);
    });

    card.appendChild(imagesWrap);

    const why = document.createElement('div');
    why.className = 'outfit-why';
    why.innerText = entry.justification;
    card.appendChild(why);

    // ✅ ADD DELETE BUTTON HERE
    const delBtn = document.createElement('button');
    delBtn.innerText = '🗑 Delete';
    delBtn.onclick = async () => {
      if (!confirm('Delete this history entry?')) return;

      await api('delete_history', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ history_id: entry.id })
      });

      loadHistory();  // refresh after delete
    };

    card.appendChild(delBtn);

    div.appendChild(card);
  });
}

/* ---------------- INIT ---------------- */
loadItems();
showPage('home');









