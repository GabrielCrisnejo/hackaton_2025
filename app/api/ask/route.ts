import { type NextRequest, NextResponse } from "next/server"

interface MovieData {
  title: string
  original_title: string
  year: string
  date_published: string
  genre: string
  duration: string
  country: string
  language: string
  director: string
  writer: string
  production_company: string
  actors: string
  description: string
  avg_vote: string
  votes: string
}

// Configuration
const AZURE_ENDPOINT = process.env.AZURE_OPENAI_ENDPOINT!
const AZURE_API_KEY = process.env.AZURE_OPENAI_API_KEY!
const AZURE_API_VERSION = process.env.AZURE_OPENAI_API_VERSION!
const CHAT_MODEL = process.env.AZURE_OPENAI_CHAT_MODEL!
const EMBED_MODEL = process.env.AZURE_OPENAI_EMBEDDING_MODEL!
const TOP_K = 5

// Cosine similarity function
function cosineSimilarity(a: number[], b: number[]): number {
  const dotProduct = a.reduce((sum, val, i) => sum + val * b[i], 0)
  const normA = Math.sqrt(a.reduce((sum, val) => sum + val * val, 0))
  const normB = Math.sqrt(b.reduce((sum, val) => sum + val * val, 0))
  return dotProduct / (normA * normB)
}

// Load data (in production, consider caching this)
let moviesData: MovieData[] | null = null
let embeddingsMatrix: number[][] | null = null

async function loadData() {
  if (moviesData && embeddingsMatrix) {
    return { moviesData, embeddingsMatrix }
  }

  try {
    const baseUrl = process.env.NEXT_PUBLIC_BASE_URL || "http://localhost:3000"

    // Load CSV data
    const csvResponse = await fetch(`${baseUrl}/data/csv/IMDb_movies.csv`)

    if (!csvResponse.ok) {
      throw new Error(
        `No se pudo cargar el archivo CSV. Asegúrate de que 'public/data/csv/IMDb_movies.csv' existe. Status: ${csvResponse.status}`,
      )
    }

    const csvText = await csvResponse.text()

    // Parse CSV
    const lines = csvText.split("\n")
    const headers = lines[0].split(",")

    moviesData = []
    for (let i = 1; i < lines.length; i++) {
      if (!lines[i].trim()) continue

      const values = lines[i].split(",")
      const movie: any = {}

      headers.forEach((header, index) => {
        movie[header.trim()] = values[index]?.trim() || ""
      })

      moviesData.push({
        title: movie.title || "Desconocido",
        original_title: movie.original_title || "Desconocido",
        year: movie.year || "Desconocido",
        date_published: movie.date_published || "Desconocido",
        genre: movie.genre || "Desconocido",
        duration: movie.duration || "Desconocido",
        country: movie.country || "Desconocido",
        language: movie.language || "Desconocido",
        director: movie.director || "Desconocido",
        writer: movie.writer || "Desconocido",
        production_company: movie.production_company || "Desconocido",
        actors: movie.actors || "Desconocido",
        description: movie.description || "Ninguna",
        avg_vote: movie.avg_vote || "Desconocido",
        votes: movie.votes || "Desconocido",
      })
    }

    const embeddingsResponse = await fetch(`${baseUrl}/data/embeddings.json`)

    if (!embeddingsResponse.ok) {
      throw new Error(
        `No se pudo cargar embeddings.json. Debes ejecutar el script 'python scripts/convert-embeddings.py' primero para convertir el archivo embeddings.npy a JSON. Status: ${embeddingsResponse.status}`,
      )
    }

    embeddingsMatrix = await embeddingsResponse.json()

    return { moviesData, embeddingsMatrix }
  } catch (error) {
    console.error("Error loading data:", error)
    throw error
  }
}

export async function POST(request: NextRequest) {
  try {
    const { question } = await request.json()

    if (!question || typeof question !== "string") {
      return NextResponse.json({ error: "Pregunta inválida" }, { status: 400 })
    }

    // Forward request to Python backend
    const backendUrl = process.env.BACKEND_URL || "http://localhost:8000"

    const response = await fetch(`${backendUrl}/ask`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question }),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: "Error del backend" }))
      throw new Error(errorData.error || "Error al comunicarse con el backend")
    }

    const data = await response.json()
    return NextResponse.json({ answer: data.answer })
  } catch (error) {
    console.error("Error processing question:", error)
    const errorMessage = error instanceof Error ? error.message : "Error al procesar la pregunta"
    return NextResponse.json({ error: errorMessage }, { status: 500 })
  }
}
