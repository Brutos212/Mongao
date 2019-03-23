# -- coding: utf-8 --

# Instalar todas as dependências abaixo                  

# pip3 install flask
# pip3 install pymongo
# pip3 install dnspython

from flask import request
import flask
import pymongo

#USER = 'admin'
#PASSWORD = '!23Mudar$'

#MONGODB_URL = f'mongodb+srv://{USER}:{PASSWORD}@cluster0-nstlp.mongodb.net/test?retryWrites=true'
MONGODB_URL = 'mongodb+srv://fabio212:fa140880@cluster0-v6h5c.mongodb.net/test?retryWrites=true'


# Criar classe Model para abstrair métodos úteis    
class Model:

    def __repr__(self):
        return str(self.__dict__)
#Criar classe usuário para manusear os dados

class Usuario(Model):
    def __init__(self, nome, endereco, idade):
        self.nome = nome
        self.endereco = endereco
        self.idade = idade
# Criar conexão com o MongoDB
conn = pymongo.MongoClient(MONGODB_URL)

#Criar banco de dados e coleção para salvar
db = conn.mongao
monguinho = db.monguinho

#Iniciar Flask
app= flask.Flask(__name__)

#Criar rota para inserir usuário
@app.route('/user', methods=['GET', 'POST'])
def user():
    MENSAGEM = ''
    if request.method == 'POST':

        nome = request.form['nome']
        endereco = request.form['endereco']
        idade = request.form['idade']

        usuario = Usuario(nome, endereco, idade)

        monguinho.insert(usuario.__dict__)

        MENSAGEM = '<p>Usuário inserido com sucesso!!</p>'

    usuarios = list(monguinho.find({'nome': {'$exists': True}}))

    def template_usuario(usuario):
        try: 
            return '''
                <li>
                    <ol>
                        <li>Nome: {}</li>
                        <li>Endereço: {}</li>
                        <li>Idade: {}</li>
                    </ol>    
                </li>
            '''.format(usuario['nome'], usuario['endereco'], usuario['idade'])
        except KeyError:
            return ''
            
    usuarios = ''.join(template_usuario(usuario) for usuario in usuarios)

    return '''
                {}

                <form action="/user" method="POST">
                    <input type="text" name="nome">
                    <input type="text" name="endereco">
                    <input type="text" name="idade">
                    <button type="submit">Cadastrar usuário</button>
                </form>
            <ul>
                {}
            </ul>    
        
        '''.format(MENSAGEM, usuarios)

def main():
    app.run()            
            

  
if __name__ == '__main__':
    main()