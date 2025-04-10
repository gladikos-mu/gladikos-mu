from flask import Flask, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv
import time

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
assistant_id = os.getenv("ASSISTANT_ID")

@app.route("/ask", methods=["POST"])
def ask():
    msg = request.json.get("message", "")
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(thread.id, role="user", content=msg)
    run = client.beta.threads.runs.create(thread.id, assistant_id=assistant_id)

    while True:
        run_status = client.beta.threads.runs.retrieve(thread.id, run.id)
        if run_status.status == "completed":
            break
        time.sleep(1)

    messages = client.beta.threads.messages.list(thread.id)
    reply = messages.data[0].content[0].text.value
    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
