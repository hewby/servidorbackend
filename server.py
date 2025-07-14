from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import uuid

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
    texto = f"{nome} te enviou uma música: {link}" if valido else f"{nome} te enviou um link inválido"

    novo_pedido = {
        "id": str(uuid.uuid4()),
        "texto": texto,
        "valido": valido,
        "hora": datetime.now().strftime("%H:%M:%S"),
        "excluido": False
    }

    pedidos.append(novo_pedido)
    return jsonify({"mensagem": "Pedido recebido com sucesso."}), 200

@app.route("/pedidos", methods=["GET"])
def listar_pedidos():
    # Retorna apenas pedidos não excluídos
    ativos = [p for p in pedidos if not p["excluido"]]
    return jsonify({"pedidos": ativos})

@app.route("/limpar_todos", methods=["POST"])
def limpar_todos():
    for pedido in pedidos:
        pedido["excluido"] = True
    return jsonify({"mensagem": "Todos os pedidos foram excluídos."})

@app.route("/limpar_invalidos", methods=["POST"])
def limpar_invalidos():
    for pedido in pedidos:
        if not pedido["valido"]:
            pedido["excluido"] = True
    return jsonify({"mensagem": "Pedidos inválidos foram excluídos."})

if __name__ == "__main__":
    app.run(debug=True)


