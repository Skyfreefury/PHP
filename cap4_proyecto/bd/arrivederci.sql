-- =====================================================
-- Arrivederci · Base de datos de la tienda de pizzería
-- Se puede ejecutar varias veces sin errores ni duplicados.
-- =====================================================

CREATE DATABASE IF NOT EXISTS arrivederci
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE arrivederci;

-- ---------- Tablas sin claves ajenas ----------

CREATE TABLE IF NOT EXISTS categoria (
    ID_Categoria INT AUTO_INCREMENT PRIMARY KEY,
    Nombre       VARCHAR(45)  NOT NULL UNIQUE,
    Descripcion  VARCHAR(200)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS cliente (
    ID_Cliente INT AUTO_INCREMENT PRIMARY KEY,
    Nombre     VARCHAR(45)  NOT NULL,
    Correo     VARCHAR(90)  NOT NULL UNIQUE,   -- usuario del login (RN-05)
    Clave      VARCHAR(255) NOT NULL,          -- resultado de password_hash (RNF-01)
    Direccion  VARCHAR(200) NOT NULL
) ENGINE=InnoDB;

-- ---------- Tablas con claves ajenas ----------

CREATE TABLE IF NOT EXISTS producto (
    ID_Producto  INT AUTO_INCREMENT PRIMARY KEY,
    Nombre       VARCHAR(45)  NOT NULL,
    Descripcion  VARCHAR(200),
    Precio       DECIMAL(6,2) NOT NULL,
    Stock        INT          NOT NULL DEFAULT 0,  -- solo informativo
    ID_Categoria INT          NOT NULL,
    FOREIGN KEY (ID_Categoria) REFERENCES categoria(ID_Categoria)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS pedido (
    ID_Pedido  INT AUTO_INCREMENT PRIMARY KEY,
    Fecha      DATETIME   NOT NULL,
    Enviado    TINYINT(1) NOT NULL DEFAULT 0,      -- nuevo pedido = no enviado (RN-02)
    ID_Cliente INT        NOT NULL,
    FOREIGN KEY (ID_Cliente) REFERENCES cliente(ID_Cliente)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS pedido_producto (
    ID_Pedido   INT          NOT NULL,
    ID_Producto INT          NOT NULL,
    Unidades    INT          NOT NULL,             -- de 1 a 10 (RN-01)
    Precio      DECIMAL(6,2) NOT NULL,             -- precio en el momento del pedido (RN-03)
    PRIMARY KEY (ID_Pedido, ID_Producto),
    FOREIGN KEY (ID_Pedido)   REFERENCES pedido(ID_Pedido),
    FOREIGN KEY (ID_Producto) REFERENCES producto(ID_Producto)
) ENGINE=InnoDB;

-- ---------- Datos ----------
-- INSERT IGNORE + códigos fijos: si la fila ya existe, no se duplica.

INSERT IGNORE INTO categoria (ID_Categoria, Nombre, Descripcion) VALUES
    (1, 'Pizzas',       'Pizzas al horno de leña'),
    (2, 'Bebidas',      'Refrescos y agua'),
    (3, 'Complementos', 'Para acompañar la pizza');

INSERT IGNORE INTO producto (ID_Producto, Nombre, Descripcion, Precio, Stock, ID_Categoria) VALUES
    -- Pizzas (8)
    (1,  'Margarita',       'Tomate, mozzarella, albahaca fresca y aceite de oliva.',  9.50, 24, 1),
    (2,  'Bacon',           'Tomate, mozzarella y taquitos de bacon ahumado.',        10.50, 15, 1),
    (3,  'Peperoni',        'Tomate, mozzarella y peperoni curado.',                  11.00, 18, 1),
    (4,  'Jamón',           'Tomate, mozzarella y jamón cocido.',                     10.00, 12, 1),
    (9,  'Cuatro quesos',   'Mozzarella, gorgonzola, parmesano y emmental.',          11.50, 14, 1),
    (10, 'Barbacoa',        'Salsa barbacoa, mozzarella, carne picada y bacon.',      12.00, 16, 1),
    (11, 'Hawaiana',        'Tomate, mozzarella, jamón cocido y piña.',               10.50, 10, 1),
    (12, 'Vegetal',         'Tomate, mozzarella, pimiento, champiñón y cebolla.',     10.00, 13, 1),
    -- Bebidas (8)
    (5,  'Coca-Cola',       'Lata de 33 cl.',                                          2.00, 50, 2),
    (6,  'Agua',            'Botella de 50 cl.',                                       1.50, 60, 2),
    (13, 'Coca-Cola Zero',  'Lata de 33 cl, sin azúcar.',                              2.00, 40, 2),
    (14, 'Fanta Naranja',   'Lata de 33 cl.',                                          2.00, 35, 2),
    (15, 'Nestea',          'Lata de 33 cl, té al limón.',                             2.00, 30, 2),
    (16, 'Agua con gas',    'Botella de 50 cl.',                                       1.80, 25, 2),
    (17, 'Cerveza',         'Botellín de 33 cl.',                                      2.50, 40, 2),
    (18, 'Zumo de naranja', 'Botella de 33 cl, naranja exprimida.',                    2.80, 20, 2),
    -- Complementos (8)
    (7,  'Patatas fritas',  'Ración de patatas fritas crujientes.',                    3.50, 30, 3),
    (8,  'Aros de cebolla', 'Ración de 8 aros de cebolla rebozados.',                  4.00, 25, 3),
    (19, 'Alitas de pollo', 'Ración de 6 alitas de pollo al horno.',                   5.50, 20, 3),
    (20, 'Pan de ajo',      'Pan horneado con mantequilla de ajo y perejil.',          3.00, 22, 3),
    (21, 'Nuggets',         'Ración de 8 nuggets de pollo.',                           4.50, 28, 3),
    (22, 'Ensalada César',  'Lechuga, pollo, parmesano, picatostes y salsa César.',    6.00, 15, 3),
    (23, 'Patatas gajo',    'Ración de patatas gajo con especias.',                    3.80, 26, 3),
    (24, 'Tequeños',        'Ración de 6 palitos de queso rebozados.',                 4.80, 18, 3);

-- Cliente de prueba · correo: cliente@pizzeria.es · clave: 1234
INSERT IGNORE INTO cliente (ID_Cliente, Nombre, Correo, Clave, Direccion) VALUES
    (1, 'Cliente de prueba', 'cliente@pizzeria.es',
     '$2y$10$trYIALEXoteyRlvV54d92u6DG1/t6f0i7bdZ1oMeBc9Urcy7AgvS6',
     'Calle Mayor 1, 28001 Madrid');
