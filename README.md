# 🧺 CestaMágica

**CestaMágica** es una aplicación web completa de comercio electrónico desarrollada en Django. Creada para una distribuidora de confites, abarrotes y más, esta plataforma moderniza la operación de ventas con un robusto sistema de gestión de inventario, un flujo de pago seguro y una potente interfaz de administración.

El sistema está diseñado para ser seguro, eficiente y fácil de usar tanto para los clientes como para los administradores de la tienda, con una lógica de negocio que maneja el inventario de forma inteligente desde la compra hasta la entrega.

## ✨ Características Principales

El proyecto se divide en dos experiencias principales: la tienda orientada al cliente y un potente panel de gestión para el administrador.

### 👩‍💻 Para Clientes

* **Catálogo de Productos Dinámico:** Navegación fluida por el catálogo con filtros por nombre, marca, categoría y opciones de ordenamiento.
* **Búsqueda Rápida (Live Search):** Una barra de búsqueda en el *navbar* que proporciona resultados instantáneos (con imagen y precio) mientras el usuario escribe.
* **Carrito de Compras AJAX:** Carrito 100% dinámico. Los usuarios pueden agregar, decrementar y eliminar productos sin recargar la página.
* **Gestión de Cuentas:** Sistema completo de registro, inicio de sesión y perfil de usuario.
* **Flujo de Pago Seguro:** Integración completa con **Transbank Webpay**. El sistema valida el stock antes de pagar, descuenta el inventario y revierte la operación si el pago falla.
* **Historial de Pedidos:** Los usuarios pueden ver un historial de todas sus compras pasadas, descargar un **comprobante en PDF** de cada una y acceder a la función de **"Volver a Comprar"**.
* **Volver a Comprar:** Un botón en el historial de pedidos que añade todos los productos de un pedido antiguo al carrito, verificando el stock disponible en el proceso.

### 🛠️ Para Administradores

* **Panel de Gestión Personalizado:** Una vista de `/gestion` que centraliza la administración de productos, pedidos, marcas y categorías.
* **Gestión de Pedidos:** Los administradores pueden ver todos los pedidos y filtrar por estado o fecha, además de actualizar el estado del envío (ej. "En preparación", "Entregado").
* **Gestión de Inventario (CRUD):** Formularios protegidos por roles para crear, editar y eliminar productos, marcas y categorías.
* **Carga y Actualización Masiva (Excel + ZIP):** La característica más potente. El admin puede:
    1.  **Descargar** una plantilla Excel (`.xlsx`) con todo el inventario actual (incluyendo el `id` de la base de datos).
    2.  Modificar cualquier dato en el Excel (precio, stock, `id_tienda`, nombre, etc.).
    3.  Añadir filas para productos nuevos (dejando la columna `id` en blanco).
    4.  **Subir** el Excel junto a un archivo `.zip` opcional con las imágenes de los productos *nuevos*.
    5.  El sistema **actualiza** los productos existentes (usando el `id` como llave) y **crea** los nuevos, asignando sus imágenes automáticamente.

## 🧠 Lógica de Negocio Destacada

* **Manejo Transaccional de Stock:** El stock solo se descuenta *después* de que la vista de `confirmar_pedido` valida que hay existencias, y todo el proceso está envuelto en un `transaction.atomic()`.
* **Restauración de Stock:** Si el pago es rechazado por Transbank, el usuario cancela, o la API de Webpay falla, el sistema automáticamente **revierte la transacción** y devuelve el stock "reservado" al inventario.
* **Stock de Seguridad:** El modelo `Producto` tiene un `STOCK_UMBRAL_MINIMO` (fijado en 3). Los clientes solo pueden comprar el `stock_vendible` (stock real - 3). Cuando el stock llega a 3, el producto se muestra como "Sin Stock" en toda la tienda.
* **Creación Automática de Perfiles:** Se usan Señales de Django (`post_save`) para crear automáticamente un `userProfile` cada vez que se crea un `User` nuevo, sin importar si fue por registro, por el admin o por `createsuperuser`.
* **Optimización N+1:** Las consultas a la base de datos en las vistas de listas (productos, historial) usan `select_related` y `prefetch_related` para minimizar los "hits" a la base de datos y asegurar un rendimiento rápido.

## 🧑‍💻 Pila Tecnológica

| Tecnología | Rol |
| :--- | :--- |
| **Python** | Lenguaje principal del backend. |
| **Django** | Framework principal para toda la lógica, vistas y modelos. |
| **SQLite** | Base de datos ligera para desarrollo. |
| **Django Rest Framework** | Para construir la API (`/api/`) del proyecto. |
| **Bootstrap 5** | Framework CSS para el diseño responsive. |
| **jQuery** | Para las interacciones dinámicas del frontend (AJAX). |
| **Transbank SDK** | SDK oficial para la integración de pagos con Webpay Plus. |
| **Openpyxl** | Librería para leer y escribir archivos Excel (`.xlsx`) en las cargas masivas. |
| **ReportLab** | Para la generación de comprobantes de pedido en PDF. |
| **Python-Decouple** | Para gestionar secretos y variables de entorno (`.env`). |


## 🔮 Próximos Pasos (Roadmap)

El proyecto tiene una base sólida para crecer. Los siguientes pasos lógicos incluyen:

* **Sistema de Cupones:** Crear un modelo `Cupon` para aplicar descuentos en el carrito.
* **Reseñas de Productos:** Permitir a los usuarios que compraron un producto dejar una calificación y un comentario.
* **Despliegue en Producción:** Configurar el proyecto para un servidor real usando MySQL y S3 para el almacenamiento de imágenes.