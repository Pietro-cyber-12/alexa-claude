from flask import Flask, request, jsonify
import anthropic
import os

app = Flask(__name__)

@app.route("/alexa", methods=["POST"])
def alexa_handler():
    body = request.json
    req_type = body["request"]["type"]
    if req_type == "LaunchRequest":
        return jsonify({"version": "1.0", "response": {"outputSpeech": {"type": "PlainText", "text": "Ciao! Dimmi pure la tua domanda."}, "shouldEndSession": False}})
    try:
        query = body["request"]["intent"]["slots"]["query"]["value"]
        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        msg = client.messages.create(model="claude-haiku-4-5-20251001", max_tokens=150, system="Rispondi in italiano in massimo 2 frasi.", messages=[{"role": "user", "content": query}])
        speech = msg.content[0].text
    except Exception as e:
        speech = "Errore: " + str(e)
    return jsonify({"version": "1.0", "response": {"outputSpeech": {"type": "PlainText", "text": speech}, "shouldEndSession": True}})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))