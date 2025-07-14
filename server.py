from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Estrutura de dados: lista de dicionários { mensagem, horario }
pedidos = []

@app.route("/pedido", methods=["POST"])
def receber_pedido():
    dados = request.get_json()
    nome = dados.get("nome", "").strip()
    link = dados.get("link", "").strip()

    if not nome or not link:
        return jsonify({"mensagem": "Nome e link são obrigatórios."}), 400

    horario = datetime.now().strftime("%H:%M:%S")
    if "youtube.com" in link or "youtu.be" in link:
        msg = f"{nome} te enviou uma música: {link}"
    else:
        msg = f"{nome} te enviou um link inválido"

    pedidos.append({"mensagem": msg, "horario": horario})

    return jsonify({"mensagem": "Pedido recebido com sucesso."}), 200

@app.route("/pedidos", methods=["GET"])
def listar_pedidos():
    return jsonify({"pedidos": pedidos})

@app.route("/limpar_todos", methods=["POST"])
def limpar_todos():
    global pedidos
    pedidos.clear()
    return jsonify({"mensagem": "Todos os pedidos foram limpos."})

@app.route("/limpar_invalidos", methods=["POST"])
def limpar_invalidos():
    global pedidos
    # Mantém apenas pedidos que NÃO possuem "link inválido"
    pedidos = [p for p in pedidos if "link inválido" not in p["mensagem"]]
    return jsonify({"mensagem": "Pedidos inválidos limpos."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
