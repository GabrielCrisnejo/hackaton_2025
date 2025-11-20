"""
Script opcional para descargar datos desde una URL al iniciar el servidor.
Útil para Railway/Render donde no puedes subir archivos grandes directamente.

Uso:
1. Sube tus archivos de datos a Google Drive, Dropbox o similar
2. Obtén un link de descarga directo
3. Configura las variables de entorno:
   - MOVIES_CSV_URL
   - EMBEDDINGS_NPY_URL
4. Este script se ejecutará automáticamente al iniciar
"""

import os
import requests
from pathlib import Path

def download_file(url: str, destination: str):
    """Descarga un archivo desde una URL"""
    print(f"Descargando {destination}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    Path(destination).parent.mkdir(parents=True, exist_ok=True)
    
    with open(destination, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print(f"✓ {destination} descargado")

def setup_data():
    """Descarga los archivos de datos si no existen"""
    data_dir = Path("data")
    csv_path = data_dir / "csv" / "IMDb_movies.csv"
    embeddings_path = data_dir / "embeddings.npy"
    
    # Si los archivos ya existen, no hacer nada
    if csv_path.exists() and embeddings_path.exists():
        print("✓ Archivos de datos ya existen")
        return
    
    # Obtener URLs desde variables de entorno
    csv_url = os.getenv("MOVIES_CSV_URL")
    embeddings_url = os.getenv("EMBEDDINGS_NPY_URL")
    
    if not csv_url or not embeddings_url:
        print("⚠ MOVIES_CSV_URL y EMBEDDINGS_NPY_URL no configuradas")
        print("  Los datos deben estar en backend/data/")
        return
    
    # Descargar archivos
    try:
        if not csv_path.exists():
            download_file(csv_url, str(csv_path))
        
        if not embeddings_path.exists():
            download_file(embeddings_url, str(embeddings_path))
        
        print("✓ Datos configurados correctamente")
    except Exception as e:
        print(f"✗ Error descargando datos: {e}")
        raise

if __name__ == "__main__":
    setup_data()
