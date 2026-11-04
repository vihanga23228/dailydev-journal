# DailyDev Journal

A free static developer inspiration journal updated by Python and GitHub Actions.

## Setup

1. Create a **public** GitHub repository named `dailydev-journal` with default branch `main`.
2. Copy these files into it.
3. In **Settings → Secrets and variables → Actions → Variables**, set:
   - `COMMIT_NAME`: your GitHub username or desired author name.
   - `COMMIT_EMAIL`: a verified email on your GitHub account (or your exact GitHub noreply address).
4. In **Settings → Actions → General → Workflow permissions**, select **Read and write permissions**, if needed to allow `GITHUB_TOKEN` to push.
5. In **Settings → Pages → Build and deployment → Source**, choose **GitHub Actions**.
6. Push to `main` and run **Actions → DailyDev Journal → Run workflow**.
7. Visit `https://YOUR_USERNAME.github.io/dailydev-journal/`.

## Local testing

```bash
python3 update.py
python3 -m http.server 8000 --directory site
```

Open http://localhost:8000. Python uses only standard-library modules.

## How it works

The scheduled workflow runs at 18:35 UTC (00:05 the next day in Sri Lanka), fetches a quote from https://zenquotes.io/api/random, and commits the new entry to `site/data/quotes.json` on `main`. It deploys the `site` folder to GitHub Pages. Manual runs also update the journal. Pushes to `main` deploy the site without fetching a quote; changes only to the JSON archive do not trigger a second deployment run.

The API may have rate limits or temporary failures; a failed fetch leaves the archive unchanged. Scheduled runs are best effort and can be delayed or disabled after repository inactivity. A successful workflow does not guarantee a contribution graph square: the author email and branch must meet GitHub's contribution rules.

Quotes attributed to [ZenQuotes](https://zenquotes.io/).
