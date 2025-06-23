# 🧺 CestaMágica

**CestaMágica** es una aplicación web desarrollada para modernizar la operación y ventas de una distribuidora de confites, helados, abarrotes y artículos de cumpleaños. Brinda una experiencia de compra moderna tanto para clientes como para administradores del sistema.

## 🚀 Características Principales

- 🔍 **Catálogo Dinámico**: Visualización clara y organizada de productos con filtros, paginación y ofertas destacadas.
- 👤 **Gestión de Usuarios**: Registro, autenticación y administración de sesiones para clientes.
- 🛒 **Carrito de Compras Mejorado**:
  - Botones `+` y `-` para ajustar cantidades sin recargar la página.
  - Confirmación manual de agregados.
  - Indicador visual del número de productos.
- 💳 **Pagos con Webpay**: Integración con Transbank (modo sandbox) para procesar pagos seguros.
- 📦 **Sistema de Pedidos**:
  - Confirmación y resumen visual del pedido.
  - Generación automática de un código único por pedido.
  - PDF descargable con el detalle del pedido y logo personalizado.
- 🧾 **PDF del Pedido**:
  - Incluye productos, cantidades, subtotales, totales, métodos de retiro y pago.
  - Diseño limpio con logo de empresa alineado correctamente.
- 🛠️ **Gestión de Inventario (Admin)**:
  - Agregar, editar o eliminar productos.
  - Marcas personalizables desde la interfaz.
- 🖼️ **Diseño Adaptativo**: Compatible con pantallas móviles y de escritorio.
- ✅ **Toasts Personalizados**: Notificaciones visuales modernas para acciones del usuario.

## 🧑‍💻 Tecnologías Utilizadas

| Tecnología     | Rol                               |
|----------------|------------------------------------|
| Django         | Backend y gestión de sesiones     |
| SQLite         | Base de datos (por ahora)         |
| HTML/CSS/JS    | Interfaz web básica               |
| jQuery         | AJAX para carrito dinámico        |
| ReportLab      | Generación de PDF de pedidos      |
| Transbank SDK  | Integración con Webpay Plus       |
| Bootstrap Icons| Íconos en UI                      |


## Instalación
Para ejecutar el proyecto en tu entorno local, sigue estos pasos:

1. Clona el repositorio:
   ```sh
   git clone https://github.com/maarroyo76/CestaMagica.git
   ```
2. Accede al directorio del proyecto:
   ```sh
   cd CestaMagica
   ```
3. Crea un entorno virtual y actívalo:
   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```
4. Instala las dependencias:
   ```sh
   pip install -r requirements.txt
   ```
5. Aplica las migraciones de la base de datos:
   ```sh
   python manage.py migrate
   ```
6. Ejecuta el servidor local:
   ```sh
   python manage.py runserver
   ```

## Uso
- Accede a `http://127.0.0.1:8000/` para ver la aplicación en funcionamiento.
- Regístrate o inicia sesión para acceder a más funcionalidades.
- Explora el catálogo de productos.

## Estado del Proyecto
El proyecto se encuentra en desarrollo activo. Las siguientes implementaciones en curso incluyen:
- Sistema de descuentos automatico
- Programa de fidelizacion
- Sistema de reseñas para productos
- Historial de pedidos del usuario

---
**Contacto:** Si tienes preguntas o sugerencias, no dudes en abrir un issue en el repositorio.
