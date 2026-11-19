# Instrucciones de diseño · Arrivederci

Reglas fijas para cualquier pantalla o prototipo del proyecto. La fuente de verdad es `memoria/ERS_borrador.md`: si una pantalla contradice la ERS, manda la ERS.

## Marca

- Nombre: **Arrivederci** (así, con "d"). Tienda web de una pizzería.

## Catálogo: exactamente 3 categorías con 8 productos cada una (24)

| Categoría | Productos |
|---|---|
| Pizzas | Margarita, Bacon, Peperoni, Jamón, Cuatro quesos, Barbacoa, Hawaiana, Vegetal |
| Bebidas | Coca-Cola, Agua, Coca-Cola Zero, Fanta Naranja, Nestea, Agua con gas, Cerveza, Zumo de naranja |
| Complementos | Patatas fritas, Aros de cebolla, Alitas de pollo, Pan de ajo, Nuggets, Ensalada César, Patatas gajo, Tequeños |

- No añadir otros productos (nada de Diavola, Carbonara, Sprite…).
- Cada producto muestra: nombre, descripción, precio y stock.
- No inventar campos que no están en la base de datos (etiquetas "Vegetariana", "Más pedida", "Picante"…).

## Stock

- El stock es solo informativo ("24 disponibles").
- Nunca bloquea la compra: no existe el estado "Agotado" ni botones deshabilitados por stock.

## Carrito y pedido

- Unidades por producto: de 1 a 10 (RN-01).
- El total es la suma de precio × unidades (RF-07).
- El pedido nuevo queda "no enviado" (RN-02). No hay pago con tarjeta en esta versión.

## Pantallas de la ERS (apartado 8)

| Fichero | Pantalla | Requisitos |
|---|---|---|
| `memoria/prototipo_8_1_login.png` | Login con correo recordado por cookie y aviso de error | RF-01, RF-12 |
| `memoria/prototipo_8_2_productos.png` | Productos de una categoría con unidades y «Añadir» | RF-03, RF-04, RF-05 |
| `memoria/prototipo_8_3_carrito.png` | Carrito con unidades, «Eliminar», total y «Realizar pedido» | RF-06 a RF-10 |
| `memoria/prototipo_8_3b_confirmacion.png` | Confirmación con número de pedido | RF-11 |

- Exportar con esos mismos nombres para que el PDF de la ERS los recoja.
- No editar `memoria/ERS_borrador.md` ni los PDF: los mantiene la sesión de VS Code.

## Decoración

- Vídeo de fondo de Blender y animaciones GSAP solo en el inicio público (RF-15).
- Todo es opcional (RNF-06): sin JavaScript o sin vídeo, la tienda funciona igual.
