import sqlite3

DB_NAME = 'gerenciador_veiculos.db'
connection = sqlite3.connect(DB_NAME)

def execute_sql_file(filename):
        cursor = connection.cursor()
        with open(filename, 'r') as sql_file:
            sql_script = sql_file.read()
            cursor.executescript(sql_script)

execute_sql_file('./schemas/veiculos.sql')
execute_sql_file('./schemas/abastecimentos.sql')

cursor = connection.cursor()
cursor.execute("INSERT INTO veiculos VALUES ('ABC-1234', 'Toyota', 'Etios', 'Sedan', '2019', '2020')")

cursor.execute("INSERT INTO abastecimentos (veiculo, valor, volume, completandoTanque, odometro) VALUES ('ABC-1234', 127.40, 23.5, true, 14563)")
cursor.execute("INSERT INTO abastecimentos (veiculo, valor, volume, completandoTanque, odometro) VALUES ('ABC-1234', 54.65, 12.9, false, 15546)")

connection.commit()
connection.close()