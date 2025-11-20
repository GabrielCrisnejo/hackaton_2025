# Guía de Deployment

## Preparación de Datos

Los archivos de datos NO están incluidos en el repositorio por su tamaño. Necesitas subirlos manualmente al servidor de producción.

### Archivos necesarios:
- `backend/data/csv/IMDb_movies.csv`
- `backend/data/embeddings.npy`

## Opción 1: Deploy con Railway/Render

### 1. Sube tu código a GitHub
\`\`\`bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/tu-usuario/tu-repo.git
git push -u origin main
\`\`\`

### 2. Deploy el Backend en Railway

1. Ve a [railway.app](https://railway.app) y crea cuenta
2. New Project → Deploy from GitHub repo
3. Selecciona tu repositorio
4. Configura:
   - **Root Directory**: `backend`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`

5. Agrega las variables de entorno en Railway:
   - `AZURE_OPENAI_ENDPOINT`
   - `AZURE_OPENAI_API_KEY`
   - `AZURE_OPENAI_API_VERSION`
   - `AZURE_OPENAI_CHAT_MODEL`
   - `AZURE_OPENAI_EMBEDDING_MODEL`

6. **Sube los archivos de datos:**
   - Ve a tu proyecto en Railway
   - Settings → Volumes → Create Volume
   - Monta el volumen en `/app/data`
   - Usa Railway CLI para subir archivos:
     \`\`\`bash
     railway login
     railway link
     railway run bash
     # Dentro del contenedor, sube tus archivos con scp/sftp
     \`\`\`
   
   **Alternativa más simple**: Usa un servicio de almacenamiento:
   - Sube tus archivos a Google Drive, Dropbox o S3
   - Agrega un script en `backend/download_data.py` que descargue los datos al iniciar
   - Railway ejecutará este script automáticamente

### 3. Deploy el Frontend en Vercel

Desde v0:
1. Haz clic en el botón de GitHub (arriba derecha) para crear el repo
2. Haz clic en "Publish" para desplegar en Vercel
3. En Vercel Dashboard → Settings → Environment Variables:
   - Agrega: `BACKEND_URL` = URL de tu backend en Railway
4. Redeploy el proyecto

## Opción 2: Usar Almacenamiento en la Nube para Datos

Modifica `backend/app.py` para leer los datos desde S3/Azure Blob/Google Cloud Storage en lugar de archivos locales.

### Ejemplo con Azure Blob Storage:

\`\`\`python
from azure.storage.blob import BlobServiceClient
import pandas as pd
import numpy as np
from io import BytesIO

# Descargar CSV
blob_service = BlobServiceClient.from_connection_string(os.getenv("AZURE_STORAGE_CONNECTION_STRING"))
blob_client = blob_service.get_blob_client(container="data", blob="IMDb_movies.csv")
csv_data = blob_client.download_blob().readall()
movies_df = pd.read_csv(BytesIO(csv_data))

# Descargar embeddings
blob_client = blob_service.get_blob_client(container="data", blob="embeddings.npy")
npy_data = blob_client.download_blob().readall()
embeddings = np.load(BytesIO(npy_data))
\`\`\`

## Opción 3: VPS con Docker Compose

Si tienes un servidor (DigitalOcean, AWS EC2, etc.):

\`\`\`bash
# En tu servidor
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo

# Sube tus archivos de datos con scp
scp -r ./backend/data/ usuario@servidor:/ruta/tu-repo/backend/

# Crea .env y backend/.env con tus variables

# Ejecuta con Docker
docker-compose up -d
\`\`\`

## Recomendación

Para empezar rápido: **Railway + Vercel**
- Railway tiene una capa gratuita de 5 USD/mes en créditos
- Vercel es gratis para proyectos personales
- Sube los datos a Google Drive y agrégale al backend un script que los descargue al iniciar
