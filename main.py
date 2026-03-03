import os
from flask import Flask, request, jsonify
from findmy import AppleAccount
from findmy.keys import KeyPair

app = Flask(__name__)

ANISETTE_URL = os.getenv("ANISETTE_URL", "http://anisette:6969")
APPLE_ID = os.getenv("APPLE_ID", "seu_email@apple.com")
APPLE_PWD = os.getenv("APPLE_PWD", "sua_senha")

async def get_findmy_reports(private_keys_b64):
    """
    Conecta na Apple, busca os relatórios criptografados e os descriptografa
    usando as chaves privadas fornecidas.
    """
    # 1. Configura a conta usando o Anisette local para gerar os headers do Mac
    account = AppleAccount(APPLE_ID, APPLE_PWD, anisette_server=ANISETTE_URL)
    
    # 2. Verifica o login (na primeira execução, isso pode exigir 2FA)
    if not account.is_logged_in:
        await account.login()

    # 3. Converte as strings Base64 do request em objetos KeyPair
    devices = []
    for pk_b64 in private_keys_b64:
        # Aqui entra exatamente o código da documentação que você mandou!
        device = KeyPair.from_b64(pk_b64)
        devices.append(device)

    # 4. Busca os relatórios na rede da Apple
    # A biblioteca vai cuidar de fazer o hash da chave pública, buscar e descriptografar
    relatorios = await account.fetch_reports(devices)
    
    # 5. Formata a resposta
    resultados = []
    for report in relatorios:
        resultados.append({
            "lat": report.latitude,
            "lon": report.longitude,
            "accuracy": report.accuracy,
            "timestamp": report.timestamp.isoformat(),
        })
        
    return resultados


@app.route('/sync', methods=['POST'])
async def sync_with_apple():
    try:
        data = request.json
        # Agora esperamos receber uma lista de chaves PRIVADAS em base64
        private_keys = data.get("private_keys", [])

        if not private_keys:
            return jsonify({"error": "Nenhuma chave privada (private_keys) fornecida"}), 400

        # Executa a busca assíncrona
        resultados = await get_findmy_reports(private_keys)

        return jsonify({"status": "success", "reports": resultados})

    except Exception as e:
        return jsonify({
            "error": "Erro interno no processamento do FindMy.py",
            "details": str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)