# IMDB AI Assistant - Streamlit Frontend

Aplicación web interactiva para consultar información de películas usando embeddings y Azure OpenAI.

## 🚀 Características

- Interfaz moderna con gradiente azul-magenta futurista
- Búsqueda semántica usando embeddings vectoriales
- Respuestas generadas por LLM basadas en contexto
- Integración con PostgreSQL + pgvector
- Diseño responsive y animaciones suaves

## 📋 Requisitos Previos

1. Base de datos PostgreSQL con extensión pgvector
2. Embeddings generados (archivo `embeddings.npy`)
3. Variables de entorno configuradas en `.env`

## ⚙️ Configuración

### 1. Variables de Entorno

Crea un archivo `.env` con:

\`\`\`env
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=tu_endpoint
AZURE_OPENAI_API_KEY=tu_api_key
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_CHAT_MODEL=gpt-4
AZURE_OPENAI_EMBEDDING_MODEL=text-embedding-ada-002

# PostgreSQL
PG_HOST=localhost
PG_DATABASE=imdb
PG_USER=gabriel
PG_PASSWORD=password123
PG_PORT=5432
\`\`\`

### 2. Instalación

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 3. Generar Embeddings (si aún no lo hiciste)

\`\`\`bash
python ingest_data2-uIFEw.py
\`\`\`

Esto creará:
- Tabla `movies_embeddings` en PostgreSQL
- Archivo `data/embeddings.npy` con los vectores

## 🎬 Uso

### Iniciar la aplicación

\`\`\`bash
streamlit run app.py
\`\`\`

La aplicación se abrirá en tu navegador en `http://localhost:8501`

### Hacer Preguntas

1. Escribe tu pregunta en el campo de texto
2. Haz clic en "🔍 Buscar Respuesta"
3. Espera la respuesta del asistente AI

## 🎨 Personalización

El diseño está inspirado en el estilo futurista con:
- Fondo oscuro con gradiente
- Efecto de malla wireframe azul-magenta
- Bordes y sombras con glow effects
- Animaciones suaves en interacciones

Puedes modificar los colores editando el CSS en `app.py`.

## 📦 Estructura del Proyecto

\`\`\`
.
├── app.py                      # Aplicación Streamlit principal
├── ingest_data2-uIFEw.py      # Script para generar embeddings
├── ask_questions-8fo11.py     # Script CLI para pruebas
├── requirements.txt            # Dependencias Python
├── docker-compose-SDMwT.yml   # Configuración PostgreSQL
└── data/
    ├── csv/IMDb_movies.csv    # Datos de películas
    └── embeddings.npy         # Vectores de embeddings
\`\`\`

## 🐛 Troubleshooting

**Error de conexión a PostgreSQL:**
- Verifica que Docker esté corriendo: `docker-compose up -d`
- Confirma las credenciales en `.env`

**Error de Azure OpenAI:**
- Verifica tu API key y endpoint
- Confirma que los modelos estén desplegados

**No se encuentran películas:**
- Ejecuta `ingest_data2-uIFEw.py` para cargar datos
- Verifica que la tabla `movies_embeddings` exista

## 📄 Licencia

MIT
