# Software para Talleres Mecánicos Independientes
## Proyecto SaaS para digitalización de talleres pequeños en Sevilla y alrededores

---

# 1. Visión del Proyecto

Desarrollar un software SaaS simple, específico y accesible para talleres mecánicos pequeños (1–5 empleados) que actualmente gestionan su negocio con:

- Papel
- Excel
- WhatsApp
- Memoria

Objetivo: Digitalizar su operativa diaria y ayudarles a ganar más dinero, organizarse mejor y fidelizar clientes.

Propuesta de valor:

> “El programa sencillo para talleres pequeños que quieren trabajar mejor y ganar más.”

---

# 2. Problema Detectado

En Sevilla y alrededores hay:

- Muchísimos talleres familiares
- Baja digitalización
- Procesos manuales
- Falta de métricas reales

Problemas frecuentes:

- Órdenes de trabajo desorganizadas
- Historial de vehículos perdido
- Presupuestos poco profesionales
- Pérdida de clientes
- No conocen su rentabilidad real
- No tienen base de datos estructurada

---

# 3. Funcionalidades del Producto

## 3.1 Gestión de Órdenes de Trabajo

- Crear orden en menos de 1 minuto
- Estados: pendiente / en proceso / terminado / entregado
- Asignación a mecánico
- Registro de piezas utilizadas
- Registro de horas de mano de obra
- Subida de fotos del vehículo
- Firma del cliente
- Conversión desde presupuesto

---

## 3.2 Historial Completo del Vehículo

Consulta por matrícula:

- Reparaciones anteriores
- Piezas cambiadas
- Fechas
- Kilometraje
- Garantías

Beneficio clave: fidelización del cliente.

---

## 3.3 Presupuestos Profesionales

- Generación automática en PDF
- Logo del taller
- Desglose claro de piezas y mano de obra
- Aceptación digital (WhatsApp o enlace)
- Conversión automática en orden de trabajo

---

## 3.4 Avisos Automáticos

- Recordatorio de ITV
- Cambio de aceite
- Revisión anual
- Coche listo para recoger
- Presupuesto pendiente de aceptación

Automatización sencilla pero muy valiosa.

---

## 3.5 Facturación

- Generación automática de facturas
- Control de cobros pendientes
- Exportación para gestoría
- Resumen mensual de ingresos

---

## 3.6 Métricas del Taller

Panel con:

- Facturación mensual
- Ticket medio
- Vehículos atendidos
- Clientes recurrentes
- Mecánico más productivo
- Servicios más rentables

Muchos talleres nunca han visto estos datos.

---

# 4. Diferenciación

La mayoría de softwares del sector:

- Son caros
- Están pensados para grandes talleres
- Son complejos
- Exceso de funcionalidades innecesarias

Nuestra ventaja:

- Ultra simple
- Adaptado al taller pequeño
- Precio accesible
- Soporte cercano

---

# 5. Modelo de Negocio

## SaaS mensual

- Plan básico: 29–39€/mes
- Plan completo: 49–59€/mes

Opcionales:
- Setup inicial: 99€
- Migración desde Excel
- Personalización con logo

Proyección ejemplo:

150 talleres x 49€/mes = 7.350€/mes  
= 88.200€/año

---

# 6. Estrategia de Entrada al Mercado

## Paso 1: Validación real

- Visitar talleres físicamente
- Analizar cómo trabajan
- Detectar frustraciones
- Ofrecer demo gratuita

## Paso 2: MVP

Solo incluir:

- Órdenes de trabajo
- Historial del vehículo
- Presupuestos
- Avisos básicos

## Paso 3: Venta directa local

- Demos presenciales
- Tablet o portátil
- 30 días gratis
- Soporte telefónico

En este nicho, la cercanía es clave.

---

# 7. Arquitectura Técnica Recomendada

## Stack Principal (Recomendado)

### Backend
- Django
- Django REST Framework
- PostgreSQL

### Frontend
Opción rápida:
- Django Templates
- Bootstrap
- HTMX

Opción más profesional:
- React + Django REST

### Hosting
- Render / Railway / Hetzner
- PostgreSQL gestionado
- Docker

---

# 8. Justificación Tecnológica

Django es ideal porque:

- Proyecto basado en CRUD
- Relaciones complejas
- Gestión de usuarios y permisos
- Panel administrativo automático
- ORM potente
- Rápido desarrollo para SaaS

FastAPI no aporta ventaja relevante en este tipo de sistema.

Spring Boot es viable pero más pesado para MVP.

---

# 9. Arquitectura de Módulos

- Usuarios
- Taller
- Clientes
- Vehículos
- Órdenes de trabajo
- Presupuestos
- Facturas
- Recordatorios
- Métricas

---

# 10. Modelo de Datos (Relaciones clave)

- Cliente → muchos Vehículos
- Vehículo → muchas Órdenes
- Orden → muchas Piezas
- Orden → muchas Horas de Trabajo
- Presupuesto → se convierte en Orden
- Orden → genera Factura

Base de datos recomendada: PostgreSQL.

---

# 11. Multi‑Tenant (Muy Importante)

Cada taller debe tener sus datos aislados.

Opción recomendada para inicio:

- Campo `taller_id` en todas las tablas
- Filtros automáticos por usuario autenticado

Más simple que base de datos separada por cliente.

---

# 12. PDFs

Opciones:

- WeasyPrint
- ReportLab
- Renderizado HTML + CSS a PDF

Para presupuestos y facturas.

---

# 13. WhatsApp Automático

Opciones:

- API oficial WhatsApp Business
- Twilio
- Enlace preformateado simple (ideal para MVP)

---

# 14. Roadmap Estimado

- MVP funcional: 6–8 semanas
- Producto vendible: 3 meses
- Expansión de funcionalidades: continuo

---

# 15. Riesgos

- Baja digitalización
- Resistencia al cambio
- Márgenes pequeños para pagar software

Mitigación:

- Producto extremadamente fácil
- Precio accesible
- Acompañamiento cercano

---

# 16. Evolución Futura

- Integración con proveedores de piezas
- App para cliente final
- CRM avanzado
- Integración con aseguradoras
- Expansión a Andalucía
- Escalado nacional

---

# Conclusión

No es un proyecto “startup sexy”.
No es viral.
No es Silicon Valley.

Pero es:

- Recurrente
- Estable
- Poco competido a nivel local
- Altamente rentable si se ejecuta bien

Proyecto con fuerte encaje en mercado local y potencial de expansión nacional.