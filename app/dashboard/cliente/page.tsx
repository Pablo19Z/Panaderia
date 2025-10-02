"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Checkbox } from "@/components/ui/checkbox"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import {
  User,
  ShoppingBag,
  Heart,
  Settings,
  Headphones,
  Plus,
  Eye,
  Bell,
  Shield,
  Phone,
  Mail,
  Clock,
  Trash2,
  Send,
  Calendar,
  HelpCircle,
  Info,
} from "lucide-react"

export default function ClienteDashboard() {
  const [activeTab, setActiveTab] = useState("pedidos")

  // Datos de ejemplo - en una app real vendrían de una API
  const usuario = {
    nombre: "fabian",
    email: "fabian@gmail.com",
    telefono: "+57 300 123 4567",
    direccion: "Calle 123 #45-67",
  }

  const pedidos = [
    {
      id: 1,
      total: 25000,
      estado: "entregado",
      fecha: "2024-01-15",
      direccion: "Calle 123 #45-67",
    },
    {
      id: 2,
      total: 18500,
      estado: "preparando",
      fecha: "2024-01-20",
      direccion: "Calle 123 #45-67",
    },
  ]

  const getEstadoBadge = (estado: string) => {
    const variants = {
      pendiente: "bg-yellow-500",
      preparando: "bg-blue-500",
      listo: "bg-green-500",
      entregado: "bg-amber-600",
      cancelado: "bg-red-500",
    }
    return variants[estado as keyof typeof variants] || "bg-gray-500"
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="container mx-auto px-4 py-8">
        {/* Mensaje de bienvenida */}
        <div className="bg-green-800 border border-green-600 rounded-lg p-4 mb-6">
          <p className="text-green-100">¡Bienvenido fabian!</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Sidebar */}
          <div className="lg:col-span-1">
            {/* Perfil del usuario */}
            <Card className="bg-gray-800 border-gray-700 mb-4">
              <CardContent className="p-6 text-center">
                <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-3">
                  <User className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-lg font-semibold text-white">{usuario.nombre}</h3>
                <p className="text-gray-400 text-sm">{usuario.email}</p>
                <Badge className="bg-blue-600 hover:bg-blue-700 mt-2">Cliente</Badge>
              </CardContent>
            </Card>

            {/* Navegación */}
            <div className="space-y-2">
              <Button
                variant={activeTab === "pedidos" ? "default" : "ghost"}
                className={`w-full justify-start ${activeTab === "pedidos" ? "bg-blue-600 hover:bg-blue-700" : "text-gray-300 hover:text-white hover:bg-gray-700"}`}
                onClick={() => setActiveTab("pedidos")}
              >
                <ShoppingBag className="w-4 h-4 mr-2" />
                Mis Pedidos
              </Button>
              <Button
                variant={activeTab === "perfil" ? "default" : "ghost"}
                className={`w-full justify-start ${activeTab === "perfil" ? "bg-blue-600 hover:bg-blue-700" : "text-gray-300 hover:text-white hover:bg-gray-700"}`}
                onClick={() => setActiveTab("perfil")}
              >
                <User className="w-4 h-4 mr-2" />
                Mi Perfil
              </Button>
              <Button
                variant={activeTab === "configuracion" ? "default" : "ghost"}
                className={`w-full justify-start ${activeTab === "configuracion" ? "bg-blue-600 hover:bg-blue-700" : "text-gray-300 hover:text-white hover:bg-gray-700"}`}
                onClick={() => setActiveTab("configuracion")}
              >
                <Settings className="w-4 h-4 mr-2" />
                Configuración
              </Button>
              <Button
                variant={activeTab === "soporte" ? "default" : "ghost"}
                className={`w-full justify-start ${activeTab === "soporte" ? "bg-blue-600 hover:bg-blue-700" : "text-gray-300 hover:text-white hover:bg-gray-700"}`}
                onClick={() => setActiveTab("soporte")}
              >
                <Headphones className="w-4 h-4 mr-2" />
                Soporte
              </Button>
            </div>
          </div>

          {/* Contenido principal */}
          <div className="lg:col-span-3">
            {/* Tab de Pedidos */}
            {activeTab === "pedidos" && (
              <div>
                <div className="flex justify-between items-center mb-6">
                  <h1 className="text-3xl font-bold text-amber-400" style={{ fontFamily: "cursive" }}>
                    Mis Pedidos
                  </h1>
                  <Button className="bg-amber-600 hover:bg-amber-700">
                    <Plus className="w-4 h-4 mr-2" />
                    Nuevo Pedido
                  </Button>
                </div>

                {pedidos.length > 0 ? (
                  <div className="space-y-4">
                    {pedidos.map((pedido) => (
                      <Card key={pedido.id} className="bg-gray-800 border-gray-700">
                        <CardContent className="p-4">
                          <div className="grid grid-cols-1 md:grid-cols-6 gap-4 items-center">
                            <div>
                              <h6 className="font-semibold text-white">Pedido #{pedido.id}</h6>
                              <small className="text-gray-400">{pedido.fecha}</small>
                            </div>
                            <div>
                              <div className="font-bold text-amber-400">${pedido.total.toLocaleString()}</div>
                            </div>
                            <div>
                              <Badge className={`${getEstadoBadge(pedido.estado)} text-white`}>
                                {pedido.estado.charAt(0).toUpperCase() + pedido.estado.slice(1)}
                              </Badge>
                            </div>
                            <div className="md:col-span-2">
                              <small className="text-gray-400">{pedido.direccion}</small>
                            </div>
                            <div className="text-right">
                              <Button
                                size="sm"
                                variant="outline"
                                className="border-gray-600 text-gray-300 hover:text-white bg-transparent"
                              >
                                <Eye className="w-4 h-4" />
                              </Button>
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-12">
                    <ShoppingBag className="w-16 h-16 text-gray-500 mx-auto mb-4" />
                    <h4 className="text-xl text-gray-400 mb-2">No tienes pedidos aún</h4>
                    <p className="text-gray-500 mb-4">¡Haz tu primer pedido y disfruta de nuestros productos!</p>
                    <Button className="bg-amber-600 hover:bg-amber-700">Ver Productos</Button>
                  </div>
                )}
              </div>
            )}

            {/* Tab de Perfil */}
            {activeTab === "perfil" && (
              <div>
                <h1 className="text-3xl font-bold text-amber-400 mb-6" style={{ fontFamily: "cursive" }}>
                  Mi Perfil
                </h1>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                  <Card className="bg-gray-800 border-amber-600/20 hover:border-amber-600/40 transition-colors">
                    <CardContent className="p-6 text-center">
                      <div className="w-12 h-12 bg-blue-600 rounded-lg flex items-center justify-center mx-auto mb-3">
                        <ShoppingBag className="w-6 h-6 text-white" />
                      </div>
                      <h3 className="text-2xl font-bold text-white mb-1">0</h3>
                      <p className="text-gray-400 text-sm">Pedidos Realizados</p>
                    </CardContent>
                  </Card>

                  <Card className="bg-gray-800 border-amber-600/20 hover:border-amber-600/40 transition-colors">
                    <CardContent className="p-6 text-center">
                      <div className="w-12 h-12 bg-red-600 rounded-lg flex items-center justify-center mx-auto mb-3">
                        <Heart className="w-6 h-6 text-white" />
                      </div>
                      <h3 className="text-2xl font-bold text-white mb-1">0</h3>
                      <p className="text-gray-400 text-sm">Productos Favoritos</p>
                    </CardContent>
                  </Card>

                  <Card className="bg-gray-800 border-amber-600/20 hover:border-amber-600/40 transition-colors">
                    <CardContent className="p-6 text-center">
                      <div className="w-12 h-12 bg-green-600 rounded-lg flex items-center justify-center mx-auto mb-3">
                        <Calendar className="w-6 h-6 text-white" />
                      </div>
                      <h3 className="text-2xl font-bold text-white mb-1">Cliente</h3>
                      <p className="text-gray-400 text-sm">Desde 2024</p>
                    </CardContent>
                  </Card>
                </div>

                <Card className="bg-gray-800 border-amber-600/20">
                  <CardHeader className="border-b border-gray-700">
                    <CardTitle className="text-white flex items-center text-xl">
                      <User className="w-6 h-6 mr-3" />
                      Información Personal
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="p-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div className="space-y-2">
                        <Label htmlFor="nombre" className="text-gray-300 font-medium">
                          Nombre Completo
                        </Label>
                        <Input
                          id="nombre"
                          value={usuario.nombre}
                          readOnly
                          className="bg-gray-700 border-gray-600 text-white focus:border-amber-500 focus:ring-amber-500/20"
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="email" className="text-gray-300 font-medium">
                          Email
                        </Label>
                        <Input
                          id="email"
                          value={usuario.email}
                          readOnly
                          className="bg-gray-700 border-gray-600 text-white focus:border-amber-500 focus:ring-amber-500/20"
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="telefono" className="text-gray-300 font-medium">
                          Teléfono
                        </Label>
                        <Input
                          id="telefono"
                          value={usuario.telefono}
                          readOnly
                          className="bg-gray-700 border-gray-600 text-white focus:border-amber-500 focus:ring-amber-500/20"
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="direccion" className="text-gray-300 font-medium">
                          Dirección
                        </Label>
                        <Input
                          id="direccion"
                          value={usuario.direccion}
                          readOnly
                          className="bg-gray-700 border-gray-600 text-white focus:border-amber-500 focus:ring-amber-500/20"
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="rol" className="text-gray-300 font-medium">
                          Tipo de Usuario
                        </Label>
                        <Input
                          id="rol"
                          value="Cliente"
                          readOnly
                          className="bg-gray-700 border-gray-600 text-white focus:border-amber-500 focus:ring-amber-500/20"
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="estado" className="text-gray-300 font-medium">
                          Estado de la Cuenta
                        </Label>
                        <Input
                          id="estado"
                          value="Activa"
                          readOnly
                          className="bg-gray-700 border-gray-600 text-white focus:border-amber-500 focus:ring-amber-500/20"
                        />
                      </div>
                    </div>

                    <div className="mt-8 pt-6 border-t border-gray-700">
                      <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
                        <Settings className="w-5 h-5 mr-2" />
                        Preferencias de Cuenta
                      </h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="flex items-center space-x-3 p-3 bg-gray-700/50 rounded-lg">
                          <Checkbox id="notificaciones" checked disabled className="border-amber-500" />
                          <Label htmlFor="notificaciones" className="text-gray-300 cursor-pointer">
                            Recibir notificaciones por email
                          </Label>
                        </div>
                        <div className="flex items-center space-x-3 p-3 bg-gray-700/50 rounded-lg">
                          <Checkbox id="promociones" checked disabled className="border-amber-500" />
                          <Label htmlFor="promociones" className="text-gray-300 cursor-pointer">
                            Recibir ofertas y promociones
                          </Label>
                        </div>
                      </div>
                    </div>

                    <div className="bg-blue-900/30 border border-blue-600/30 rounded-lg p-4 mt-6">
                      <div className="flex items-start space-x-3">
                        <Info className="w-5 h-5 text-blue-400 mt-0.5 flex-shrink-0" />
                        <p className="text-blue-100 text-sm leading-relaxed">
                          Para actualizar tu información de perfil, contacta con nuestro equipo de soporte.
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            )}

            {/* Tab de Configuración */}
            {activeTab === "configuracion" && (
              <div>
                <h1 className="text-3xl font-bold text-amber-400 mb-6" style={{ fontFamily: "cursive" }}>
                  Configuración de Cuenta
                </h1>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <Card className="bg-gray-800 border-gray-700">
                    <CardHeader>
                      <CardTitle className="text-white flex items-center">
                        <Bell className="w-5 h-5 mr-2" />
                        Notificaciones
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <div className="flex items-center space-x-2">
                        <Checkbox id="emailNotif" defaultChecked />
                        <Label htmlFor="emailNotif" className="text-gray-300">
                          Notificaciones por email
                        </Label>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Checkbox id="orderNotif" defaultChecked />
                        <Label htmlFor="orderNotif" className="text-gray-300">
                          Estado de pedidos
                        </Label>
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="bg-gray-800 border-gray-700">
                    <CardHeader>
                      <CardTitle className="text-white flex items-center">
                        <Shield className="w-5 h-5 mr-2" />
                        Privacidad
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <div className="flex items-center space-x-2">
                        <Checkbox id="profilePublic" />
                        <Label htmlFor="profilePublic" className="text-gray-300">
                          Perfil público
                        </Label>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Checkbox id="shareData" />
                        <Label htmlFor="shareData" className="text-gray-300">
                          Compartir datos para mejoras
                        </Label>
                      </div>
                      <Button
                        variant="outline"
                        size="sm"
                        className="border-red-600 text-red-400 hover:bg-red-600 hover:text-white bg-transparent"
                      >
                        <Trash2 className="w-4 h-4 mr-1" />
                        Eliminar cuenta
                      </Button>
                    </CardContent>
                  </Card>
                </div>
              </div>
            )}

            {/* Tab de Soporte */}
            {activeTab === "soporte" && (
              <div>
                <h1 className="text-3xl font-bold text-amber-400 mb-6" style={{ fontFamily: "cursive" }}>
                  Centro de Soporte
                </h1>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  <div className="lg:col-span-2">
                    <Card className="bg-gray-800 border-gray-700">
                      <CardHeader>
                        <CardTitle className="text-white flex items-center">
                          <HelpCircle className="w-5 h-5 mr-2" />
                          ¿Necesitas ayuda?
                        </CardTitle>
                      </CardHeader>
                      <CardContent className="space-y-4">
                        <div>
                          <Label htmlFor="asunto" className="text-gray-300">
                            Asunto
                          </Label>
                          <Select>
                            <SelectTrigger className="bg-gray-700 border-gray-600 text-white">
                              <SelectValue placeholder="Selecciona un asunto" />
                            </SelectTrigger>
                            <SelectContent className="bg-gray-700 border-gray-600">
                              <SelectItem value="pedido">Problema con pedido</SelectItem>
                              <SelectItem value="productos">Consulta sobre productos</SelectItem>
                              <SelectItem value="tecnico">Problema técnico</SelectItem>
                              <SelectItem value="sugerencia">Sugerencia</SelectItem>
                              <SelectItem value="otro">Otro</SelectItem>
                            </SelectContent>
                          </Select>
                        </div>
                        <div>
                          <Label htmlFor="mensaje" className="text-gray-300">
                            Mensaje
                          </Label>
                          <Textarea
                            id="mensaje"
                            placeholder="Describe tu consulta..."
                            rows={4}
                            className="bg-gray-700 border-gray-600 text-white"
                          />
                        </div>
                        <Button className="bg-amber-600 hover:bg-amber-700">
                          <Send className="w-4 h-4 mr-2" />
                          Enviar Consulta
                        </Button>
                      </CardContent>
                    </Card>
                  </div>

                  <div>
                    <Card className="bg-gray-800 border-gray-700">
                      <CardHeader>
                        <CardTitle className="text-white flex items-center">
                          <Info className="w-5 h-5 mr-2" />
                          Contacto Directo
                        </CardTitle>
                      </CardHeader>
                      <CardContent className="space-y-3">
                        <div className="flex items-center text-gray-300">
                          <Phone className="w-4 h-4 mr-2" />
                          +57 300 123 4567
                        </div>
                        <div className="flex items-center text-gray-300">
                          <Mail className="w-4 h-4 mr-2" />
                          soporte@migasdeorodore.com
                        </div>
                        <div className="flex items-center text-gray-300">
                          <Clock className="w-4 h-4 mr-2" />
                          Lun-Vie: 8AM-6PM
                        </div>
                        <hr className="border-gray-600" />
                        <div>
                          <h6 className="text-white font-semibold mb-2">Preguntas Frecuentes</h6>
                          <ul className="space-y-1 text-sm">
                            <li>
                              <a href="#" className="text-blue-400 hover:text-blue-300">
                                ¿Cómo hacer un pedido?
                              </a>
                            </li>
                            <li>
                              <a href="#" className="text-blue-400 hover:text-blue-300">
                                Tiempos de entrega
                              </a>
                            </li>
                            <li>
                              <a href="#" className="text-blue-400 hover:text-blue-300">
                                Métodos de pago
                              </a>
                            </li>
                          </ul>
                        </div>
                      </CardContent>
                    </Card>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
