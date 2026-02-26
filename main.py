from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

MACLESS_URL = os.getenv("MACLESS_URL", "http://macless-haystack:6176")

@app.route('/sync', methods=['POST'])
def sync_with_apple():
    try:
        data = request.json

        response = requests.post(
            f"{MACLESS_URL}/sync",
            json={
                "keys": data.get("keys")
            },
            timeout=60
        )

        response.raise_for_status()

        return jsonify(response.json())

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Erro ao comunicar com macless-haystack",
            "details": str(e)
        }), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)