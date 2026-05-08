# Sistema de Gestión de Reservas de Laboratorios

Este proyecto es una aplicación web desarrollada con **Django** para la gestión y control de reservas de laboratorios. Permite a los usuarios solicitar espacios, ver el estado de sus reservas y a los administradores gestionar dichas solicitudes.

## 🚀 Funcionalidades Principales

- **Gestión de Reservas:** Crear, editar, listar y eliminar reservas de laboratorios.
- **Autenticación:** Sistema de inicio de sesión y registro de usuarios.
- **Estadísticas:** Visualización de datos sobre el uso de los laboratorios.
- **Estados de Reserva:** Control de estados (Pendiente, Aprobada, Rechazada).

## 🛠️ Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

- `App/`: Aplicación principal que contiene los modelos, vistas y plantillas de la lógica de negocio.
- `reservasLaboratorio/`: Directorio de configuración del proyecto Django (settings, urls, wsgi).
- `manage.py`: Script principal para la administración del proyecto.
- `venv/`: Entorno virtual de Python (excluido en git).

## 📋 Requisitos Previos

Asegúrate de tener instalado:
- Python 3.8 o superior.
- Pip (gestor de paquetes de Python).

## 🔧 Configuración e Instalación

Sigue estos pasos para poner en marcha el proyecto en tu máquina local:

1. **Clonar el repositorio:**
   ```bash
   git clone <url-del-repositorio>
   cd Parcial-Electiva1
   ```

2. **Activar el entorno virtual:**
   Si no existe, créalo con: `python -m venv venv`.
   - **Windows:**
     ```bash
     .\venv\Scripts\activate
     ```
   - **Linux/macOS:**
     ```bash
     source venv/bin/activate
     ```

3. **Instalar dependencias:**
   ```bash
   pip install django
   ```

4. **Preparar la base de datos:**
   Asegúrate de que las migraciones estén aplicadas:
   ```bash
   python manage.py migrate
   ```

5. **Crear un superusuario (opcional):**
   Para acceder al panel de administración de Django:
   ```bash
   python manage.py createsuperuser
   ```

6. **Ejecutar el servidor:**
   ```bash
   python manage.py runserver
   ```
   La aplicación estará disponible en `http://127.0.0.1:8000/`.

---

## 🔀 Proceso de Fusión (Git Merge)

Para combinar los cambios de la rama `develop` a `main` manteniendo el historial de ambas:

1. Cambiar a la rama `main`:
   ```bash
   git checkout main
   ```
2. Fusionar `develop`:
   ```bash
   git merge develop
   ```
3. Resolver conflictos (si los hay) y realizar el commit:
   ```bash
   git add .
   git commit -m "Merge develop into main"
   ```
4. Subir los cambios al repositorio remoto:
   ```bash
   git push origin main
   ```

---
*Desarrollado como parte del curso Electiva 1.*
