# URL Shortener

A backend service that takes a long URL and generates a short, unique code that redirects back to it — built with Flask and SQLite, with real system design thinking behind the ID generation.

## Why this exists

Long URLs are unwieldy to share — especially in space-constrained contexts like messages or printed material. This project builds the actual mechanism behind services like Bitly: a reliable way to shorten links and redirect through them, while thinking carefully about a real, common trap in system design — predictable, guessable IDs.

## How it works

- Every shortened link gets a random 6-character code, drawn from a 62-character alphabet (digits, lowercase, uppercase)
- Codes are checked for uniqueness against the database, with automatic retry on the rare collision
- An earlier, sequential base62-encoding approach was deliberately built and then replaced — sequential IDs are predictable and let anyone enumerate other users' links by guessing nearby values; true randomness closes that gap entirely
- The whole "create and verify" process for a new link is handled as a single atomic operation, so a crash mid-creation can never leave a broken, half-saved link behind

## Features

- `POST /create` — accepts a JSON body with a `url`, returns a unique short code
- `GET /<code>` — visiting a short link redirects to the original URL, or returns a clear "not found" message if the code doesn't exist
- Backed by SQLite with a `UNIQUE` constraint on short codes, enforced at the database level, not just in application code

## How to run it

```bash
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py
```

Then send a request to create a link:

```bash
python test_create.py
```

## What's next

- Multiple related tables (click analytics, custom aliases) with real SQL JOINs
- Rate limiting, to prevent abuse
- A caching layer in front of the redirect lookup, since reads vastly outnumber writes for a service like this
- Deployment to a real cloud host, with basic monitoring

## Built as part of a self-directed backend + AI/ML learning journey — Project 7.