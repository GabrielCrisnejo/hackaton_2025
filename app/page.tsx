"use client"

import type React from "react"

import { useState } from "react"
import { Search, Film, Sparkles, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"

export default function HomePage() {
  const [question, setQuestion] = useState("")
  const [answer, setAnswer] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState("")

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!question.trim()) {
      setError("Por favor, ingresa una pregunta")
      return
    }

    setIsLoading(true)
    setError("")
    setAnswer("")

    try {
      const response = await fetch("/api/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || "Error al procesar la pregunta")
      }

      setAnswer(data.answer)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error desconocido")
    } finally {
      setIsLoading(false)
    }
  }

  const exampleQuestions = [
    "Detalles de Saving Private Ryan",
    "¿Cuál es el género de la película Inception?",
    "¿Quién fue el director de The Dark Knight?",
    "¿Qué año se publicó Titanic?",
    "Dame información sobre películas de Christopher Nolan",
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5">
      {/* Background effects */}
      <div className="fixed inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-primary/10 via-background to-background pointer-events-none" />

      <div className="relative">
        {/* Header */}
        <header className="border-b border-border/40 backdrop-blur-sm bg-background/50">
          <div className="container mx-auto px-4 py-6">
            <div className="flex items-center justify-center gap-3">
              <Film className="h-8 w-8 text-primary" />
              <h1 className="text-3xl font-bold bg-gradient-to-r from-foreground to-foreground/70 bg-clip-text text-transparent">
                IMDB AI Assistant
              </h1>
            </div>
          </div>
        </header>

        {/* Main content */}
        <main className="container mx-auto px-4 py-12">
          <div className="max-w-4xl mx-auto space-y-8">
            {/* Hero section */}
            <div className="text-center space-y-4">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20">
                <Sparkles className="h-4 w-4 text-primary" />
                <span className="text-sm font-medium text-primary">Powered by Azure OpenAI</span>
              </div>
              <h2 className="text-4xl md:text-5xl font-bold text-balance">Pregúntame sobre cualquier película</h2>
              <p className="text-lg text-muted-foreground text-balance">
                Usa IA para explorar nuestra base de datos de películas de IMDB
              </p>
            </div>

            {/* Search form */}
            <Card className="p-6 shadow-xl border-border/50 bg-card/50 backdrop-blur-sm">
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="relative">
                  <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
                  <Input
                    type="text"
                    placeholder="Ej: Detalles de Saving Private Ryan"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    className="pl-12 h-14 text-lg bg-background border-border/50 focus-visible:ring-primary"
                    disabled={isLoading}
                  />
                </div>
                <Button
                  type="submit"
                  size="lg"
                  className="w-full h-12 text-base font-semibold bg-gradient-to-r from-primary to-primary/80 hover:from-primary/90 hover:to-primary/70"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                      Buscando...
                    </>
                  ) : (
                    <>
                      <Search className="mr-2 h-5 w-5" />
                      Buscar Respuesta
                    </>
                  )}
                </Button>
              </form>

              {error && (
                <div className="mt-4 p-4 rounded-lg bg-destructive/10 border border-destructive/20">
                  <p className="text-destructive text-sm">{error}</p>
                </div>
              )}
            </Card>

            {/* Answer display */}
            {answer && (
              <Card className="p-6 shadow-xl border-primary/20 bg-gradient-to-br from-card/80 to-primary/5 backdrop-blur-sm animate-in fade-in-0 slide-in-from-bottom-4 duration-500">
                <div className="space-y-3">
                  <div className="flex items-center gap-2 text-primary font-semibold">
                    <Sparkles className="h-5 w-5" />
                    <h3 className="text-lg">Respuesta</h3>
                  </div>
                  <div className="prose prose-sm max-w-none dark:prose-invert">
                    <p className="text-foreground/90 leading-relaxed whitespace-pre-wrap">{answer}</p>
                  </div>
                </div>
              </Card>
            )}

            {/* Example questions */}
            {!answer && !isLoading && (
              <div className="space-y-4">
                <h3 className="text-center text-sm font-medium text-muted-foreground">Preguntas de ejemplo</h3>
                <div className="grid gap-2 md:grid-cols-2">
                  {exampleQuestions.map((example, index) => (
                    <button
                      key={index}
                      onClick={() => setQuestion(example)}
                      className="text-left p-3 rounded-lg border border-border/50 hover:border-primary/50 hover:bg-primary/5 transition-colors text-sm text-muted-foreground hover:text-foreground"
                    >
                      {example}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        </main>

        {/* Footer */}
        <footer className="border-t border-border/40 mt-16">
          <div className="container mx-auto px-4 py-6 text-center text-sm text-muted-foreground">
            Powered by Next.js & Azure OpenAI
          </div>
        </footer>
      </div>
    </div>
  )
}
