import requests
def buscar_dados():
    dados = requests.get("http://localhost:5000/buscarPalavrasCategoria/Arqueologia")
    print(dados.content)

if __name__ == '__main__':
    buscar_dados()

"""#Rota para adicionar usuários
@app.route('/adicionarUsuario', methods=["POST"])
def adicionarUsuario():
   _json = request.json
   _nome = _json['nome']
   _email = _json['email']
   _senha = _json['senha']
   regex = '^[\w-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$'
   _json["senha"] = generate_password_hash(_senha)
   login_details = request.get_json()
   doc = mongo.db.usuarios.find_one({"email":_json["email"]})
   if not doc:
        if (re.search(regex, _email)) and _nome and _email and _senha and request.method == 'POST':
            login_details['senha'] = hashlib.sha256(_senha['senha'].encode("utf-8")).hexdigest()
            id = mongo.db.usuarios.insert_one({'nome': _nome, 'email':_email, 'senha': doc()})
            resposta = jsonify("Usuário adicionado com sucesso!")
            resposta.status_code = 200
            return resposta

   else:
       resposta = jsonify({'msg': 'Este usuário já está cadastrado no banco de dados!'}), 409
       return resposta
"""










# Testes com a senha 1234
# User from db =                        03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4
# Senha encripitada enviada via postman 03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4
# Testes com a senha 1234
# User from db =                        03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4
# Senha encripitada enviada via postman 5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5