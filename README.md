# tlf-backend
A backend app built using fastapi.

## How to setup
- Clone this repo.
- Open your terminal/command propmt inside the repo
- Create and activte a virtual environment.
- Run <code> pip install -r requirements.txt </code> in your terminal.
- cd into the app folder <code>cd app</code>.
- Set an environment variable named SECRET_KEY and assign it a 32 bit random string.
- Run <code>uvicorn main:app --reload</code>.
- Open http://localhost:8000/docs in your browser.
