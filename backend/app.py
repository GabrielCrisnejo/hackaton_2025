from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import numpy as np
import csv
from dotenv import load_dotenv
from openai import AzureOpenAI
from download_data import setup_data

load_dotenv()

setup_data()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Next.js domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
CHAT_MODEL = os.getenv("AZURE_OPENAI_CHAT_MODEL")
EMBED_MODEL = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL")

CSV_PATH = "data/csv/IMDb_movies.csv"
EMBEDDINGS_PATH = "data/embeddings.npy"
TOP_K = 5

# Initialize OpenAI client
client = AzureOpenAI(
    api_key=AZURE_API_KEY,
    api_version=AZURE_API_VERSION,
    azure_endpoint=AZURE_ENDPOINT,
)

print("Loading embeddings from file...")
embeddings_matrix = np.load(EMBEDDINGS_PATH)
print(f"Loaded {len(embeddings_matrix)} embeddings")

print("Loading movie data from CSV...")
movies_data = []
with open(CSV_PATH, "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        movies_data.append({
            "title": row["title"],
            "original_title": row["original_title"],
            "year": row["year"] if row["year"] else "Desconocido",
            "date_published": row["date_published"] if row["date_published"] else "Desconocido",
            "genre": row["genre"],
            "duration": row["duration"] if row["duration"] else "Desconocido",
            "country": row["country"],
            "language": row["language"],
            "director": row["director"],
            "writer": row["writer"],
            "production_company": row["production_company"],
            "actors": row["actors"],
            "description": row["description"],
            "avg_vote": row["avg_vote"] if row["avg_vote"] else "Desconocido",
            "votes": row["votes"] if row["votes"] else "Desconocido",
        })
print(f"Loaded {len(movies_data)} movies")


def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str


@app.get("/")
async def root():
    return {"message": "IMDB AI Backend is running"}


@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """
    Main endpoint to ask questions to the LLM based on embeddings
    Returns the answer from the LLM
    """
    try:
        question = request.question
        
        # Generate embedding for the question
        emb = client.embeddings.create(
            model=EMBED_MODEL,
            input=question
        ).data[0].embedding
        
        query_embedding = np.array(emb)
        
        similarities = []
        for i, movie_emb in enumerate(embeddings_matrix):
            sim = cosine_similarity(query_embedding, movie_emb)
            similarities.append((i, sim))
        
        # Sort by similarity (highest first) and get top K
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_indices = [idx for idx, _ in similarities[:TOP_K]]
        
        if not top_indices:
            return AnswerResponse(answer="No se encontraron documentos similares.")

        context_parts = []
        for idx in top_indices:
            movie = movies_data[idx]
            
            doc_text = (
                f"Título: {movie['title'] or 'Desconocido'}. "
                f"Título original: {movie['original_title'] or 'Desconocido'}. "
                f"Año de publicación: {movie['year']}. "
                f"Fecha publicada: {movie['date_published']}. "
                f"Género: {movie['genre'] or 'Desconocido'}. "
                f"Duración: {movie['duration']} minutos. "
                f"País: {movie['country'] or 'Desconocido'}. "
                f"Idioma: {movie['language'] or 'Desconocido'}. "
                f"Director: {movie['director'] or 'Desconocido'}. "
                f"Guionista: {movie['writer'] or 'Desconocido'}. "
                f"Productora: {movie['production_company'] or 'Desconocido'}. "
                f"Actores principales: {movie['actors'] or 'Desconocido'}. "
                f"Descripción: {movie['description'] or 'Ninguna'}. "
                f"Voto promedio: {movie['avg_vote']}. "
                f"Cantidad de votos: {movie['votes']}."
            )
            context_parts.append(doc_text)

        context = "\n\n".join(context_parts)

        # Ask LLM with context
        response = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres un asistente de IMDB. Responde únicamente usando el "
                        "CONTEXTO proporcionado. Si la información no está allí, "
                        "responde: 'No puedo responder con la información disponible.'"
                    )
                },
                {
                    "role": "user",
                    "content": f"Contexto:\n{context}\n\nPregunta: {question}"
                }
            ]
        )

        answer = response.choices[0].message.content
        return AnswerResponse(answer=answer)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
