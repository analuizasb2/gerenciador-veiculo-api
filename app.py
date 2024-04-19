import sqlite3
from flask import request, jsonify, redirect
from model.veiculo import Veiculo, VeiculoSchema, VeiculoPath, VeiculoListSchema
from model.abastecimento import Abastecimento, AbastecimentoSchema, AbastecimentoListSchema, AbastecimentoInsertSchema, AbastecimentoPath
from flask_openapi3 import OpenAPI, Info, Tag
from model.error import ConflictErrorSchema, BadRequestErrorSchema
from flask_cors import CORS

info = Info(title="Gerenciador de Veiculos API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)
DB_NAME = 'gerenciador_veiculos.db'

@app.get('/')
def home():
    """Documentação.
    """
    return redirect('/openapi/swagger')

veiculo_tag = Tag(name="Veiculo", description="Adição, remoção e visualização de veículo")
abastecimento_tag = Tag(name="Abastecimentos", description="Adição, remoção e visualização de abastecimentos para um veículo")

@app.post('/api/veiculos',
          tags=[veiculo_tag],
          responses={200: None, 400: BadRequestErrorSchema, 409: ConflictErrorSchema})
def insertVeiculo(body: VeiculoSchema):
    try:
        """ Insere um novo veículo.
        """
        data = request.get_json()
        print(data)
        placa = data.get('placa')
        marca = data.get('marca')
        modelo = data.get('modelo')
        tipo_carroceria = data.get('tipo_carroceria')
        ano_fabricacao = data.get('ano_fabricacao')
        ano_modelo = data.get('ano_modelo')
        veiculo_novo = Veiculo(placa, marca, modelo, tipo_carroceria, ano_fabricacao, ano_modelo)
        veiculo_novo.save()
        return {'Veiculo registrado': placa}
    except sqlite3.IntegrityError as e:
        return {"message": "Veículo já cadastrado."}, 409

@app.get('/api/veiculos',
         tags=[veiculo_tag],
         responses={200: VeiculoListSchema, 404: None})
def getVeiculos():
    """Retorna todos os veículos cadastrados.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM veiculos')
    veiculos = []
    for row in cursor.fetchall():
        veiculo = VeiculoSchema(
            placa=row[0],
            marca=row[1],
            modelo=row[2],
            tipo_carroceria=row[3],
            ano_fabricacao=row[4],
            ano_modelo=row[5]
        )
        veiculos.append(veiculo)
    conn.close()
    if veiculos == []:
        return "Nenhum veiculo encontrado", 404
    return jsonify({'veiculos': [dict(veiculo) for veiculo in veiculos]})

@app.delete('/api/veiculos',
            tags=[veiculo_tag],
            responses={200: None, 400: BadRequestErrorSchema})
def deleteVeiculo(query: VeiculoPath):
    """Deleta um veículo pelo número da placa.
    """
    veiculo = request.args.get('Placa')
    if veiculo.isspace() or veiculo == '':
        return {"message": "O parâmetro 'Placa' é obrigatório"}, 400
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM veiculos WHERE placa = ?', (veiculo,))
        conn.commit()
        conn.close()
        return f"Veiculo {veiculo} deletado!"
    finally:
            conn.close()

@app.get('/api/abastecimentos',
         tags=[abastecimento_tag],
         responses={200: AbastecimentoListSchema, 400: BadRequestErrorSchema})
def getAbastecimentos(query: VeiculoPath):
    """ Retorna todos os abastecimentos para um veículo específico.
    """
    veiculo = request.args.get('Placa')
    if veiculo is None:
        return "O parâmetro 'Placa' é obrigatório", 400
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM abastecimentos WHERE veiculo = ?', (veiculo,))
    abastecimentos = []
    for row in cursor.fetchall():
        abastecimento = AbastecimentoSchema(
            id=row[0],
            horario=row[1],
            valor=row[3],
            volume=row[4],
            completando_tanque=row[5],
            odometro=row[6]
        )
        abastecimentos.append(abastecimento)
    conn.close()
    return jsonify({'abastecimentos': [dict(abastecimento) for abastecimento in abastecimentos]})

@app.post('/api/abastecimentos', 
          tags=[abastecimento_tag], 
          responses={200: None, 400: BadRequestErrorSchema})
def insertAbastecimento(body: AbastecimentoInsertSchema):
    """ Insere um novo abastecimento para um veículo específico.
    """
    data = request.get_json()
    valor = data.get('valor')
    volume = data.get('volume')
    veiculo = data.get('veiculo')
    completando_tanque = data.get('completando_tanque')
    odometro = data.get('odometro')
    abastecimento = Abastecimento(veiculo, valor, volume, completando_tanque, odometro)
    abastecimento.save()
    return 'Abastecimento salvo'

@app.delete('/api/abastecimentos', 
            tags=[abastecimento_tag], 
            responses={200: None, 400: BadRequestErrorSchema})
def deleteAbastecimento(query: AbastecimentoPath):
    """ Deleta um abastecimento pelo ID.
    """
    id = request.args.get('id')
    if id.isspace() or id == '':
        return "O parâmetro 'id' é obrigatório", 400
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM abastecimentos WHERE id = ?', (id,))
        conn.commit()
    finally:
        conn.close()
    return f"Abastecimento de ID {id} deletado!"
