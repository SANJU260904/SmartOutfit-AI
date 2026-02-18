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

    /* category dropdown */
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

    /* worn */
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

    /* favorite (FIXED) */
    const favBtn = document.createElement('button');
    favBtn.innerText = it.favorited ? '⭐ Favorited' : '☆ Favorite';
    favBtn.onclick = async () => {
      await api('favorite', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          item_id: it.id,
          favorite: !it.favorited
        })
      });
      loadItems();
    };

    /* delete */
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

    /* vertical images */
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
};

/* ---------------- INIT ---------------- */
loadItems();
