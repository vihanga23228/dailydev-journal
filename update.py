"""Fetch one daily quote and store it in the static site's JSON archive."""
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / 'site' / 'data' / 'quotes.json'
API_URL = 'https://zenquotes.io/api/random'
SLST = timezone(timedelta(hours=5, minutes=30))


def main():
    today = datetime.now(SLST).date().isoformat()
    history = json.loads(DATA_FILE.read_text(encoding='utf-8')) if DATA_FILE.exists() else []
    if not isinstance(history, list):
        raise ValueError('Quote history must be a JSON list')
    if any(item.get('date') == today for item in history):
        print(f'Already updated for {today}; no changes')
        return

    request = Request(API_URL, headers={'User-Agent': 'DailyDevJournal/1.0'})
    with urlopen(request, timeout=25) as response:
        payload = json.load(response)
    if not isinstance(payload, list) or not payload or not isinstance(payload[0], dict):
        raise ValueError('Unexpected quote API response')
    item = payload[0]
    quote = item.get('q')
    author = item.get('a')
    if not isinstance(quote, str) or not quote.strip() or not isinstance(author, str) or not author.strip():
        raise ValueError('Quote API returned missing or invalid content')
    if quote.lower().startswith('too many requests'):
        raise ValueError('API rate limit reached')

    history.insert(0, {'date': today, 'quote': quote.strip(), 'author': author.strip()})
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(history, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Saved quote for {today}; {len(history)} total entries')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'Daily update failed: {exc}', file=sys.stderr)
        sys.exit(1)
