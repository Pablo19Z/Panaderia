import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Clock, Users, ChefHat } from "lucide-react"

const recetas = [
  {
    id: 1,
    nombre: "Muffins de Arándanos",
    descripcion: "Esponjosos muffins caseros con arándanos frescos",
    imagen: "/fresh-blueberry-muffins.png",
    tiempoPreparacion: "45 min",
    porciones: "12 muffins",
    dificultad: "Fácil",
    ingredientes: [
      "2 tazas de harina",
      "1/2 taza de azúcar",
      "2 cucharaditas de polvo de hornear",
      "1/2 cucharadita de sal",
      "1/3 taza de aceite",
      "1 huevo",
      "1 taza de leche",
      "1 taza de arándanos frescos",
    ],
    preparacion: [
      "Precalienta el horno a 200°C y engrasa moldes para muffins.",
      "Mezcla ingredientes secos en un bowl grande.",
      "En otro bowl, bate huevo, leche y aceite.",
      "Combina ingredientes húmedos con secos sin batir demasiado.",
      "Incorpora los arándanos con movimientos suaves.",
      "Llena moldes 2/3 y hornea 20-25 minutos hasta dorar.",
    ],
  },
  {
    id: 2,
    nombre: "Brownies de Chocolate",
    descripcion: "Ricos brownies húmedos con intenso sabor a chocolate",
    imagen: "/fudgy-chocolate-brownies.png",
    tiempoPreparacion: "1 hora",
    porciones: "16 porciones",
    dificultad: "Fácil",
    ingredientes: [
      "200g chocolate negro",
      "150g mantequilla",
      "200g azúcar",
      "3 huevos",
      "100g harina",
      "1/4 cucharadita de sal",
      "100g nueces (opcional)",
    ],
    preparacion: [
      "Precalienta horno a 180°C y forra molde cuadrado.",
      "Derrite chocolate y mantequilla a baño maría.",
      "Bate huevos con azúcar hasta que blanquee.",
      "Incorpora chocolate derretido a la mezcla de huevos.",
      "Añade harina y sal, mezcla hasta combinar.",
      "Vierte en molde y hornea 25-30 minutos.",
    ],
  },
  {
    id: 3,
    nombre: "Cookies de Avena",
    descripcion: "Clásicas galletas de avena crujientes por fuera y suaves por dentro",
    imagen: "/homemade-oatmeal-cookies.png",
    tiempoPreparacion: "30 min",
    porciones: "24 cookies",
    dificultad: "Fácil",
    ingredientes: [
      "1 taza de avena",
      "1 taza de harina",
      "1/2 taza de azúcar morena",
      "1/2 taza de mantequilla",
      "1 huevo",
      "1 cucharadita de vainilla",
      "1/2 cucharadita de bicarbonato",
      "1/2 cucharadita de canela",
    ],
    preparacion: [
      "Precalienta horno a 180°C.",
      "Bate mantequilla con azúcar hasta cremosa.",
      "Añade huevo y vainilla, mezcla bien.",
      "Incorpora ingredientes secos gradualmente.",
      "Forma bolitas y aplasta ligeramente en bandeja.",
      "Hornea 12-15 minutos hasta dorar bordes.",
    ],
  },
  {
    id: 4,
    nombre: "Pancakes Esponjosos",
    descripcion: "Pancakes americanos perfectos para el desayuno",
    imagen: "/fluffy-honey-pancakes.png",
    tiempoPreparacion: "20 min",
    porciones: "8 pancakes",
    dificultad: "Fácil",
    ingredientes: [
      "2 tazas de harina",
      "2 cucharadas de azúcar",
      "2 cucharaditas de polvo de hornear",
      "1 cucharadita de sal",
      "2 huevos",
      "1 3/4 tazas de leche",
      "1/4 taza de mantequilla derretida",
    ],
    preparacion: [
      "Mezcla ingredientes secos en un bowl.",
      "Bate huevos, leche y mantequilla en otro bowl.",
      "Combina mezclas sin batir demasiado.",
      "Calienta sartén a fuego medio.",
      "Vierte 1/4 taza de mezcla por pancake.",
      "Cocina hasta que aparezcan burbujas, voltea y cocina 2 min más.",
    ],
  },
  {
    id: 5,
    nombre: "Cupcakes de Vainilla",
    descripcion: "Suaves cupcakes de vainilla con frosting cremoso",
    imagen: "/vanilla-cupcakes-with-frosting.png",
    tiempoPreparacion: "1 hora",
    porciones: "12 cupcakes",
    dificultad: "Intermedio",
    ingredientes: [
      "1 1/2 tazas de harina",
      "1 taza de azúcar",
      "1/3 taza de mantequilla",
      "2 huevos",
      "2 cucharaditas de vainilla",
      "1 1/2 cucharaditas de polvo de hornear",
      "1/2 taza de leche",
    ],
    preparacion: [
      "Precalienta horno a 180°C y coloca capacillos.",
      "Bate mantequilla con azúcar hasta cremosa.",
      "Añade huevos uno a uno, luego vainilla.",
      "Alterna harina y leche en la mezcla.",
      "Llena capacillos 2/3 y hornea 18-20 minutos.",
      "Enfría completamente antes de decorar.",
    ],
  },
  {
    id: 6,
    nombre: "Pan de Banana",
    descripcion: "Húmedo pan dulce con bananas maduras",
    imagen: "/homemade-moist-banana-bread.png",
    tiempoPreparacion: "1 hora 15 min",
    porciones: "1 hogaza",
    dificultad: "Fácil",
    ingredientes: [
      "3 bananas maduras",
      "1/3 taza de mantequilla derretida",
      "3/4 taza de azúcar",
      "1 huevo batido",
      "1 cucharadita de vainilla",
      "1 cucharadita de bicarbonato",
      "1 1/3 tazas de harina",
    ],
    preparacion: [
      "Precalienta horno a 180°C y engrasa molde.",
      "Machaca bananas en bowl grande.",
      "Mezcla mantequilla derretida con bananas.",
      "Añade azúcar, huevo, vainilla y bicarbonato.",
      "Incorpora harina hasta apenas combinar.",
      "Hornea 60-65 minutos hasta que palillo salga limpio.",
    ],
  },
  {
    id: 7,
    nombre: "Donas Glaseadas",
    descripcion: "Donas esponjosas con glaseado dulce",
    imagen: "/homemade-glazed-donuts.png",
    tiempoPreparacion: "2 horas",
    porciones: "12 donas",
    dificultad: "Intermedio",
    ingredientes: [
      "2 tazas de harina",
      "3/4 taza de azúcar",
      "2 cucharaditas de polvo de hornear",
      "1 cucharadita de sal",
      "3/4 taza de leche",
      "2 huevos",
      "2 cucharadas de mantequilla derretida",
      "Aceite para freír",
    ],
    preparacion: [
      "Mezcla ingredientes secos en bowl grande.",
      "Bate leche, huevos y mantequilla en otro bowl.",
      "Combina mezclas y amasa suavemente.",
      "Extiende masa y corta donas con molde.",
      "Deja reposar 30 minutos.",
      "Fríe en aceite caliente 2-3 minutos por lado.",
    ],
  },
  {
    id: 8,
    nombre: "Waffles Belgas",
    descripcion: "Waffles crujientes por fuera y esponjosos por dentro",
    imagen: "/belgian-waffles-syrup.png",
    tiempoPreparacion: "25 min",
    porciones: "6 waffles",
    dificultad: "Fácil",
    ingredientes: [
      "2 tazas de harina",
      "1 cucharada de azúcar",
      "1 cucharada de polvo de hornear",
      "1/2 cucharadita de sal",
      "2 huevos separados",
      "1 3/4 tazas de leche",
      "1/2 taza de mantequilla derretida",
    ],
    preparacion: [
      "Mezcla ingredientes secos.",
      "Bate yemas con leche y mantequilla.",
      "Combina mezclas húmedas y secas.",
      "Bate claras a punto de nieve e incorpora.",
      "Cocina en waflera precalentada.",
      "Sirve inmediatamente con jarabe.",
    ],
  },
  {
    id: 9,
    nombre: "Cheesecake de Fresa",
    descripcion: "Cremoso cheesecake con salsa de fresas frescas",
    imagen: "/cheesecake-fresa-cremoso.png",
    tiempoPreparacion: "4 horas",
    porciones: "8 porciones",
    dificultad: "Intermedio",
    ingredientes: [
      "200g galletas graham",
      "100g mantequilla derretida",
      "600g queso crema",
      "200g azúcar",
      "3 huevos",
      "1 cucharadita de vainilla",
      "300g fresas frescas",
      "50g azúcar para salsa",
    ],
    preparacion: [
      "Mezcla galletas trituradas con mantequilla para base.",
      "Presiona en molde desmontable y refrigera.",
      "Bate queso crema hasta suave, añade azúcar.",
      "Incorpora huevos uno a uno, luego vainilla.",
      "Vierte sobre base y hornea a 160°C por 50 minutos.",
      "Enfría completamente y sirve con salsa de fresas.",
    ],
  },
]

