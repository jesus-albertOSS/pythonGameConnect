# 🎮 Game Connect – Análisis y Visualización de Datos

**Autor:** Jesus Alberto Osuna Guillen  
**Versión:** 1.0  
**Fecha:** Octubre 2025  

---

## 🧩 Descripción del Proyecto

Este proyecto forma parte del **Momento 3** del curso.  
Su objetivo es analizar los datos de usuarios y productos obtenidos desde una API de la plataforma **Game Connect**, aplicando **limpieza, validación y visualización de datos**.

A partir de los datos procesados, se generan **gráficos** y un **reporte HTML interactivo**, integrando estadísticas, visualizaciones y tablas dinámicas.

---

## 🚀 Funcionalidades Principales

✅ Obtención de datos desde la **API del backend (Render)**.  
✅ Limpieza, normalización y validación de datos con **Pandas** y **Pandera**.  
✅ Visualización con **Matplotlib** y **Seaborn**.  
✅ Generación automática de un **reporte HTML interactivo**.  
✅ Servidor **FastAPI** para visualizar el reporte desde el navegador.  
✅ Integración de **DataTables.js** para tablas con búsqueda, ordenamiento y paginación.

---

## 🧠 Módulo de Visualización (`visualizacion.py`)

El módulo `visualizacion.py` contiene las funciones que generan las visualizaciones analíticas del proyecto.

### 📊 Funciones Principales

- **`top_users_by_points(df)`**  
  Genera un gráfico de barras que muestra los **Top 5 usuarios con más puntos** en la plataforma.

- **`price_distribution(df)`**  
  Crea un histograma que representa la **distribución de precios** de los productos disponibles.

Ambos gráficos incluyen títulos, etiquetas y estilos personalizables para facilitar su interpretación visual.

---

## 📄 Generador de Reporte HTML

El archivo `utils/report_generator.py` ensambla los resultados en un **reporte visual completo** que incluye:

- Un **título principal** con el nombre del proyecto.  
- **Tarjetas con métricas generales**, como total de usuarios, total de productos, precio promedio y usuario con más puntos.  
- Los gráficos generados por el módulo `visualizacion.py`.  
- **Tablas de datos** exportadas desde los DataFrames procesados.  
- Estilos modernos con **Bootstrap 5** y soporte para **DataTables.js**.

📁 El reporte se genera automáticamente en:  
`reports/reporte.html`

---

## 📈 Resultados y Análisis Visual

### 🔹 Gráficos Incluidos

1. **Top 5 Usuarios con Más Puntos:**  
   Muestra los usuarios más activos o con mayor fidelidad.

2. **Distribución de Precios de Productos:**  
   Permite identificar rangos de precios y detectar valores atípicos.

### 🔹 Tabla Interactiva
Incluye todos los productos y usuarios, con búsqueda, ordenamiento y paginación integrados.

### 🔹 Hallazgos Principales

- Los usuarios con mayor puntaje reflejan **alta participación** en la plataforma.  
- Los precios de los productos se concentran en rangos **medios**, con pocos valores extremos.  
- El proceso de limpieza eliminó **duplicados** y corrigió **inconsistencias de formato**.  
- El reporte HTML facilita la **interpretación técnica y visual** de los datos.

---

## 🧰 Tecnologías Utilizadas.

| Tecnología | Uso Principal |
|-------------|----------------|
| **Python 3.11** | Lenguaje base del proyecto |
| **FastAPI** | Servidor web para exponer el reporte |
| **Pandas & Pandera** | Limpieza y validación de datos |
| **Matplotlib / Seaborn** | Visualización de datos |
| **Bootstrap 5 + DataTables.js** | Estilo e interactividad del HTML |
| **Render** | Despliegue del servidor backend |
| **Supabase** | Base de datos principal |

---

## ⚙️ Instrucciones de Ejecución

### 1️⃣ Clonar el Repositorio
```bash
git clone https://github.com/jesus-albertOSS/pythonGameConnect
cd pythonGameConnect
