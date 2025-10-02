import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ShoppingBag, Heart, ChefHat } from "lucide-react"

export default function HomePage() {
  return (
    <main className="min-h-screen bg-gray-900">
      <div className="container mx-auto px-4 py-8">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-amber-400 mb-4">Panadería Migas de Oro</h1>
          <p className="text-gray-300 text-lg max-w-2xl mx-auto">
            Descubre nuestros deliciosos productos artesanales, guarda tus favoritos y aprende a preparar increíbles
            recetas de panadería y repostería.
          </p>
        </div>

        {/* Navigation Cards */}
        <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
          <Card className="hover:shadow-lg transition-shadow bg-gray-800 border-gray-700">
            <CardHeader className="text-center">
              <ShoppingBag className="h-12 w-12 mx-auto text-amber-600 mb-2" />
              <CardTitle className="text-white">Productos</CardTitle>
              <CardDescription className="text-gray-300">
                Explora nuestra amplia variedad de panes, pasteles y productos de repostería
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button asChild className="w-full bg-amber-600 hover:bg-amber-700">
                <Link href="/productos">Ver Productos</Link>
              </Button>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow bg-gray-800 border-gray-700">
            <CardHeader className="text-center">
              <Heart className="h-12 w-12 mx-auto text-red-500 mb-2" />
              <CardTitle className="text-white">Favoritos</CardTitle>
              <CardDescription className="text-gray-300">
                Guarda y organiza tus productos y recetas favoritas en un solo lugar
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button
                asChild
                className="w-full bg-transparent border-amber-600 text-amber-400 hover:bg-amber-600 hover:text-white"
                variant="outline"
              >
                <Link href="/favoritos">Mis Favoritos</Link>
              </Button>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow bg-gray-800 border-gray-700">
            <CardHeader className="text-center">
              <ChefHat className="h-12 w-12 mx-auto text-green-600 mb-2" />
              <CardTitle className="text-white">Recetas</CardTitle>
              <CardDescription className="text-gray-300">
                Aprende a preparar deliciosas recetas paso a paso con ingredientes y técnicas
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button
                asChild
                className="w-full bg-transparent border-amber-600 text-amber-400 hover:bg-amber-600 hover:text-white"
                variant="outline"
              >
                <Link href="/recetas">Ver Recetas</Link>
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </main>
  )
}
