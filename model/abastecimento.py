import sqlite3
from datetime import datetime
from pydantic import BaseModel
from typing import List

DB_NAME = 'gerenciador_veiculos.db'

class AbastecimentoPath(BaseModel):
    id: str

class AbastecimentoInsertSchema(BaseModel):
    veiculo: str
    valor: float
    volume: float
    completando_tanque: bool
    odometro: int

class AbastecimentoSchema(BaseModel):
    id: int
    horario: str
    valor: float
    volume: float
    completando_tanque: bool
    odometro: int

class AbastecimentoListSchema(BaseModel):
    abastecimentos: List[AbastecimentoSchema]

class Abastecimento:
    def __init__(self, veiculo, valor, volume, completando_tanque, odometro, horario = datetime.now()):
        self.horario = horario
        self.veiculo = veiculo
        self.valor = valor
        self.volume = volume
        self.completando_tanque = completando_tanque
        self.odometro = odometro

    def save(self):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO abastecimentos (veiculo, valor, volume, completandoTanque, odometro) VALUES (?, ?, ?, ?, ?)", 
                        (self.veiculo, self.valor, self.volume, self.completando_tanque, self.odometro,))
            conn.commit()
        finally:
            conn.close()