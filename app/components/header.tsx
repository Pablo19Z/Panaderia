"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { ShoppingBag, Heart, ChefHat, Menu, User, LogIn } from "lucide-react"
import { cn } from "@/lib/utils"
import { useIsMobile } from "@/components/ui/use-mobile"
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet"
import { Button } from "@/components/ui/button"

export function Header() {
  const pathname = usePathname()
  const isMobile = useIsMobile()

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

  const authItems = [
    {
      href: "/auth/login",
      label: "Iniciar Sesión",
      icon: LogIn,
    },
    {
      href: "/auth/register",
      label: "Registrarse",
      icon: User,
    },
  ]

  const MobileNav = () => (
    <Sheet>
      <SheetTrigger asChild>
        <Button variant="ghost" size="icon" className="md:hidden">
          <Menu className="h-5 w-5" />
          <span className="sr-only">Abrir menú</span>
        </Button>
      </SheetTrigger>
      <SheetContent side="left" className="w-[300px] sm:w-[400px]">
        <SheetHeader>
          <SheetTitle className="flex items-center gap-2">
            <ChefHat className="h-6 w-6 text-amber-600" />
            Migas de Oro
          </SheetTitle>
        </SheetHeader>
        <nav className="flex flex-col gap-4 mt-8">
          {navItems.map((item) => {
            const Icon = item.icon
            const isActive = pathname === item.href

            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors",
                  isActive
                    ? "bg-primary text-primary-foreground"
                    : "text-muted-foreground hover:text-foreground hover:bg-accent",
                )}
              >
                <Icon className="h-5 w-5" />
                <span>{item.label}</span>
              </Link>
            )
          })}
          <div className="border-t pt-4 mt-4">
            {authItems.map((item) => {
              const Icon = item.icon
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className="flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium text-muted-foreground hover:text-foreground hover:bg-accent transition-colors"
                >
                  <Icon className="h-5 w-5" />
                  <span>{item.label}</span>
                </Link>
              )
            })}
          </div>
        </nav>
      </SheetContent>
    </Sheet>
  )

  const DesktopNav = () => (
    <nav className="hidden md:flex items-center space-x-6">
      {navItems.map((item) => {
        const Icon = item.icon
        const isActive = pathname === item.href

        return (
          <Link
            key={item.href}
            href={item.href}
            className={cn(
              "flex items-center space-x-2 text-sm font-medium transition-colors hover:text-primary",
              isActive ? "text-primary" : "text-muted-foreground",
            )}
          >
            <Icon className="h-4 w-4" />
            <span>{item.label}</span>
          </Link>
        )
      })}
    </nav>
  )

  const AuthButtons = () => (
    <div className="hidden md:flex items-center space-x-2">
      {authItems.map((item) => {
        const Icon = item.icon
        return (
          <Button key={item.href} asChild variant={item.href === "/auth/login" ? "ghost" : "default"} size="sm">
            <Link href={item.href} className="flex items-center gap-2">
              <Icon className="h-4 w-4" />
              <span className="hidden lg:inline">{item.label}</span>
            </Link>
          </Button>
        )
      })}
    </div>
  )

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between px-4">
        <Link href="/" className="flex items-center space-x-2 flex-shrink-0">
          <ChefHat className="h-6 w-6 text-amber-600" />
          <span className="font-bold text-lg sm:text-xl">Migas de Oro</span>
        </Link>

        <DesktopNav />

        <div className="flex items-center gap-2">
          <AuthButtons />
          <MobileNav />
        </div>
      </div>
    </header>
  )
}
