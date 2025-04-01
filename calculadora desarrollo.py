import tkinter as tk
from tkinter import ttk
import math
from tkinter import Menu
import json
from datetime import datetime

class Calculadora:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Calculadora Avanzada")
        self.ventana.geometry("400x600")
        
        # Inicialización de variables
        self.operacion = ""  # Añadido aquí explícitamente
        self.modo_oscuro = False
        self.tema_claro = {'bg': '#ffffff', 'fg': '#000000', 'button': '#f0f0f0'}
        self.tema_oscuro = {'bg': '#2d2d2d', 'fg': '#ffffff', 'button': '#404040'}
        self.historial = []
        
        # Crear menú superior
        self.crear_menu()
        
        # Frame principal
        self.frame_principal = ttk.Frame(self.ventana)
        self.frame_principal.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Display y historial
        self.frame_displays = ttk.Frame(self.frame_principal)
        self.frame_displays.pack(fill='x', pady=5)
        
        # Historial visible
        self.historial_display = tk.Text(self.frame_displays, height=3, font=('Arial', 10))
        self.historial_display.pack(fill='x', pady=2)
        
        # Display principal
        self.display = ttk.Entry(self.frame_displays, justify="right", font=('Arial', 24))
        self.display.pack(fill='x', pady=5)
        
        # Frame para botones
        self.frame_botones = ttk.Frame(self.frame_principal)
        self.frame_botones.pack(expand=True, fill='both')
        
        # Botones científicos
        botones_cientificos = [
            'sin', 'cos', 'tan', 'π',
            '√', 'x²', 'x³', 'x^y',
            '(', ')', 'mod', 'log',
        ]
        
        self.crear_botones_cientificos(botones_cientificos)
        
        # Botones básicos
        botones_basicos = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
        ]
        
        self.crear_botones_basicos(botones_basicos)
        
        # Fila de botones especiales
        self.crear_botones_especiales()
        
        # Aplicar tema inicial
        self.aplicar_tema()

    def crear_menu(self):
        menu_bar = Menu(self.ventana)
        self.ventana.config(menu=menu_bar)
        
        archivo_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Archivo", menu=archivo_menu)
        archivo_menu.add_command(label="Guardar Historial", command=self.guardar_historial)
        archivo_menu.add_command(label="Cargar Historial", command=self.cargar_historial)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self.ventana.quit)
        
        ver_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Ver", menu=ver_menu)
        ver_menu.add_command(label="Cambiar Tema", command=self.cambiar_tema)

    def crear_botones_cientificos(self, botones):
        frame_cientificos = ttk.Frame(self.frame_botones)
        frame_cientificos.pack(fill='x')
        
        for i, texto in enumerate(botones):
            comando = lambda x=texto: self.click_cientifico(x)
            btn = ttk.Button(frame_cientificos, text=texto, command=comando)
            btn.grid(row=i//4, column=i%4, sticky="nsew", padx=2, pady=2)

    def crear_botones_basicos(self, botones):
        frame_basicos = ttk.Frame(self.frame_botones)
        frame_basicos.pack(fill='x')
        
        for i, texto in enumerate(botones):
            comando = lambda x=texto: self.click(x)
            btn = ttk.Button(frame_basicos, text=texto, command=comando)
            btn.grid(row=i//4, column=i%4, sticky="nsew", padx=2, pady=2)

    def crear_botones_especiales(self):
        frame_especial = ttk.Frame(self.frame_botones)
        frame_especial.pack(fill='x')
        
        ttk.Button(frame_especial, text="C", command=lambda: self.click('C')).pack(side='left', expand=True, fill='x', padx=2)
        ttk.Button(frame_especial, text="⌫", command=self.borrar_ultimo).pack(side='left', expand=True, fill='x', padx=2)
        ttk.Button(frame_especial, text="Ans", command=self.usar_ultimo_resultado).pack(side='left', expand=True, fill='x', padx=2)

    def click_cientifico(self, valor):
        if not hasattr(self, 'operacion'):
            self.operacion = ""
            
        if valor == 'sin':
            self.operacion += 'math.sin('
        elif valor == 'cos':
            self.operacion += 'math.cos('
        elif valor == 'tan':
            self.operacion += 'math.tan('
        elif valor == 'π':
            self.operacion += 'math.pi'
        elif valor == '√':
            self.operacion += 'math.sqrt('
        elif valor == 'x²':
            self.operacion += '**2'
        elif valor == 'x³':
            self.operacion += '**3'
        elif valor == 'x^y':
            self.operacion += '**'
        elif valor == 'log':
            self.operacion += 'math.log10('
        else:
            self.operacion += valor
        self.actualizar_display()

    def borrar_ultimo(self):
        self.operacion = self.operacion[:-1]
        self.actualizar_display()

    def usar_ultimo_resultado(self):
        if self.historial:
            ultimo_resultado = self.historial[-1].split('=')[1].strip()
            self.operacion += ultimo_resultado
            self.actualizar_display()

    def actualizar_display(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, self.operacion)

    def guardar_historial(self):
        with open('historial_calculadora.json', 'w') as f:
            json.dump(self.historial, f)

    def cargar_historial(self):
        try:
            with open('historial_calculadora.json', 'r') as f:
                self.historial = json.load(f)
                self.actualizar_historial_display()
        except FileNotFoundError:
            pass

    def actualizar_historial_display(self):
        self.historial_display.delete(1.0, tk.END)
        ultimas_operaciones = self.historial[-3:] if self.historial else []
        for op in ultimas_operaciones:
            self.historial_display.insert(tk.END, f"{op}\n")

    def cambiar_tema(self):
        self.modo_oscuro = not self.modo_oscuro
        self.aplicar_tema()
    
    def aplicar_tema(self):
        tema = self.tema_oscuro if self.modo_oscuro else self.tema_claro
        self.ventana.configure(bg=tema['bg'])
        style = ttk.Style()
        style.configure('TButton', background=tema['button'], foreground=tema['fg'])
        style.configure('TEntry', background=tema['bg'], foreground=tema['fg'])
        style.configure('TFrame', background=tema['bg'])
        self.historial_display.configure(bg=tema['bg'], fg=tema['fg'])
    
    def click(self, valor):
        if valor == '=':
            if not self.operacion:  # Verificar si hay una operación
                return
            try:
                # Limpieza de la operación antes de evaluarla
                operacion_limpia = self.operacion.strip()
                if not operacion_limpia:
                    return
                
                resultado = eval(operacion_limpia)
                self.historial.append(f"{operacion_limpia} = {resultado}")
                self.actualizar_historial_display()
                self.operacion = str(resultado)
                self.display.delete(0, tk.END)
                self.display.insert(0, self.operacion)
            except Exception as e:
                self.display.delete(0, tk.END)
                self.display.insert(0, "Error")
                self.operacion = ""
        elif valor == 'C':
            self.operacion = ""
            self.display.delete(0, tk.END)
        else:
            self.operacion += valor
            self.display.delete(0, tk.END)
            self.display.insert(0, self.operacion)
    
    def iniciar(self):
        self.ventana.mainloop()

# Crear y ejecutar la calculadora
if __name__ == "__main__":
    calc = Calculadora()
    calc.iniciar()