export default function RecetasPage() {
  return (
    <main className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-foreground mb-2">Recetas Sencillas</h1>
          <p className="text-muted-foreground">Recetas fáciles y deliciosas para preparar en casa paso a paso</p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {recetas.map((receta) => (
            <Card key={receta.id} className="overflow-hidden hover:shadow-lg transition-shadow">
              <div className="aspect-video relative overflow-hidden">
                <img
                  src={receta.imagen || "/placeholder.svg"}
                  alt={receta.nombre}
                  className="w-full h-full object-cover"
                />
              </div>

              <CardHeader>
                <div className="flex items-start justify-between">
                  <CardTitle className="text-lg">{receta.nombre}</CardTitle>
                  <Badge
                    variant={
                      receta.dificultad === "Avanzado"
                        ? "destructive"
                        : receta.dificultad === "Intermedio"
                          ? "default"
                          : "secondary"
                    }
                  >
                    {receta.dificultad}
                  </Badge>
                </div>
                <CardDescription>{receta.descripcion}</CardDescription>
              </CardHeader>

              <CardContent className="space-y-4">
                <div className="flex items-center justify-between text-sm text-muted-foreground">
                  <div className="flex items-center gap-1">
                    <Clock className="h-4 w-4" />
                    {receta.tiempoPreparacion}
                  </div>
                  <div className="flex items-center gap-1">
                    <Users className="h-4 w-4" />
                    {receta.porciones}
                  </div>
                </div>

                <div>
                  <h4 className="font-semibold mb-2 flex items-center gap-2">
                    <ChefHat className="h-4 w-4" />
                    Ingredientes:
                  </h4>
                  <ul className="text-sm space-y-1">
                    {receta.ingredientes.slice(0, 3).map((ingrediente, index) => (
                      <li key={index} className="text-muted-foreground">
                        • {ingrediente}
                      </li>
                    ))}
                    {receta.ingredientes.length > 3 && (
                      <li className="text-muted-foreground">• Y {receta.ingredientes.length - 3} más...</li>
                    )}
                  </ul>
                </div>

                <div>
                  <h4 className="font-semibold mb-2">Preparación:</h4>
                  <ol className="text-sm space-y-1">
                    {receta.preparacion.slice(0, 2).map((paso, index) => (
                      <li key={index} className="text-muted-foreground">
                        {index + 1}. {paso}
                      </li>
                    ))}
                    {receta.preparacion.length > 2 && (
                      <li className="text-muted-foreground">... y {receta.preparacion.length - 2} pasos más</li>
                    )}
                  </ol>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </main>
  )
}
