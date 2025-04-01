import tkinter as tk
from tkinter import ttk

class Calculadora:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Calculadora")
        self.ventana.geometry("300x400")
        
        # Variable para almacenar la operación
        self.operacion = ""
        
        # Display
        self.display = ttk.Entry(self.ventana, justify="right", font=('Arial', 20))
        self.display.grid(row=0, column=0, columnspan=4, pady=5, padx=5, sticky="nsew")
        
        # Botones
        botones = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'C'
        ]
        
        # Crear y posicionar botones
        row = 1
        col = 0
        for boton in botones:
            comando = lambda x=boton: self.click(x)
            if boton == 'C':
                ttk.Button(self.ventana, text=boton, command=comando).grid(row=5, column=0, columnspan=4, sticky="nsew")
            else:
                ttk.Button(self.ventana, text=boton, command=comando).grid(row=row, column=col, sticky="nsew")
                col += 1
                if col > 3:
                    col = 0
                    row += 1
        
        # Configurar el grid
        for i in range(6):
            self.ventana.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.ventana.grid_columnconfigure(i, weight=1)
    
    def click(self, valor):
        if valor == '=':
            try:
                resultado = eval(self.operacion)
                self.operacion = str(resultado)
                self.display.delete(0, tk.END)
                self.display.insert(0, self.operacion)
            except:
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
