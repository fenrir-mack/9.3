from flask import Flask, request, jsonify

app = Flask(__name__)

# Banco de dados temporário em memória
itens = [
    {"id": 1, "nome": "Teclado Mecânico", "preco": 250.00},
    {"id": 2, "nome": "Mouse Gamer", "preco": 150.00}
]


# Rota principal
@app.route("/")
def home():
    return (
        "<h1>API Flask funcionando!</h1>"
        "<p>Use os endpoints de <b>/itens</b> para interagir com a API.</p>"
    )


# 1. GET - Obter todos os itens (READ)
@app.route("/itens", methods=["GET"])
def listar_itens():
    return jsonify(itens), 200


# 2. GET - Obter um item específico por ID (READ)
@app.route("/itens/<int:item_id>", methods=["GET"])
def obter_item(item_id):
    # Procura o item na lista
    item = next((i for i in itens if i["id"] == item_id), None)
    if item is None:
        return jsonify({"erro": "Item não encontrado"}), 404
    return jsonify(item), 200


# 3. POST - Criar um novo item (CREATE)
@app.route("/itens", methods=["POST"])
def criar_item():
    dados = request.get_json()  # Pega os dados enviados no corpo da requisição (JSON)

    # Validação simples
    if not dados or "nome" not in dados or "preco" not in dados:
        return jsonify({"erro": "Dados inválidos. Envie 'nome' e 'preco'."}), 400

    # Cria o novo item gerando um ID incremental
    novo_id = max([item["id"] for item in itens], default=0) + 1
    novo_item = {
        "id": novo_id,
        "nome": dados["nome"],
        "preco": dados["preco"]
    }

    itens.append(novo_item)
    return jsonify(novo_item), 201  # 21 Created


# 4. PUT - Atualizar um item existente por ID (UPDATE)
@app.route("/itens/<int:item_id>", methods=["PUT"])
def atualizar_item(item_id):
    dados = request.get_json()  # Pega os novos dados

    # Procura o item na lista
    item = next((i for i in itens if i["id"] == item_id), None)
    if item is None:
        return jsonify({"erro": "Item não encontrado"}), 404

    # Atualiza os dados se fornecidos no corpo da requisição
    item["nome"] = dados.get("nome", item["nome"])
    item["preco"] = dados.get("preco", item["preco"])

    return jsonify(item), 200


# 5. DELETE - Deletar um item por ID (DELETE)
@app.route("/itens/<int:item_id>", methods=["DELETE"])
def deletar_item(item_id):
    global itens
    # Procura o item na lista
    item = next((i for i in itens if i["id"] == item_id), None)
    if item is None:
        return jsonify({"erro": "Item não encontrado"}), 404

    # Filtra a lista removendo o item com o ID especificado
    itens = [i for i in itens if i["id"] != item_id]
    return jsonify({"mensagem": f"Item {item_id} removido com sucesso!"}), 200


if __name__ == "__main__":
    app.run(debug=True)
