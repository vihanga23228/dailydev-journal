async function loadJournal() {
  const quote = document.getElementById('feature-title');
  const author = document.getElementById('latest-author');
  const date = document.getElementById('latest-date');
  const entries = document.getElementById('entries');
  const count = document.getElementById('count');
  try {
    const response = await fetch('./data/quotes.json', {cache: 'no-cache'});
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const records = await response.json();
    if (!Array.isArray(records)) throw new Error('Invalid archive format');
    records.sort((a,b) => b.date.localeCompare(a.date));
    count.textContent = `${records.length} entries`;
    if (records.length === 0) {
      quote.textContent = 'Your first daily quote is coming soon.';
      entries.textContent = 'Run the daily workflow to create your first entry.';
      return;
    }
    const latest = records[0];
    quote.textContent = `“${latest.quote}”`;
    author.textContent = `— ${latest.author}`;
    date.textContent = latest.date;
    for (const item of records.slice(1)) {
      const card = document.createElement('article'); card.className = 'entry';
      const day = document.createElement('span'); day.className = 'date'; day.textContent = item.date;
      const text = document.createElement('p'); text.textContent = `“${item.quote}”`;
      const by = document.createElement('span'); by.className = 'author'; by.textContent = `— ${item.author}`;
      card.append(day,text,by); entries.appendChild(card);
    }
  } catch (error) {
    quote.textContent = 'The journal is temporarily unavailable.';
    entries.textContent = 'Please try again later.';
    console.error('Failed to load journal:',error);
  }
}
loadJournal();
