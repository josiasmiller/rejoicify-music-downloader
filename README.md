# Rejoicify Music Downloader

A browser-based tool for browsing Rejoicify music albums and downloading songs using a valid Rejoicify access token.

## Notes

- This app does not include or publish any token.
- Users must sign in to their own Rejoicify account and provide their own token.
- Tokens are stored locally in the browser using localStorage.

## Development note

This is not affiliated with, endorsed by, or maintained by Rejoicify.

No access tokens are included in this repository. Users must sign in to their own Rejoicify account and provide their own valid token. Use at your own risk.

## Local Server Setup

The included `server.py` runs a local CORS proxy so the app can communicate with Rejoicify's API from your browser.

### Requirements

- Python 3.7+
- Flask (`pip install flask`)

### Running the server

1. Make sure `index.html` and `server.py` are in the same folder.
2. Start the server:
   ```bash
   python server.py
