import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ShoppingBag, Heart, ChefHat, Star, Clock, Users } from "lucide-react"

export default function HomePage() {
  return (
    <main className="min-h-screen bg-background">
      <section className="relative overflow-hidden bg-gradient-to-br from-amber-50 to-orange-50 dark:from-amber-950/20 dark:to-orange-950/20">
        <div className="container mx-auto px-4 py-12 sm:py-16 lg:py-20">
          <div className="text-center max-w-4xl mx-auto">
            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-foreground mb-4 sm:mb-6">
              Panadería Migas de Oro
            </h1>
            <p className="text-muted-foreground text-base sm:text-lg lg:text-xl max-w-2xl mx-auto mb-8">
              Descubre nuestros deliciosos productos artesanales, guarda tus favoritos y aprende a preparar increíbles
              recetas de panadería y repostería.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Button asChild size="lg" className="w-full sm:w-auto">
                <Link href="/productos">Ver Productos</Link>
              </Button>
              <Button asChild variant="outline" size="lg" className="w-full sm:w-auto bg-transparent">
                <Link href="/recetas">Explorar Recetas</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      <section className="container mx-auto px-4 py-12 sm:py-16">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
          <Card className="hover:shadow-lg transition-all duration-300 hover:scale-105">
            <CardHeader className="text-center pb-4">
              <div className="mx-auto mb-4 p-3 bg-amber-100 dark:bg-amber-900/20 rounded-full w-fit">
                <ShoppingBag className="h-8 w-8 text-amber-600" />
              </div>
              <CardTitle className="text-xl">Productos</CardTitle>
              <CardDescription className="text-sm sm:text-base">
                Explora nuestra amplia variedad de panes, pasteles y productos de repostería artesanal
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button asChild className="w-full">
                <Link href="/productos">Ver Productos</Link>
              </Button>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-all duration-300 hover:scale-105">
            <CardHeader className="text-center pb-4">
              <div className="mx-auto mb-4 p-3 bg-red-100 dark:bg-red-900/20 rounded-full w-fit">
                <Heart className="h-8 w-8 text-red-500" />
              </div>
              <CardTitle className="text-xl">Favoritos</CardTitle>
              <CardDescription className="text-sm sm:text-base">
                Guarda y organiza tus productos y recetas favoritas en un solo lugar
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button asChild variant="outline" className="w-full bg-transparent">
                <Link href="/favoritos">Mis Favoritos</Link>
              </Button>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-all duration-300 hover:scale-105 sm:col-span-2 lg:col-span-1">
            <CardHeader className="text-center pb-4">
              <div className="mx-auto mb-4 p-3 bg-green-100 dark:bg-green-900/20 rounded-full w-fit">
                <ChefHat className="h-8 w-8 text-green-600" />
              </div>
              <CardTitle className="text-xl">Recetas</CardTitle>
              <CardDescription className="text-sm sm:text-base">
                Aprende a preparar deliciosas recetas paso a paso con ingredientes y técnicas profesionales
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button asChild variant="outline" className="w-full bg-transparent">
                <Link href="/recetas">Ver Recetas</Link>
              </Button>
            </CardContent>
          </Card>
        </div>
      </section>

      <section className="bg-muted/50 py-12 sm:py-16">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-2xl sm:text-3xl font-bold text-foreground mb-4">¿Por qué elegir Migas de Oro?</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Más de 20 años de experiencia en panadería artesanal nos respaldan
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 max-w-4xl mx-auto">
            <div className="text-center">
              <div className="mx-auto mb-4 p-3 bg-blue-100 dark:bg-blue-900/20 rounded-full w-fit">
                <Star className="h-6 w-6 text-blue-600" />
              </div>
              <h3 className="font-semibold mb-2">Calidad Premium</h3>
              <p className="text-sm text-muted-foreground">
                Ingredientes frescos y de la más alta calidad en cada producto
              </p>
            </div>

            <div className="text-center">
              <div className="mx-auto mb-4 p-3 bg-purple-100 dark:bg-purple-900/20 rounded-full w-fit">
                <Clock className="h-6 w-6 text-purple-600" />
              </div>
              <h3 className="font-semibold mb-2">Horneado Diario</h3>
              <p className="text-sm text-muted-foreground">
                Productos frescos horneados cada día desde las primeras horas
              </p>
            </div>

            <div className="text-center sm:col-span-2 lg:col-span-1">
              <div className="mx-auto mb-4 p-3 bg-teal-100 dark:bg-teal-900/20 rounded-full w-fit">
                <Users className="h-6 w-6 text-teal-600" />
              </div>
              <h3 className="font-semibold mb-2">Tradición Familiar</h3>
              <p className="text-sm text-muted-foreground">
                Recetas tradicionales transmitidas de generación en generación
              </p>
            </div>
          </div>
        </div>
      </section>
    </main>
  )
}
