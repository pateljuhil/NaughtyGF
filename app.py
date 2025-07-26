import sqlite3
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types

client = genai.Client(api_key="AIzaSyDpZrKHoJhMhxPzy3_xuo2Z4FL7UBDcuqc")

app = Flask(__name__)

# ------------------ Home Route ------------------ #
@app.route('/')
def home():
    return render_template('chat.html')

# ------------------ Ask Route ------------------ #
@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_input = data.get('message')
    username = data.get('username', 'Anonymous')

    # Save user's message
    save_message(username, "You", user_input)

    # Gemini response
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=(
                "You are a young 25 years hot and sexy girl. Your name is Sweety. "
                "You are my Girlfriend. Suppose that asking person is innocent and shy young boy. "
                "You are very naughty and can talk like double meaning, in 10-15 words, in Hinglish only. Use emojis also."
            ),
        ),
        contents=user_input
    )

    reply_text = response.text

    # Save Sweety's response
    save_message(username, "Sweety", reply_text)

    return jsonify({'reply': reply_text})

# ------------------ Save Message Function ------------------ #
def save_message(username, sender, message):
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute(
        "INSERT INTO messages (username, sender, message) VALUES (?, ?, ?)",
        (username, sender, message)
    )
    conn.commit()
    conn.close()

# ------------------ View History Route ------------------ #
@app.route("/history")
def view_history():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute("SELECT * FROM messages ORDER BY timestamp")
    rows = c.fetchall()
    conn.close()

    history_html = "<h2>Chat History</h2><ul>"
    for row in rows:
        history_html += f"<li><strong>{row[1]} ({row[2]})</strong>: {row[3]} <em>({row[4]})</em></li>"
    history_html += "</ul>"

    return history_html

# ------------------ Main ------------------ #
if __name__ == '__main__':
    app.run(debug=True)
