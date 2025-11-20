# IMDB AI Assistant - Next.js + Python Backend

Aplicación de búsqueda inteligente de películas usando Azure OpenAI, Next.js y Python (FastAPI).

## 🚀 Características

- Búsqueda semántica de películas usando embeddings
- Respuestas generadas por Azure OpenAI
- Interfaz moderna y responsive con Next.js 16
- Backend en Python con FastAPI para manejar archivos .npy directamente
- Base de datos de películas de IMDB

## 📋 Requisitos Previos

1. **Azure OpenAI**: Necesitas una cuenta de Azure con acceso a OpenAI
2. **Node.js**: Versión 18 o superior
3. **Python**: Versión 3.9 o superior
4. **Datos**: 
   - Archivo CSV de películas: `IMDb_movies.csv`
   - Archivo de embeddings: `embeddings.npy`

## 🛠️ Instalación

### Paso 1: Preparar tus archivos de datos

**IMPORTANTE**: Copia tu carpeta `data` completa a la carpeta `backend/`:

\`\`\`bash
# Desde la raíz de tu proyecto
cp -r ./data ./backend/data
\`\`\`

Tu estructura debe quedar así:
\`\`\`
proyecto/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── data/                    # <-- Tu carpeta data aquí
│       ├── csv/
│       │   └── IMDb_movies.csv
│       └── embeddings.npy
├── app/
└── ...
\`\`\`

### Paso 2: Configurar el Backend de Python

\`\`\`bash
# Navega a la carpeta backend
cd backend

# Crea un entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instala las dependencias
pip install -r requirements.txt

# Copia y configura las variables de entorno
cp .env.example .env
\`\`\`

Edita `backend/.env` con tus credenciales de Azure OpenAI:

\`\`\`env
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com
AZURE_OPENAI_API_KEY=tu-api-key-aqui
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_CHAT_MODEL=nombre-deployment-chat
AZURE_OPENAI_EMBEDDING_MODEL=nombre-deployment-embeddings
\`\`\`

### Paso 3: Configurar el Frontend de Next.js

\`\`\`bash
# Vuelve a la raíz del proyecto
cd ..

# Instala las dependencias
npm install

# Copia y configura las variables de entorno
cp .env.example .env.local
\`\`\`

Edita `.env.local`:

\`\`\`env
BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_BASE_URL=http://localhost:3000
\`\`\`

### Paso 4: Ejecutar la aplicación

**Opción A: Ejecutar manualmente (2 terminales)**

Terminal 1 - Backend:
\`\`\`bash
cd backend
python app.py
# o
uvicorn app:app --reload
\`\`\`

Terminal 2 - Frontend:
\`\`\`bash
npm run dev
\`\`\`

**Opción B: Usar Docker Compose (recomendado)**

\`\`\`bash
docker-compose up
\`\`\`

Abre [http://localhost:3000](http://localhost:3000) en tu navegador.

## 📁 Estructura del Proyecto

\`\`\`
├── app/
│   ├── page.tsx              # Página principal
│   ├── layout.tsx            # Layout principal
│   ├── globals.css           # Estilos globales
│   └── api/
│       └── ask/
│           └── route.ts      # API proxy al backend de Python
├── backend/
│   ├── app.py                # Backend FastAPI
│   ├── requirements.txt      # Dependencias de Python
│   ├── .env.example          # Variables de entorno del backend
│   └── data/
│       ├── csv/
│       │   └── IMDb_movies.csv
│       └── embeddings.npy
├── components/
│   └── ui/                   # Componentes de shadcn/ui
└── docker-compose.yml        # Configuración de Docker
\`\`\`

## 🎯 Uso

1. Escribe tu pregunta sobre películas en el campo de búsqueda
2. Haz clic en "Buscar Respuesta"
3. La IA encontrará las películas más relevantes y generará una respuesta

### Ejemplos de preguntas:

- "Detalles de Saving Private Ryan"
- "¿Cuál es el género de la película Inception?"
- "¿Quién fue el director de The Dark Knight?"
- "Dame información sobre películas de Christopher Nolan"

## 🐛 Solución de Problemas

### Error: "Error al comunicarse con el backend"

Asegúrate de que el backend de Python esté ejecutándose:
\`\`\`bash
cd backend
python app.py
\`\`\`

Verifica que esté corriendo en `http://localhost:8000` y visita esa URL para ver el mensaje "IMDB AI Backend is running".

