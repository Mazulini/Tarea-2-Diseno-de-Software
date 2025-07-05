INSERT INTO usuario (id, nombre, correo, contrasena, telefono, fecha_registro, rol) VALUES
  (1, 'Juan Pérez', 'juan.perez@example.com', 'hashed_pw1', '+56912345678', '2025-01-15 09:30:00', 'cliente'),
  (2, 'María Gómez', 'maria.gomez@example.com', 'hashed_pw2','+56987654321', '2025-01-20 10:45:00', 'cliente'),
  (3, 'Pedro Ramírez', 'pedro.ramirez@example.com', 'hashed_pw3', '+56911223344', '2025-02-01 08:15:00', 'conductor'),
  (4, 'Lucía Díaz', 'lucia.diaz@example.com', 'hashed_pw4', '+56922334455', '2025-02-05 11:00:00', 'conductor'),
  (5, 'Pablo Admin', 'pablo.admin@example.com', 'hashed_pw5', '+56933445566', '2025-01-10 14:20:00', 'admin'),
  (6, 'Ana Torres',    'ana.torres@example.com',    'hashed_pw6', '+56944556677', '2025-02-10 12:00:00', 'cliente'),
  (7, 'Carlos Soto',   'carlos.soto@example.com',   'hashed_pw7', '+56955667788', '2025-02-12 15:30:00', 'cliente'),
  (8, 'Elena Martínez','elena.martinez@example.com','hashed_pw8', '+56966778899', '2025-02-15 09:45:00', 'conductor'),
  (9, 'Fernando Silva','fernando.silva@example.com','hashed_pw9', '+56977889900', '2025-02-18 11:20:00', 'conductor'),
  (10, 'Raúl Pinto',   'raul.pinto@example.com',    'hashed_pw10','+56988990011', '2025-02-20 14:10:00', 'cliente'),
  (11, 'Sofía Reyes',  'sofia.reyes@example.com',   'hashed_pw11','+56999001122', '2025-02-22 10:05:00', 'admin'),
  (12, 'Diego Rojas',  'diego.rojas@example.com',   'hashed_pw12','+56910111213', '2025-02-25 16:40:00', 'conductor'),
  (13, 'Valentina Arce','valentina.arce@example.com','hashed_pw13','+56912131415', '2025-02-28 13:55:00', 'cliente'),
  (14, 'Andrés Muñoz', 'andres.munoz@example.com',  'hashed_pw14','+56914151617', '2025-03-02 09:15:00', 'cliente'),
  (15, 'Paula Vega',   'paula.vega@example.com',    'hashed_pw15','+56916171819', '2025-03-05 12:30:00', 'conductor');

INSERT INTO cliente (usuario_id, direccion) VALUES
  (1, 'Avenida Libertador 1234, Santiago'),
  (2, 'Calle Serrano 567, Valparaíso'),
  (6,  'Calle San Martín 234, Ñuñoa, Santiago'),
  (7,  'Av. España 890, Concepción'),
  (10, 'Pasaje Los Nogales 45, Talca'),
  (13, 'Camino Real 1234, Puerto Montt'),
  (14, 'Calle Larga 567, La Serena');

INSERT INTO conductor (usuario_id, tipo_licencia) VALUES
  (3, 'A1'),
  (4, 'A2'),
  (8,  'A3'),
  (9,  'B'),
  (12, 'C'),
  (15, 'A2');

INSERT INTO admin (usuario_id) VALUES
  (5),
  (11);

INSERT INTO ruta (id, origen, destino, distancia_recorrida, fecha_hora_prevista) VALUES
  (1, 'Santiago', 'Valparaíso', 120.5, '2025-06-15 08:00:00'),
  (2, 'Valparaíso', 'Viña del Mar', 10.2, '2025-06-16 09:30:00'),
  (3, 'Santiago',    'Concepción', 300.0, '2025-06-17 08:00:00'),
  (4, 'Concepción',  'Temuco',     200.5, '2025-06-18 09:00:00'),
  (5, 'Temuco',      'Valdivia',   150.7, '2025-06-19 10:00:00');

