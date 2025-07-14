from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

pedidos = []
proximo_id = 1

@app.route("/pedido", methods=["POST"])
def receber_pedido():
    global proximo_id
    dados = request.get_json()
    nome = dados.get("nome", "").strip()
    link = dados.get("link", "").strip()

    if not nome or not link:
        return jsonify({"mensagem": "Nome e link são obrigatórios."}), 400

    invalido = not ("youtube.com" in link or "youtu.be" in link)
    hora = datetime.now().strftime("%H:%M:%S")

    texto = f"{nome} te enviou uma música: {link}" if not invalido else f"{nome} te enviou um link inválido"

    pedido = {
        "id": proximo_id,
        "texto": texto,
        "invalido": invalido,
        "hora": hora
    }
    proximo_id += 1
    pedidos.append(pedido)

    return jsonify({"mensagem": "Pedido recebido com sucesso."}), 200

@app.route("/pedidos", methods=["GET"])
def listar_pedidos():
    return jsonify({"pedidos": pedidos})

@app.route("/limpar_todos", methods=["POST"])
def limpar_todos():
    global pedidos
    pedidos = []
    return jsonify({"mensagem": "Todos os pedidos foram limpos."}), 200

@app.route("/limpar_invalidos", methods=["POST"])
def limpar_invalidos():
    global pedidos
    pedidos = [p for p in pedidos if not p["invalido"]]
    return jsonify({"mensagem": "Pedidos inválidos foram limpos."}), 200

@app.route("/deletar_pedido/<int:pedido_id>", methods=["DELETE"])
def deletar_pedido(pedido_id):
    global pedidos
    pedidos = [p for p in pedidos if p["id"] != pedido_id]
    return jsonify({"mensagem": f"Pedido {pedido_id} deletado."}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
