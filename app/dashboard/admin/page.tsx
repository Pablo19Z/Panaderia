"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import {
  Shield,
  Users,
  UserMinus as UserFriends,
  Package,
  ClipboardList,
  BarChart3,
  Settings,
  Crown,
  Clock,
  TrendingUp,
  ArrowUp,
  Box,
  ShoppingCart,
  DollarSign,
  UserPlus,
  PlusCircle,
  AlertTriangle,
  Server,
  ChefHat,
  CaseLower as CashRegister,
  Utensils,
  Download,
  Filter,
  Save,
  Terminal,
  Activity,
} from "lucide-react"

export default function AdminDashboard() {
  const [activeTab, setActiveTab] = useState("dashboard")
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [filtroPersonal, setFiltroPersonal] = useState("todos")

  // Datos de ejemplo - en una app real vendrían de una API
  const usuario = {
    nombre: "Administrador",
    email: "admin@migasdeorodore.com",
  }

  const estadisticas = {
    total_usuarios: 156,
    total_productos: 45,
    ventas_hoy: {
      cantidad: 23,
      total: 850000,
    },
  }

  const crearNuevoUsuario = () => {
    console.log("[v0] Creando nuevo usuario...")
    alert("Funcionalidad de creación de usuario en desarrollo")
    setIsModalOpen(false)
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="container-fluid px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Sidebar Administrativo */}
          <div className="lg:col-span-1">
            {/* Perfil del administrador */}
            <Card className="bg-gray-800 border-gray-700 mb-4">
              <CardContent className="p-6 text-center">
                <div className="relative mb-4">
                  <div className="w-16 h-16 bg-amber-600 rounded-full flex items-center justify-center mx-auto">
                    <Shield className="w-8 h-8 text-white" />
                  </div>
                  <Badge className="absolute -top-1 -right-1 bg-red-600 text-white px-2 py-1 text-xs">Admin</Badge>
                </div>
                <h3 className="text-lg font-semibold text-white">{usuario.nombre}</h3>
                <p className="text-gray-400 text-sm mb-2">{usuario.email}</p>
                <Badge className="bg-gradient-to-r from-amber-600 to-amber-700 text-black px-3 py-2">
                  <Crown className="w-4 h-4 mr-1" />
                  Administrador del Sistema
                </Badge>
                <div className="mt-4 pt-4 border-t border-gray-700">
                  <small className="text-gray-400 flex items-center justify-center">
                    <Clock className="w-4 h-4 mr-1" />
                    Último acceso: Ahora
                  </small>
                </div>
              </CardContent>
            </Card>

            {/* Navegación administrativa */}
            <div className="space-y-2">
              <Button
                variant={activeTab === "dashboard" ? "default" : "ghost"}
                className={`w-full justify-start ${
                  activeTab === "dashboard"
                    ? "bg-amber-600 hover:bg-amber-700 text-black"
                    : "text-gray-300 hover:text-white hover:bg-gray-700"
                }`}
                onClick={() => setActiveTab("dashboard")}
              >
                <BarChart3 className="w-4 h-4 mr-2 text-amber-400" />
                Dashboard Principal
              </Button>
              <Button
                variant={activeTab === "usuarios" ? "default" : "ghost"}
                className={`w-full justify-start ${
                  activeTab === "usuarios"
                    ? "bg-amber-600 hover:bg-amber-700 text-black"
                    : "text-gray-300 hover:text-white hover:bg-gray-700"
                }`}
                onClick={() => setActiveTab("usuarios")}
              >
                <Users className="w-4 h-4 mr-2 text-blue-400" />
                Gestión de Personal
              </Button>
              <Button
                variant={activeTab === "clientes" ? "default" : "ghost"}
                className={`w-full justify-start ${
                  activeTab === "clientes"
                    ? "bg-amber-600 hover:bg-amber-700 text-black"
                    : "text-gray-300 hover:text-white hover:bg-gray-700"
                }`}
                onClick={() => setActiveTab("clientes")}
              >
                <UserFriends className="w-4 h-4 mr-2 text-green-400" />
                Gestión de Clientes
              </Button>
              <Button
                variant={activeTab === "productos" ? "default" : "ghost"}
                className={`w-full justify-start ${
                  activeTab === "productos"
                    ? "bg-amber-600 hover:bg-amber-700 text-black"
                    : "text-gray-300 hover:text-white hover:bg-gray-700"
                }`}
                onClick={() => setActiveTab("productos")}
              >
                <Package className="w-4 h-4 mr-2 text-blue-500" />
                Inventario y Productos
              </Button>
              <Button
                variant={activeTab === "pedidos" ? "default" : "ghost"}
                className={`w-full justify-start ${
                  activeTab === "pedidos"
                    ? "bg-amber-600 hover:bg-amber-700 text-black"
                    : "text-gray-300 hover:text-white hover:bg-gray-700"
                }`}
                onClick={() => setActiveTab("pedidos")}
              >
                <ClipboardList className="w-4 h-4 mr-2 text-amber-400" />
                Control de Pedidos
              </Button>
              <Button
                variant={activeTab === "reportes" ? "default" : "ghost"}
                className={`w-full justify-start ${
                  activeTab === "reportes"
                    ? "bg-amber-600 hover:bg-amber-700 text-black"
                    : "text-gray-300 hover:text-white hover:bg-gray-700"
                }`}
                onClick={() => setActiveTab("reportes")}
              >
                <BarChart3 className="w-4 h-4 mr-2 text-red-400" />
                Análisis y Reportes
              </Button>
              <Button
                variant={activeTab === "sistema" ? "default" : "ghost"}
                className={`w-full justify-start ${
                  activeTab === "sistema"
                    ? "bg-amber-600 hover:bg-amber-700 text-black"
                    : "text-gray-300 hover:text-white hover:bg-gray-700"
                }`}
                onClick={() => setActiveTab("sistema")}
              >
                <Settings className="w-4 h-4 mr-2 text-gray-400" />
                Configuración del Sistema
              </Button>
            </div>
          </div>

          {/* Contenido principal */}
          <div className="lg:col-span-3">
            {/* Dashboard Principal */}
            {activeTab === "dashboard" && (
              <div>
                <div className="flex justify-between items-center mb-6">
                  <div>
                    <h1 className="text-4xl font-bold text-amber-400 mb-2" style={{ fontFamily: "cursive" }}>
                      Centro de Control Administrativo
                    </h1>
                    <p className="text-gray-400">Panel de monitoreo y gestión integral - Migas de oro Dorè</p>
                  </div>
                  <Badge className="bg-green-600 text-white px-4 py-2 text-lg">
                    <Activity className="w-4 h-4 mr-2" />
                    Sistema Operativo
                  </Badge>
                </div>

                {/* Métricas principales */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                  <Card className="bg-gradient-to-br from-blue-600 to-purple-700 border-0">
                    <CardContent className="p-6 text-white">
                      <div className="flex justify-between items-center">
                        <div>
                          <h3 className="text-3xl font-bold mb-1">{estadisticas.total_usuarios}</h3>
                          <p className="text-blue-100 text-sm mb-1">Usuarios Registrados</p>
                          <small className="text-blue-200 flex items-center">
                            <ArrowUp className="w-3 h-3 mr-1" />
                            +12% este mes
                          </small>
                        </div>
                        <Users className="w-8 h-8 text-blue-200" />
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="bg-gradient-to-br from-pink-500 to-red-600 border-0">
                    <CardContent className="p-6 text-white">
                      <div className="flex justify-between items-center">
                        <div>
                          <h3 className="text-3xl font-bold mb-1">{estadisticas.total_productos}</h3>
                          <p className="text-pink-100 text-sm mb-1">Productos Activos</p>
                          <small className="text-pink-200 flex items-center">
                            <Box className="w-3 h-3 mr-1" />
                            En inventario
                          </small>
                        </div>
                        <Package className="w-8 h-8 text-pink-200" />
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="bg-gradient-to-br from-cyan-500 to-blue-600 border-0">
                    <CardContent className="p-6 text-white">
                      <div className="flex justify-between items-center">
                        <div>
                          <h3 className="text-3xl font-bold mb-1">{estadisticas.ventas_hoy.cantidad}</h3>
                          <p className="text-cyan-100 text-sm mb-1">Pedidos Procesados Hoy</p>
                          <small className="text-cyan-200 flex items-center">
                            <Clock className="w-3 h-3 mr-1" />
                            Tiempo real
                          </small>
                        </div>
                        <ShoppingCart className="w-8 h-8 text-cyan-200" />
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="bg-gradient-to-br from-green-500 to-teal-600 border-0">
                    <CardContent className="p-6 text-white">
                      <div className="flex justify-between items-center">
                        <div>
                          <h3 className="text-3xl font-bold mb-1">${estadisticas.ventas_hoy.total.toLocaleString()}</h3>
                          <p className="text-green-100 text-sm mb-1">Ingresos del Día</p>
                          <small className="text-green-200 flex items-center">
                            <TrendingUp className="w-3 h-3 mr-1" />
                            +8% vs ayer
                          </small>
                        </div>
                        <DollarSign className="w-8 h-8 text-green-200" />
                      </div>
                    </CardContent>
                  </Card>
                </div>

                {/* Panel de control operativo */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  <div className="lg:col-span-2">
                    <Card className="bg-gray-800 border-gray-700">
                      <CardHeader className="border-b border-gray-700">
                        <CardTitle className="text-white flex items-center">
                          <Terminal className="w-5 h-5 mr-2 text-amber-400" />
                          Centro de Comando Operativo
                        </CardTitle>
                      </CardHeader>
                      <CardContent className="p-6">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          <Button
                            className="h-20 bg-transparent border-2 border-green-600 text-green-400 hover:bg-green-600 hover:text-white flex flex-col items-center justify-center"
                            onClick={() => setIsModalOpen(true)}
                          >
                            <UserPlus className="w-6 h-6 mb-2" />
                            <strong>Crear Personal</strong>
                            <small className="text-xs opacity-75">Chef, Vendedor, Cocinero</small>
                          </Button>
                          <Button
                            className="h-20 bg-transparent border-2 border-blue-600 text-blue-400 hover:bg-blue-600 hover:text-white flex flex-col items-center justify-center"
                            onClick={() => alert("Redirigiendo a gestión de productos...")}
                          >
                            <PlusCircle className="w-6 h-6 mb-2" />
                            <strong>Nuevo Producto</strong>
                            <small className="text-xs opacity-75">Agregar al inventario</small>
                          </Button>
                          <Button
                            className="h-20 bg-transparent border-2 border-amber-600 text-amber-400 hover:bg-amber-600 hover:text-white flex flex-col items-center justify-center"
                            onClick={() => alert("Generando reportes de análisis...")}
                          >
                            <BarChart3 className="w-6 h-6 mb-2" />
                            <strong>Generar Reporte</strong>
                            <small className="text-xs opacity-75">Análisis de ventas</small>
                          </Button>
                          <Button
                            className="h-20 bg-transparent border-2 border-cyan-600 text-cyan-400 hover:bg-cyan-600 hover:text-white flex flex-col items-center justify-center"
                            onClick={() => alert("Accediendo a configuración del sistema...")}
                          >
                            <Settings className="w-6 h-6 mb-2" />
                            <strong>Configuración</strong>
                            <small className="text-xs opacity-75">Parámetros del sistema</small>
                          </Button>
                        </div>
                      </CardContent>
                    </Card>
                  </div>

                  <div>
                    <Card className="bg-gray-800 border-gray-700">
                      <CardHeader className="border-b border-gray-700">
                        <CardTitle className="text-white flex items-center">
                          <AlertTriangle className="w-5 h-5 mr-2 text-red-400" />
                          Alertas del Sistema
                        </CardTitle>
                      </CardHeader>
                      <CardContent className="p-6 space-y-4">
                        <div className="bg-amber-900/30 border border-amber-600/30 rounded-lg p-3">
                          <div className="flex items-center text-amber-400">
                            <Package className="w-4 h-4 mr-2" />
                            <strong>Stock Bajo:</strong> 3 productos
                          </div>
                        </div>
                        <div className="bg-blue-900/30 border border-blue-600/30 rounded-lg p-3">
                          <div className="flex items-center text-blue-400">
                            <Clock className="w-4 h-4 mr-2" />
                            <strong>Pedidos Pendientes:</strong> {estadisticas.ventas_hoy.cantidad}
                          </div>
                        </div>
                        <div className="bg-green-900/30 border border-green-600/30 rounded-lg p-3">
                          <div className="flex items-center text-green-400">
                            <Server className="w-4 h-4 mr-2" />
                            <strong>Sistema:</strong> Funcionando correctamente
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  </div>
                </div>
              </div>
            )}

            {/* Gestión de Personal */}
            {activeTab === "usuarios" && (
              <div>
                <div className="flex justify-between items-center mb-6">
                  <div>
                    <h1 className="text-3xl font-bold text-amber-400 mb-2" style={{ fontFamily: "cursive" }}>
                      Gestión de Personal
                    </h1>
                    <p className="text-gray-400">Administración de empleados: Chef, Vendedores y Cocineros</p>
                  </div>
                  <Button className="bg-green-600 hover:bg-green-700" onClick={() => setIsModalOpen(true)}>
                    <UserPlus className="w-4 h-4 mr-2" />
                    Nuevo Empleado
                  </Button>
                </div>

                {/* Filtros por tipo de empleado */}
                <Card className="bg-gray-800 border-gray-700 mb-6">
                  <CardContent className="p-4">
                    <div className="flex flex-wrap gap-2">
                      <Button
                        variant={filtroPersonal === "todos" ? "default" : "outline"}
                        size="sm"
                        onClick={() => setFiltroPersonal("todos")}
                        className={filtroPersonal === "todos" ? "bg-white text-black" : "border-gray-600 text-gray-300"}
                      >
                        Todos
                      </Button>
                      <Button
                        variant={filtroPersonal === "chef" ? "default" : "outline"}
                        size="sm"
                        onClick={() => setFiltroPersonal("chef")}
                        className={
                          filtroPersonal === "chef" ? "bg-amber-600 text-white" : "border-amber-600 text-amber-400"
                        }
                      >
                        <ChefHat className="w-4 h-4 mr-1" />
                        Chef
                      </Button>
                      <Button
                        variant={filtroPersonal === "vendedor" ? "default" : "outline"}
                        size="sm"
                        onClick={() => setFiltroPersonal("vendedor")}
                        className={
                          filtroPersonal === "vendedor" ? "bg-green-600 text-white" : "border-green-600 text-green-400"
                        }
                      >
                        <CashRegister className="w-4 h-4 mr-1" />
                        Vendedores
                      </Button>
                      <Button
                        variant={filtroPersonal === "cocinero" ? "default" : "outline"}
                        size="sm"
                        onClick={() => setFiltroPersonal("cocinero")}
                        className={
                          filtroPersonal === "cocinero" ? "bg-blue-600 text-white" : "border-blue-600 text-blue-400"
                        }
                      >
                        <Utensils className="w-4 h-4 mr-1" />
                        Cocineros
                      </Button>
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-gray-800 border-gray-700">
                  <CardContent className="p-6">
                    <div className="text-center py-12">
                      <Users className="w-16 h-16 text-gray-500 mx-auto mb-4 opacity-50" />
                      <p className="text-gray-400">Cargando personal... Implementar funcionalidad de listado</p>
                    </div>
                  </CardContent>
                </Card>
              </div>
            )}

            {/* Gestión de Clientes */}
            {activeTab === "clientes" && (
              <div>
                <div className="flex justify-between items-center mb-6">
                  <div>
                    <h1 className="text-3xl font-bold text-amber-400 mb-2" style={{ fontFamily: "cursive" }}>
                      Gestión de Clientes
                    </h1>
                    <p className="text-gray-400">Administración y seguimiento de la base de clientes</p>
                  </div>
                  <div className="flex gap-2">
                    <Button variant="outline" className="border-green-600 text-green-400 bg-transparent">
                      <Download className="w-4 h-4 mr-2" />
                      Exportar
                    </Button>
                    <Button variant="outline" className="border-blue-600 text-blue-400 bg-transparent">
                      <Filter className="w-4 h-4 mr-2" />
                      Filtros
                    </Button>
                  </div>
                </div>

                <Card className="bg-gray-800 border-gray-700">
                  <CardContent className="p-6">
                    <div className="text-center py-12">
                      <UserFriends className="w-16 h-16 text-gray-500 mx-auto mb-4 opacity-50" />
                      <p className="text-gray-400">Implementar listado de clientes con estadísticas</p>
                    </div>
                  </CardContent>
                </Card>
              </div>
            )}

            {/* Otras pestañas con contenido placeholder */}
            {(activeTab === "productos" ||
              activeTab === "pedidos" ||
              activeTab === "reportes" ||
              activeTab === "sistema") && (
              <div>
                <h1 className="text-3xl font-bold text-amber-400 mb-6" style={{ fontFamily: "cursive" }}>
                  {activeTab === "productos" && "Gestión de Productos"}
                  {activeTab === "pedidos" && "Gestión de Pedidos"}
                  {activeTab === "reportes" && "Reportes y Análisis"}
                  {activeTab === "sistema" && "Configuración del Sistema"}
                </h1>

                <Card className="bg-gray-800 border-gray-700">
                  <CardContent className="p-6">
                    <div className="bg-blue-900/30 border border-blue-600/30 rounded-lg p-4">
                      <div className="flex items-start space-x-3">
                        <AlertTriangle className="w-5 h-5 text-blue-400 mt-0.5 flex-shrink-0" />
                        <p className="text-blue-100 text-sm leading-relaxed">
                          {activeTab === "productos" &&
                            "Panel de gestión de productos en desarrollo. Próximamente podrás agregar, editar y eliminar productos."}
                          {activeTab === "pedidos" &&
                            "Panel de gestión de pedidos en desarrollo. Próximamente podrás ver y gestionar todos los pedidos."}
                          {activeTab === "reportes" &&
                            "Sistema de reportes en desarrollo. Próximamente tendrás acceso a análisis detallados de ventas y rendimiento."}
                          {activeTab === "sistema" &&
                            "Panel de configuración del sistema en desarrollo. Próximamente podrás ajustar parámetros y opciones del sistema."}
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Modal para crear nuevo empleado */}
      <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
        <DialogContent className="bg-gray-800 border-gray-700 text-white max-w-2xl">
          <DialogHeader>
            <DialogTitle className="flex items-center text-xl">
              <UserPlus className="w-5 h-5 mr-2" />
              Crear Nuevo Empleado
            </DialogTitle>
          </DialogHeader>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="nombre" className="text-gray-300">
                Nombre Completo
              </Label>
              <Input id="nombre" className="bg-gray-700 border-gray-600 text-white focus:border-amber-500" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="email" className="text-gray-300">
                Email
              </Label>
              <Input
                id="email"
                type="email"
                className="bg-gray-700 border-gray-600 text-white focus:border-amber-500"
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="telefono" className="text-gray-300">
                Teléfono
              </Label>
              <Input
                id="telefono"
                type="tel"
                className="bg-gray-700 border-gray-600 text-white focus:border-amber-500"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="rol" className="text-gray-300">
                Rol
              </Label>
              <Select>
                <SelectTrigger className="bg-gray-700 border-gray-600 text-white">
                  <SelectValue placeholder="Seleccionar rol..." />
                </SelectTrigger>
                <SelectContent className="bg-gray-700 border-gray-600">
                  <SelectItem value="chef">👨‍🍳 Chef (Jefe de Cocina)</SelectItem>
                  <SelectItem value="vendedor">💼 Vendedor</SelectItem>
                  <SelectItem value="cocinero">🍳 Cocinero</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="md:col-span-2 space-y-2">
              <Label htmlFor="direccion" className="text-gray-300">
                Dirección
              </Label>
              <Textarea
                id="direccion"
                rows={2}
                className="bg-gray-700 border-gray-600 text-white focus:border-amber-500"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password" className="text-gray-300">
                Contraseña
              </Label>
              <Input
                id="password"
                type="password"
                className="bg-gray-700 border-gray-600 text-white focus:border-amber-500"
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="confirm_password" className="text-gray-300">
                Confirmar Contraseña
              </Label>
              <Input
                id="confirm_password"
                type="password"
                className="bg-gray-700 border-gray-600 text-white focus:border-amber-500"
                required
              />
            </div>
          </div>
          <div className="flex justify-end gap-3 pt-4 border-t border-gray-700">
            <Button variant="outline" onClick={() => setIsModalOpen(false)} className="border-gray-600 text-gray-300">
              Cancelar
            </Button>
            <Button onClick={crearNuevoUsuario} className="bg-green-600 hover:bg-green-700">
              <Save className="w-4 h-4 mr-2" />
              Crear Empleado
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  )
}
