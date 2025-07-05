CREATE TYPE usuario_rol AS ENUM ('cliente', 'conductor', 'admin');

CREATE TABLE usuario (
  id                BIGSERIAL       PRIMARY KEY,
  nombre            VARCHAR(100)    NOT NULL,
  correo            VARCHAR(150)    UNIQUE NOT NULL,
  contrasena        VARCHAR(200)    NOT NULL,
  telefono          VARCHAR(20),
  fecha_registro    TIMESTAMP       NOT NULL DEFAULT NOW(),
  rol               usuario_rol     NOT NULL
);

CREATE INDEX idx_usuario_rol ON usuario(rol);
CREATE INDEX idx_usuario_correo ON usuario(correo);

CREATE TABLE cliente (
  usuario_id        BIGINT          PRIMARY KEY REFERENCES usuario(id) ON DELETE CASCADE,
  direccion         VARCHAR(300)    NOT NULL
);

CREATE INDEX idx_cliente_usuario ON cliente(usuario_id);

CREATE TABLE conductor (
  usuario_id        BIGINT          PRIMARY KEY REFERENCES usuario(id) ON DELETE CASCADE,
  tipo_licencia     VARCHAR(100)    NOT NULL,

  CONSTRAINT fk_conductor_usuario
    FOREIGN KEY(usuario_id) REFERENCES usuario(id)
      ON DELETE CASCADE
);
CREATE INDEX idx_conductor_usuario ON conductor(usuario_id);

CREATE TABLE admin (
  usuario_id        BIGINT          PRIMARY KEY REFERENCES usuario(id) ON DELETE CASCADE
);
CREATE INDEX idx_admin_usuario ON admin(usuario_id);

CREATE TABLE estado_de_entrega (
  id                SERIAL          PRIMARY KEY,
  nombre_estado     VARCHAR(50)     UNIQUE NOT NULL
);

INSERT INTO estado_de_entrega(nombre_estado) VALUES
  ('En preparación'),
  ('En tránsito'),
  ('Entregado'),
  ('Fallido');

CREATE TABLE ruta (
  id                         SERIAL        PRIMARY KEY,
  origen                     VARCHAR(255)  NOT NULL,
  destino                    VARCHAR(255)  NOT NULL,
  distancia_recorrida        NUMERIC(10,2),
  fecha_hora_prevista        TIMESTAMP      NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_ruta_origen ON ruta(origen);
CREATE INDEX idx_ruta_destino ON ruta(destino);

CREATE TABLE envio (
  id                         SERIAL         PRIMARY KEY,
  ruta_id                    INTEGER
                                   REFERENCES ruta(id) ON DELETE RESTRICT,
  conductor_id               BIGINT         NOT NULL
                                   REFERENCES conductor(usuario_id) ON DELETE RESTRICT,
  fecha_hora_inicio          TIMESTAMP      NOT NULL DEFAULT NOW(),
  fecha_hora_fin             TIMESTAMP
);

CREATE INDEX idx_envio_ruta       ON envio(ruta_id);
CREATE INDEX idx_envio_conductor  ON envio(conductor_id);

CREATE TABLE paquete (
  id                         SERIAL         PRIMARY KEY,
  remitente                  BIGINT         NOT NULL
                                   REFERENCES cliente(usuario_id) ON DELETE CASCADE,
  tipo                       VARCHAR(100)   NOT NULL,
  contenido                  TEXT,
  peso                       NUMERIC(10,2)  NOT NULL,
  dimensiones                VARCHAR(50),
  destinatario               BIGINT         NOT NULL
                                   REFERENCES cliente(usuario_id) ON DELETE CASCADE,
  estado_entrega             INTEGER        NOT NULL
                                   REFERENCES estado_de_entrega(id) ON DELETE RESTRICT
);

CREATE INDEX idx_paquete_cliente     ON paquete(remitente);
CREATE INDEX idx_paquete_estado      ON paquete(estado_entrega);

CREATE TABLE historial_estados (
  id                         SERIAL         PRIMARY KEY,
  paquete_id                 INTEGER        NOT NULL
                                   REFERENCES paquete(id) ON DELETE CASCADE,
  estado_id                  INTEGER        NOT NULL
                                   REFERENCES estado_de_entrega(id) ON DELETE RESTRICT,
  fecha_cambio               TIMESTAMP     NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_historial_paquete  ON historial_estados(paquete_id);

CREATE TABLE envio_paquete (
  envio_id                   INTEGER       NOT NULL
                                   REFERENCES envio(id) ON DELETE CASCADE,
  paquete_id                 INTEGER       NOT NULL
                                   REFERENCES paquete(id) ON DELETE CASCADE,
  PRIMARY KEY (envio_id, paquete_id)
);

CREATE INDEX idx_envio_paquete_paquete  ON envio_paquete(paquete_id);

CREATE TABLE notificacion (
  id                         SERIAL        PRIMARY KEY,
  envio_id                   INTEGER       NOT NULL
                                   REFERENCES envio(id) ON DELETE CASCADE,
  paquete_id                 INTEGER       NOT NULL
                                   REFERENCES paquete(id) ON DELETE CASCADE,
  usuario_id                 BIGINT        NOT NULL
                                   REFERENCES usuario(id) ON DELETE CASCADE,
  mensaje                    TEXT          NOT NULL,
  fecha_envio                TIMESTAMP     NOT NULL DEFAULT NOW(),
  leido                      BOOLEAN       NOT NULL DEFAULT FALSE
);

CREATE INDEX idx_notif_usuario  ON notificacion(usuario_id);
CREATE INDEX idx_notif_envio    ON notificacion(envio_id);

CREATE TABLE reporte (
  id                         SERIAL        PRIMARY KEY,
  conductor_id               BIGINT        NOT NULL
                                   REFERENCES conductor(usuario_id) ON DELETE RESTRICT,
  ruta_id                    INTEGER       NOT NULL
                                   REFERENCES ruta(id) ON DELETE RESTRICT,
  fecha_generacion           TIMESTAMP     NOT NULL DEFAULT NOW(),
  contenido                  VARCHAR(500)  NOT NULL
                                   
);

CREATE INDEX idx_reporte_conductor ON reporte(conductor_id);
CREATE INDEX idx_reporte_ruta      ON reporte(ruta_id);


CREATE TABLE estadistica_ruta (
  id                         SERIAL        PRIMARY KEY,
  ruta_id                    INTEGER       NOT NULL
                                   REFERENCES ruta(id) ON DELETE CASCADE,
  conductor_id               BIGINT        NOT NULL
                                   REFERENCES conductor(usuario_id) ON DELETE CASCADE,
  fecha_periodo              DATE          NOT NULL,
  tiempo_real_min            NUMERIC(10,2),
  distancia_recorrida_km     NUMERIC(10,2),
  eficiencia                 NUMERIC(5,2)
);

CREATE INDEX idx_est_ruta      ON estadistica_ruta(ruta_id);
CREATE INDEX idx_est_conductor ON estadistica_ruta(conductor_id);
CREATE UNIQUE INDEX idx_est_unico_ruta_fecha ON estadistica_ruta(ruta_id, fecha_periodo);
