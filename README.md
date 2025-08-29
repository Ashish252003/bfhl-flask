
# Flask BFHL API (Starter)

A minimal Flask app that fulfills the BFHL assignment:

- POST `/bfhl` accepts a JSON body with `data: [ ... ]`.
- Returns:
  - `is_success` (bool)
  - `user_id` as `full_name_ddmmyyyy` (lowercase full name)
  - `email`, `roll_number`
  - `odd_numbers`, `even_numbers` (values as **strings**)
  - `alphabets` (uppercase)
  - `special_characters`
  - `sum` (string)
  - `concat_string` (reverse of all letters, alternating caps starting with upper)

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

export FULL_NAME="john_doe"       # must be lowercase
export DOB_DDMMYYYY="17091999"
export EMAIL="john@xyz.com"
export ROLL_NUMBER="ABCD123"

python app.py
# in another terminal:
curl -X POST http://localhost:5000/bfhl   -H "Content-Type: application/json"   -d '{"data":["a","1","334","4","R","$"]}'
```

Expected (example) response:
```json
{
  "is_success": true,
  "user_id": "john_doe_17091999",
  "email": "john@xyz.com",
  "roll_number": "ABCD123",
  "odd_numbers": ["1"],
  "even_numbers": ["334", "4"],
  "alphabets": ["A", "R"],
  "special_characters": ["$"],
  "sum": "339",
  "concat_string": "Ra"
}
```

## Deploy (one easy option: Render)

1. Push this folder to a new public GitHub repo.
2. On Render, create a **Web Service** from your repo.
3. Select a Python version (e.g., 3.11), and ensure the Start Command is:
   ```
   gunicorn app:app
   ```
4. Once deployed, POST to `https://<your-service>.onrender.com/bfhl`.

(You can deploy to other platforms like Railway, Fly.io, or your own server — just use the `gunicorn app:app` entry point.)