INSERT INTO paquete (id, remitente, tipo, contenido, peso, dimensiones, destinatario, estado_entrega) VALUES
  (1, 1, 'documento', 'Factura pendiente', 2.5, '30x20x10', 2, 1),
  (2, 2, 'mercancía', 'Repuestos mecánicos', 5.0, '50x40x20', 1, 1),
  (3, 6,  'mercancía', 'Componentes electrónicos', 3.2, '40x30x20', 7, 1),
  (4, 7,  'documento', 'Contrato firmado', 1.0, '25x20x1', 6, 1),
  (5, 10, 'mercancía', 'Ropa deportiva', 4.5, '45x35x15', 13, 2),
  (6, 13, 'otro', 'Regalo cumpleaños', 2.0, '30x30x30', 10, 1);

INSERT INTO envio (id, ruta_id, conductor_id, fecha_hora_inicio, fecha_hora_fin) VALUES
  (1, 1, 3, '2025-06-15 07:50:00', NULL),
  (2, 2, 4, '2025-06-16 09:20:00', NULL),
  (3, 3,  8,  '2025-06-17 07:50:00', NULL),
  (4, 4,  9,  '2025-06-18 08:50:00', NULL),
  (5, 5, 12,  '2025-06-19 09:50:00', NULL);

INSERT INTO envio_paquete (envio_id, paquete_id) VALUES
  (1, 1),
  (2, 2),
  (3, 3),
  (4, 4),
  (5, 5),
  (5, 6);

INSERT INTO historial_estados (id, paquete_id, estado_id, fecha_cambio) VALUES
  (1, 1, 1, '2025-06-10 10:00:00'),
  (2, 1, 2, '2025-06-12 14:30:00'),
  (3, 2, 1, '2025-06-11 11:15:00'),
  (4, 3, 1, '2025-06-15 08:30:00'),
  (5, 3, 2, '2025-06-16 12:00:00'),
  (6, 4, 1, '2025-06-16 09:10:00'),
  (7, 5, 1, '2025-06-18 09:30:00'),
  (8, 6, 1, '2025-06-19 10:05:00');

INSERT INTO notificacion (id, envio_id, paquete_id, usuario_id, mensaje, fecha_envio, leido) VALUES
  (1, 1, 1, 1, 'Están llegando las facturas', '2025-06-10 10:05:00', True),
  (2, 2, 2, 2, 'Los repuestos están en camino', '2025-06-12 14:35:00', False),
  (3, 3, 3, 6, 'Tu paquete ha sido asignado al conductor', '2025-06-15 08:35:00', False),
  (4, 4, 4, 7, 'Contrato en camino', '2025-06-16 09:15:00', True),
  (5, 5, 5,10, 'Tu paquete está en tránsito', '2025-06-18 09:45:00', False),
  (6, 5, 6,13, '¡Feliz cumpleaños! Tu regalo va en camino', '2025-06-19 10:15:00', False);

INSERT INTO reporte (id, conductor_id, ruta_id, fecha_generacion, contenido) VALUES
  (1, 3, 1, '2025-06-15 09:00:00', 'Zona de mucha niebla'),
  (2, 4, 2, '2025-06-16 10:00:00', 'Socavon en mitad del camino'),
  (3,  8, 3, '2025-06-17 09:30:00', 'Retraso por tráfico pesado'),
  (4,  9, 4, '2025-06-18 10:30:00', 'Ruta despejada, sin problemas'),
  (5, 12, 5, '2025-06-19 11:00:00', 'Lluvia intensa, precaución');

INSERT INTO estadistica_ruta (id, ruta_id, conductor_id, fecha_periodo, tiempo_real_min, distancia_recorrida_km, eficiencia) VALUES
  (1, 1, 4, '2025-06-10 10:05:00', 100.00, 120.00, 500.00),
  (2, 2, 3, '2025-06-10 10:05:00', 60.00, 85.00, 650.00),
  (3, 3,  8, '2025-06-15 12:00:00', 320.00, 300.00, 400.00),
  (4, 4,  9, '2025-06-16 12:00:00', 210.00, 200.50, 570.00),
  (5, 5, 12, '2025-06-17 12:00:00', 160.00, 150.70, 550.00);