### Error al cargar los embeddings

Verifica que los archivos estén en la ubicación correcta:
- `backend/data/csv/IMDb_movies.csv`
- `backend/data/embeddings.npy`

### Error: "peer dependencies" al instalar npm

Ejecuta:
\`\`\`bash
npm install --legacy-peer-deps
\`\`\`

## 🔧 Ventajas de esta arquitectura

- **Sin conversión necesaria**: Mantiene los archivos .npy en su formato original
- **Mejor performance**: NumPy es más eficiente que JSON para operaciones vectoriales
- **Separación de responsabilidades**: Frontend en Next.js, procesamiento pesado en Python
- **Escalable**: El backend puede ser deployado independientemente

## 🚀 Deploy

**IMPORTANTE**: Los archivos de datos (CSV y embeddings.npy) son muy pesados para GitHub. Se excluyen automáticamente mediante `.gitignore`.

### Opción 1: Vercel + Railway (Recomendado)

#### Deploy del Frontend en Vercel

1. **Desde v0**:
   - Haz clic en el botón de GitHub (arriba derecha) para crear el repositorio
   - Haz clic en "Publish" para desplegar automáticamente en Vercel

2. **Configurar variables de entorno en Vercel**:
   - Ve a tu proyecto en Vercel Dashboard
   - Settings → Environment Variables
   - Agrega: `BACKEND_URL` = URL de tu backend (la obtendrás después de deployar en Railway)

#### Deploy del Backend en Railway

1. **Sube tu código a GitHub**:
   \`\`\`bash
   git add .
   git commit -m "Initial commit"
   git push
   \`\`\`

2. **Deploy en Railway**:
   - Ve a [railway.app](https://railway.app) y crea cuenta
   - New Project → Deploy from GitHub repo
   - Selecciona tu repositorio
   - Root Directory: `backend`

3. **Configurar variables de entorno en Railway**:
   - `AZURE_OPENAI_ENDPOINT`
   - `AZURE_OPENAI_API_KEY`
   - `AZURE_OPENAI_API_VERSION`
   - `AZURE_OPENAI_CHAT_MODEL`
   - `AZURE_OPENAI_EMBEDDING_MODEL`

4. **Subir archivos de datos** (elige una opción):

   **Opción A - URLs de descarga (Más fácil)**:
   - Sube tus archivos a Google Drive, Dropbox o similar
   - Obtén URLs de descarga directa
   - Agrega estas variables en Railway:
     - `MOVIES_CSV_URL=https://url-directa-a-tu-csv`
     - `EMBEDDINGS_NPY_URL=https://url-directa-a-tu-npy`
   - El backend descargará automáticamente los datos al iniciar

   **Opción B - Railway Volumes**:
   - Settings → Volumes → Create Volume
   - Monta en `/app/data`
   - Usa Railway CLI para subir archivos

5. **Obtén la URL del backend**:
   - Railway te dará una URL como `https://tu-proyecto.railway.app`
   - Cópiala y agrégala como `BACKEND_URL` en Vercel

6. **Redeploy el frontend** en Vercel para aplicar la nueva variable

### Opción 2: Render

Similar a Railway:
- Frontend en Vercel (desde v0)
- Backend en Render con Python
- Start Command: `./start.sh`
- Usar Render Disks para archivos de datos

### Opción 3: VPS con Docker

Si tienes un servidor propio:

\`\`\`bash
# En tu servidor
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo

# Sube tus archivos de datos con scp
scp -r ./backend/data/ usuario@servidor:/ruta/tu-repo/backend/

# Crea backend/.env con tus variables de Azure

# Ejecuta
docker-compose up -d
\`\`\`

Accede a:
- Frontend: http://tu-servidor-ip:3000
- Backend: http://tu-servidor-ip:8000

### Costos estimados

- **Vercel**: Gratis para proyectos personales
- **Railway**: 5 USD/mes en créditos gratis, luego pay-as-you-go
- **Render**: Plan gratuito disponible (con límites)

**Ver [DEPLOYMENT.md](./DEPLOYMENT.md) para instrucciones detalladas paso a paso.**

## 📄 Licencia

MIT
