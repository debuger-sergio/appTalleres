# Sistema de Gestión de Talleres - Sevilla Motor 🛠️

Este documento constituye el manual oficial de operación y guía técnica para la plataforma de gestión de **Talleres Sevilla Motor**.

---

## 👥 Guía para el Personal del Taller (Trabajadores)

Esta sección explica cómo utilizar la herramienta en el día a día para gestionar las reparaciones y los clientes.

### 1. Acceso al Sistema
Para abrir la aplicación, asegúrese de que el servidor esté encendido y acceda desde el navegador a la siguiente dirección:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

### 2. Flujo de Trabajo Diario

#### A. Recepción del Vehículo
1.  Vaya a la sección **Clientes** y verifique si el cliente ya existe. Si no, créelo.
2.  Vaya a **Vehículos** y registre el coche del cliente (la matrícula se guardará automáticamente en mayúsculas).
3.  Cree una **Nueva Orden de Trabajo (OT)** detallando el problema y el kilometraje actual.

#### B. Durante la Reparación
1.  Actualice el **Estado** de la orden (de *Pendiente* a *En Proceso*) para que el resto del equipo sepa en qué se está trabajando.
2.  Una vez finalizado el trabajo, marque la orden como **Terminada**.

#### C. Entrega y Facturación
1.  Desde la ficha de la Orden de Trabajo, pulse el botón **"Generar Factura"**.
2.  El sistema asignará automáticamente un número de factura legal.
3.  Pulse **"Imprimir / PDF"** para entregar el documento al cliente.
4.  Marque la orden como **Entregada**.

---

## 🛠️ Guía para Administradores (Instalación Técnica)

Manual para la puesta en marcha inicial del servidor.

### Requisitos Previos
- Python 3.10 o superior instalado.
- Dependencias listadas en `requirements.txt`.

### Pasos de Ejecución
1.  **Activar el entorno:** 
    ```powershell
    .\.venv\Scripts\activate
    ```
2.  **Iniciar el servicio:**
    ```powershell
    python manage.py runserver
    ```
3.  **Mantenimiento de datos:**
    - Para actualizar la base de datos: `python manage.py migrate`
    - Para generar datos de ejemplo: `python manage.py populate_data`

---

## 📈 Dashboard y Métricas
El panel principal muestra en tiempo real:
- Total de clientes atendidos.
- Vehículos registrados.
- Resumen de órdenes pendientes para organizar la jornada laboral.

## 📄 Normativa de Seguridad
- El acceso está protegido por contraseña. Cierre sesión al finalizar su turno.
- No modifique facturas ya emitidas sin autorización de administración.

---
**Talleres Sevilla Motor** - *Eficiencia y Profesionalidad en cada reparación.*
