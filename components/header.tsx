"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { ShoppingBag, Heart, ChefHat, User, LogOut } from "lucide-react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

export function Header() {
  const pathname = usePathname()

  const userName = "jhony" // Nombre del usuario actual

  const navItems = [
    {
      href: "/",
      label: "Inicio",
      icon: ChefHat,
    },
    {
      href: "/productos",
      label: "Productos",
      icon: ShoppingBag,
    },
    {
      href: "/favoritos",
      label: "Favoritos",
      icon: Heart,
    },
    {
      href: "/recetas",
      label: "Recetas",
      icon: ChefHat,
    },
  ]

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-gray-900 backdrop-blur">
      <div className="container flex h-16 items-center justify-between">
        <Link href="/" className="flex items-center space-x-2">
          <ChefHat className="h-6 w-6 text-amber-500" />
          <span className="font-bold text-xl text-white" style={{ fontFamily: "cursive" }}>
            🍞 Migas de oro Dorè
          </span>
        </Link>

        <nav className="flex items-center space-x-6">
          {navItems.map((item) => {
            const Icon = item.icon
            const isActive = pathname === item.href

            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex items-center space-x-2 text-sm font-medium transition-colors hover:text-amber-400",
                  isActive ? "text-amber-400" : "text-gray-300",
                )}
              >
                <Icon className="h-4 w-4" />
                <span>{item.label}</span>
              </Link>
            )
          })}

          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm" className="text-gray-300 hover:text-white hover:bg-gray-700">
                <User className="h-4 w-4 mr-2" />
                {userName}
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent className="bg-gray-800 border-gray-700" align="end">
              <DropdownMenuItem asChild>
                <Link href="/perfil" className="text-gray-300 hover:text-white cursor-pointer">
                  <User className="h-4 w-4 mr-2" />
                  Mi Perfil
                </Link>
              </DropdownMenuItem>
              <DropdownMenuSeparator className="bg-gray-700" />
              <DropdownMenuItem className="text-gray-300 hover:text-white cursor-pointer">
                <LogOut className="h-4 w-4 mr-2" />
                Cerrar Sesión
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>

          <Link
            href="/carrito"
            className="flex items-center space-x-2 text-sm font-medium transition-colors hover:text-amber-400 text-gray-300"
          >
            <ShoppingBag className="h-4 w-4" />
            <span>Carrito</span>
            <span className="bg-blue-600 text-white text-xs rounded-full px-2 py-1 ml-1">0</span>
          </Link>
        </nav>
      </div>
    </header>
  )
}
