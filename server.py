from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

pedidos = []

@app.route("/pedido", methods=["POST"])
def receber_pedido():
    dados = request.get_json()
    nome = dados.get("nome", "").strip()
    link = dados.get("link", "").strip()

    if not nome or not link:
        return jsonify({"mensagem": "Nome e link são obrigatórios."}), 400

    valido = "youtube.com" in link or "youtu.be" in link
    agora = datetime.now().strftime("%H:%M:%S")
    texto = f"{nome} te enviou uma música: {link}" if valido else f"{nome} te enviou um link inválido"

    pedido = {
        "texto": texto,
        "horario": agora,
        "valido": valido
    }
    pedidos.append(pedido)

    return jsonify({"mensagem": "Pedido recebido com sucesso."}), 200

@app.route("/pedidos", methods=["GET"])
def listar_pedidos():
    return jsonify({"pedidos": pedidos})

@app.route("/limpar_todos", methods=["POST"])
def limpar_todos():
    pedidos.clear()
    return jsonify({"mensagem": "Todos os pedidos foram limpos."}), 200

@app.route("/limpar_invalidos", methods=["POST"])
def limpar_invalidos():
    global pedidos
    pedidos = [p for p in pedidos if p["valido"]]
    return jsonify({"mensagem": "Pedidos inválidos foram limpos."}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

