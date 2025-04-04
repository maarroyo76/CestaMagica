# CestaMágica

CestaMágica es un proyecto de desarrollo web diseñado para mejorar la presencia digital y la eficiencia operativa de una distribuidora de confites, helados, abarrotes y artículos de cumpleaños. Su objetivo es proporcionar una plataforma fácil de usar para visualizar el inventario y optimizar el proceso de compra y gestión de pedidos.

## Características Principales
- **Visualización de Inventario:** Presentación organizada de productos con secciones de ofertas y destacados.
- **Gestión de Usuarios:** Registro y autenticación de clientes.
- **Carrito de Compras:** Permite a los usuarios guardar productos antes de realizar el pago.
- **Procesamiento de Pedidos:** Generación de un ID de pedido para retiro en tienda.
- **Gestión de Inventario:** Permisos restringidos para administración de productos.
- **Precios Dinámicos:** Diferenciación de precios según la cantidad adquirida.

## Tecnologías Utilizadas
- **Backend:** Django (con posibilidad de usar Django Rest Framework en el futuro).
- **Base de Datos:** SQLite (por ahora, con posibilidad de optimización futura).
- **Frontend:** HTML, CSS, JavaScript (posible integración con frameworks en el futuro).

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
   source venv/bin/activate  # En Windows: venv\Scripts\activate
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
- Desarrollo del sistema de pedidos (carrito de compras y vista de pago).
- Integración con una plataforma de pagos en línea.
- Gestión de pedidos por parte del equipo administrativo.

---
**Contacto:** Si tienes preguntas o sugerencias, no dudes en abrir un issue en el repositorio.
