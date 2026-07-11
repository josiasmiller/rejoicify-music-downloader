# Rejoicify Music Downloader

A browser-based tool for browsing Rejoicify music albums and downloading songs.

## Disclaimer

This project is not affiliated with, endorsed by, sponsored by, or maintained by Rejoicify.

No access tokens or account credentials are included in this repository. Users must sign in to their own Rejoicify account and use the project at their own risk.

## Ways to Run the App

There are two ways to run the application.

### Option 1: Standalone HTML File

Open `standalone.html` directly in your browser.

This version:

* Does not require Python or Flask.
* Requires the user to provide a valid Rejoicify access token.
* Stores the token locally in the browser using `localStorage`.

#### Running the Standalone Version

1. Download or clone the repository.
2. Locate `standalone.html`.
3. Open it in a supported web browser.
4. Enter your valid Rejoicify access token.

To remove the stored token, clear the browser's local storage or site data.

### Option 2: Local Server

The server version uses `index.html` and `server.py`.

This version:

* Runs through a local Flask server.
* Uses the browser's existing Rejoicify authentication cookie.
* Does not require the user to manually enter an access token.
* Does not store an access token in `localStorage`.
* Includes a local CORS proxy so the browser can communicate with Rejoicify's API.

You must already be signed in to Rejoicify in the browser for this version to work.

## Server Requirements

* Python 3.7 or newer
* Flask

Install Flask with:

```bash
pip install flask
```

## Running the Server

1. Make sure `index.html` and `server.py` are in the same folder.
2. Sign in to your Rejoicify account in the browser.
3. Open a terminal in the project folder.
4. Start the server:

```bash
python server.py
```

5. Open the local address displayed in the terminal, typically:

```text
http://localhost:8000
```

## Security

Authentication information may provide access to your Rejoicify account.

* Do not share or publish access tokens or browser cookies.
* Do not commit authentication information to the repository.
* The standalone version stores the token in browser `localStorage`.
* The server version uses the browser's existing Rejoicify authentication cookie.
* Only run the local server on a device and network you trust.
