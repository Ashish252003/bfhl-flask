
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# --- Configuration (edit these or set environment variables) ---
FULL_NAME = os.getenv("FULL_NAME", "john_doe")        # must be lowercase as per spec
DOB_DDMMYYYY = os.getenv("DOB_DDMMYYYY", "17091999")  # ddmmyyyy
EMAIL = os.getenv("EMAIL", "john@xyz.com")
ROLL_NUMBER = os.getenv("ROLL_NUMBER", "ABCD123")


def is_int_like(x):
    """Return True if x is an integer or a string representing an integer (with optional sign)."""
    if isinstance(x, int):
        return True
    if isinstance(x, str):
            s = x.strip()
            if s.startswith(('+', '-')):
                return s[1:].isdigit()
            return s.isdigit()
    return False


def is_alpha_only(x):
    """Return True if x is a non-empty string of alphabetic characters only."""
    return isinstance(x, str) and len(x) > 0 and x.isalpha()


@app.post("/bfhl")
def bfhl():
    # Parse JSON safely
    try:
        payload = request.get_json(force=True, silent=False)
    except Exception:
        return jsonify({"is_success": False, "error": "Invalid JSON"}), 400

    if not isinstance(payload, dict) or "data" not in payload:
        return jsonify({"is_success": False, "error": "Missing 'data' field"}), 400

    data = payload["data"]
    if not isinstance(data, list):
        return jsonify({"is_success": False, "error": "'data' must be a list"}), 400

    even_numbers = []
    odd_numbers = []
    numbers_sum = 0
    alphabets = []
    special_characters = []
    letters_stream = []  # for concat_string computation

    for item in data:
        if is_int_like(item):
            value = int(item)
            numbers_sum += value
            (even_numbers if value % 2 == 0 else odd_numbers).append(str(value))  # numbers must be strings in response
        elif is_alpha_only(item):
            alphabets.append(item.upper())
            letters_stream.extend(list(item))
        elif isinstance(item, str) and len(item) > 0 and all(not ch.isalnum() for ch in item):
            # string made of only non-alphanumeric characters (e.g., "$", "&*")
            special_characters.append(item)
        else:
            # mixed tokens like "ab1", empty strings, floats, nested types -> treat as special
            special_characters.append(str(item))

    # Build concat_string: reverse all letters encountered (in original order),
    # then alternate caps starting with UPPER on index 0.
    rev_letters = list(reversed(letters_stream))
    alt = []
    for i, ch in enumerate(rev_letters):
        alt.append(ch.upper() if i % 2 == 0 else ch.lower())
    concat_string = "".join(alt)

    response = {
        "is_success": True,
        "user_id": f"{FULL_NAME.lower()}_{DOB_DDMMYYYY}",
        "email": EMAIL,
        "roll_number": ROLL_NUMBER,
        "odd_numbers": odd_numbers,
        "even_numbers": even_numbers,
        "alphabets": alphabets,
        "special_characters": special_characters,
        "sum": str(numbers_sum),  # return as string
        "concat_string": concat_string,
    }
    return jsonify(response), 200

@app.get("/")
def home():
    return {"message": "Server running. Use GET /bfhl or POST /bfhl"}

@app.get("/bfhl")
def bfhl_get():
    return {"operation_code": 1, "message": "GET request successful"}

if __name__ == "__main__":
    # Local dev
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
