from flask import Flask, request, jsonify
import anthropic
import os

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

@app.route("/alexa", methods=["POST"])
def alexa_handler():
    try:
        body = request.json
        request_type = body["request"]["type"]

        if request_type == "LaunchRequest":
            return jsonify({
                "version": "1.0",
                "response": {
                    "outputSpeech": {
                        "type": "PlainText",
                        "text": "Ciao! Dimmi pure la tua domanda."
                    },
                    "shouldEndSession": False
                }
            })

        slots = body["request"]["intent"]["slots"]
        
        if "query" not in slots or "value" not in slots["query"]:
            return jsonify({
                "version": "1.0",
                "response": {
                    "outputSpeech": {
                        "type": "PlainText",
                        "text": "Non ho capito la domanda. Riprova."
                    },
                    "shouldEndSession": True
                }
            })

        query = slots["query"]["value"]

        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=150,
            system="Rispondi in italiano in massimo 2 frasi brevi e dirette.",
            messages=[{"role": "user", "content": query}]
        )

        risposta = message.content[0].text

        return jsonify({
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": risposta
                },
                "shouldEndSession": True
            }
        })

    except Exception as e:
        return jsonify({
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Si è verificato un errore. Riprova."
                },
                "shouldEndSession": True
            }
        })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
```

