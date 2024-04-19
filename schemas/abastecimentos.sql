DROP TABLE IF EXISTS abastecimentos;

CREATE TABLE abastecimentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    horario TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    veiculo TEXT NOT NULL,
    valor NUMERIC NOT NULL,
    volume NUMERIC NOT NULL,
    completandoTanque BOOLEAN NOT NULL,
    odometro INTEGER NOT NULL,
    FOREIGN KEY(veiculo) REFERENCES veiculos(placa)
);