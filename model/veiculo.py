from pydantic import BaseModel
from typing import List
import sqlite3

DB_NAME = 'gerenciador_veiculos.db'

class VeiculoSchema(BaseModel):
    placa: str = "undefined"
    marca: str = "undefined"
    modelo: str = "undefined"
    tipo_carroceria: str = "undefined"
    ano_fabricacao: int = 0
    ano_modelo: int = 0

class VeiculoPath(BaseModel):
    Placa: str

class VeiculoListSchema(BaseModel):
    veiculos: List[VeiculoSchema]

class Veiculo:
    def __init__(self, placa, marca, modelo, tipo_carroceria, ano_fabricacao, ano_modelo):
        self.placa = placa
        self.marca = marca
        self.modelo = modelo
        self.tipo_carroceria = tipo_carroceria
        self.ano_fabricacao = ano_fabricacao
        self.ano_modelo = ano_modelo

    def save(self):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO veiculos VALUES (?, ?, ?, ?, ?, ?)", (self.placa, self.marca, self.modelo, self.tipo_carroceria, self.ano_fabricacao, self.ano_modelo,))
            conn.commit()
        finally:
            conn.close()