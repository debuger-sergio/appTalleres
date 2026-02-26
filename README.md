# TallerApp 🛠️

TallerApp es una aplicación web integral diseñada para la gestión de talleres mecánicos. Permite administrar clientes, vehículos, órdenes de trabajo, presupuestos y facturación de manera eficiente y profesional.

## ✨ Características Principales

- **Dashboard Inteligente:** Visualización rápida de métricas (clientes, vehículos, órdenes pendientes).
- **Gestión de Clientes:** Base de datos completa de clientes con historial vinculado.
- **Control de Vehículos:** Validación de años de fabricación y normalización automática de matrículas a mayúsculas.
- **Órdenes de Trabajo (OT):** Seguimiento detallado del estado de las reparaciones (Pendiente, En Proceso, Terminado, Entregado).
- **Sistema de Presupuestos:** Creación de presupuestos y conversión automática a Órdenes de Trabajo tras aprobación.
- **Facturación Automática:** Generación de facturas profesionales listas para imprimir o guardar como PDF.
- **Multi-taller:** Arquitectura diseñada para que cada usuario gestione su propio taller de forma independiente.
- **Integración Continua:** Configuración de GitHub Actions para asegurar la calidad mediante tests automáticos.

## 🚀 Tecnologías Utilizadas

- **Backend:** Django (Python)
- **Frontend:** HTML5, CSS3 (Vanilla), Bootstrap 5
- **Base de Datos:** SQLite (desarrollo)
- **Gestión de Estáticos:** WhiteNoise
- **CI/CD:** GitHub Actions

## 📦 Instalación y Configuración

Siga estos pasos para ejecutar el proyecto en su entorno local:

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/debuger-sergio/appTalleres.git
   cd AppTallerMecanico
   ```

2. **Crear y activar un entorno virtual:**
   ```bash
   python -m venv .venv
   # En Windows:
   .\.venv\Scripts\activate
   # En Linux/Mac:
   source .venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Realizar migraciones:**
   ```bash
   python manage.py migrate
   ```

5. **Crear un superusuario:**
   ```bash
   python manage.py createsuperuser
   ```

6. **(Opcional) Cargar datos de prueba:**
   ```bash
   python manage.py populate_data
   ```

7. **Iniciar el servidor:**
   ```bash
   python manage.py runserver
   ```

La aplicación estará disponible en `http://127.0.0.1:8000/`.

## 🧪 Pruebas

Para ejecutar la suite de tests automáticos:
```bash
python manage.py test
```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

---
Desarrollado con ❤️ para la gestión profesional de talleres.
