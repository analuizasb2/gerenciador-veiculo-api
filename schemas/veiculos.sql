DROP TABLE IF EXISTS veiculos;

CREATE TABLE veiculos (
    placa TEXT NOT NULL PRIMARY KEY,
    marca TEXT NOT NULL,
    modelo TEXT NOT NULL,
    tipoCarroceria TEXT NOT NULL,
    anoFabricacao INTEGER NOT NULL,
    anoModelo INTEGER NOT NULL
);