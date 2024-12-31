import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import pickle
import os
import re  # Para validación de correos electrónicos


class BancoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Banca Móvil")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f8ff")  # Fondo de color claro

        self.usuarios, self.cuentas = self.cargar_datos()
        self.usuario_actual = None

        # Crear la pantalla de inicio de sesión
        self.crear_pantalla_login()

    def limpiar_pantalla(self):
        """Limpia la pantalla actual"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def validar_correo(self, correo):
        """Valida si el correo es válido usando expresiones regulares"""
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(patron, correo)

    def crear_pantalla_login(self):
        """Pantalla inicial de inicio de sesión"""
        self.limpiar_pantalla()

        tk.Label(self.root, text="Inicio de Sesión", font=("Arial", 16, "bold"), bg="#f0f8ff", fg="#01579b").pack(pady=20)

        tk.Label(self.root, text="Correo:", bg="#f0f8ff").pack(pady=5)
        self.entry_correo = tk.Entry(self.root, width=30)
        self.entry_correo.pack(pady=5)

        tk.Label(self.root, text="Contraseña:", bg="#f0f8ff").pack(pady=5)
        self.entry_password = tk.Entry(self.root, show="*", width=30)
        self.entry_password.pack(pady=5)

        self.aceptar_terminos_login = tk.BooleanVar()
        tk.Checkbutton(self.root, text="Acepto los términos y condiciones", variable=self.aceptar_terminos_login, bg="#f0f8ff", font=("Arial", 10), fg="#01579b").pack(pady=10)

        tk.Button(self.root, text="Iniciar Sesión", command=self.iniciar_sesion, bg="#4caf50", fg="white", width=15).pack(pady=10)
        tk.Button(self.root, text="Crear Cuenta", command=self.crear_pantalla_registro, bg="#2196f3", fg="white", width=15).pack(pady=10)

    def crear_pantalla_registro(self):
        """Pantalla de registro de usuario"""
        self.limpiar_pantalla()

        tk.Label(self.root, text="Registro de Usuario", font=("Arial", 16, "bold"), bg="#f0f8ff", fg="#01579b").pack(pady=20)

        tk.Label(self.root, text="Correo:", bg="#f0f8ff").pack(pady=5)
        self.entry_nuevo_correo = tk.Entry(self.root, width=30)
        self.entry_nuevo_correo.pack(pady=5)

        tk.Label(self.root, text="Contraseña:", bg="#f0f8ff").pack(pady=5)
        self.entry_nueva_password = tk.Entry(self.root, show="*", width=30)
        self.entry_nueva_password.pack(pady=5)

        tk.Label(self.root, text="Foto:", bg="#f0f8ff").pack(pady=5)
        self.entry_foto = tk.Entry(self.root, width=30)
        self.entry_foto.pack(pady=5)
        tk.Button(self.root, text="Seleccionar Foto", command=self.seleccionar_foto, bg="#607d8b", fg="white").pack(pady=5)

        self.aceptar_terminos = tk.BooleanVar()
        tk.Checkbutton(self.root, text="Acepto los términos y condiciones", variable=self.aceptar_terminos, bg="#f0f8ff", font=("Arial", 10), fg="#01579b").pack(pady=10)

        tk.Button(self.root, text="Crear Cuenta", command=self.crear_cuenta, bg="#4caf50", fg="white", width=15).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.crear_pantalla_login, bg="#2196f3", fg="white", width=15).pack(pady=10)

    def seleccionar_foto(self):
        """Seleccionar una foto del usuario"""
        filename = filedialog.askopenfilename(title="Seleccionar Foto", filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")])
        self.entry_foto.delete(0, tk.END)
        self.entry_foto.insert(0, filename)

    def crear_cuenta(self):
        """Crea una nueva cuenta bancaria"""
        correo = self.entry_nuevo_correo.get().strip()
        contrasena = self.entry_nueva_password.get().strip()
        foto = self.entry_foto.get().strip()

        if not correo or not contrasena or not foto:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")
            return

        if not self.validar_correo(correo):
            messagebox.showerror("Error", "Correo inválido. Por favor, ingrese un correo válido.")
            return

        if correo in self.usuarios:
            messagebox.showerror("Error", "El correo ya está registrado.")
            return

        self.usuarios[correo] = {"contrasena": contrasena, "foto": foto}
        self.cuentas[correo] = {"saldo": 0.0, "transacciones": []}
        self.guardar_datos()
        messagebox.showinfo("Éxito", "Cuenta creada con éxito.")
        self.crear_pantalla_login()

    def iniciar_sesion(self):
        """Inicia sesión con un usuario existente"""
        correo = self.entry_correo.get().strip()
        contrasena = self.entry_password.get().strip()

        if not self.aceptar_terminos_login.get():
            messagebox.showerror("Error", "Debe aceptar los términos y condiciones.")
            return

        if correo in self.usuarios and self.usuarios[correo]["contrasena"] == contrasena:
            self.usuario_actual = correo
            self.crear_pantalla_principal()
        else:
            messagebox.showerror("Error", "Correo o contraseña incorrectos.")

    def crear_pantalla_principal(self):
        """Pantalla principal del usuario"""
        self.limpiar_pantalla()

        tk.Label(self.root, text=f"Bienvenido, {self.usuario_actual}", font=("Arial", 16, "bold"), bg="#f0f8ff", fg="#01579b").pack(pady=20)

        foto = self.usuarios[self.usuario_actual]["foto"]
        if os.path.exists(foto):
            tk.Label(self.root, text=f"Foto: {os.path.basename(foto)}", bg="#f0f8ff").pack(pady=5)

        tk.Button(self.root, text="Consultar Saldo", command=self.consultar_saldo, bg="#4caf50", fg="white", width=15).pack(pady=5)
        tk.Button(self.root, text="Depositar", command=self.depositar, bg="#2196f3", fg="white", width=15).pack(pady=5)
        tk.Button(self.root, text="Retirar", command=self.retirar, bg="#ff5722", fg="white", width=15).pack(pady=5)
        tk.Button(self.root, text="Historial", command=self.ver_historial, bg="#607d8b", fg="white", width=15).pack(pady=5)
        tk.Button(self.root, text="Cerrar Sesión", command=self.crear_pantalla_login, bg="#f44336", fg="white", width=15).pack(pady=20)

    def consultar_saldo(self):
        saldo = self.cuentas[self.usuario_actual]["saldo"]
        messagebox.showinfo("Saldo", f"Saldo disponible: ${saldo:.2f}")

    def depositar(self):
        try:
            monto = float(simpledialog.askstring("Depósito", "Ingrese el monto a depositar:"))
            if monto <= 0:
                messagebox.showerror("Error", "El monto debe ser positivo.")
                return
            self.cuentas[self.usuario_actual]["saldo"] += monto
            self.cuentas[self.usuario_actual]["transacciones"].append(f"Depósito: +${monto:.2f}")
            self.guardar_datos()
            self.consultar_saldo()
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto válido.")

    def retirar(self):
        try:
            monto = float(simpledialog.askstring("Retiro", "Ingrese el monto a retirar:"))
            if monto <= 0:
                messagebox.showerror("Error", "El monto debe ser positivo.")
                return
            if monto > self.cuentas[self.usuario_actual]["saldo"]:
                messagebox.showerror("Error", "Saldo insuficiente.")
                return
            self.cuentas[self.usuario_actual]["saldo"] -= monto
            self.cuentas[self.usuario_actual]["transacciones"].append(f"Retiro: -${monto:.2f}")
            self.guardar_datos()
            self.consultar_saldo()
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto válido.")

    def ver_historial(self):
        transacciones = self.cuentas[self.usuario_actual]["transacciones"]
        historial = "\n".join(transacciones) if transacciones else "Sin transacciones"
        messagebox.showinfo("Historial", historial)

    def guardar_datos(self):
        with open("usuarios.pkl", "wb") as f:
            pickle.dump(self.usuarios, f)
        with open("cuentas.pkl", "wb") as f:
            pickle.dump(self.cuentas, f)

    def cargar_datos(self):
        if os.path.exists("usuarios.pkl") and os.path.exists("cuentas.pkl"):
            with open("usuarios.pkl", "rb") as f:
                usuarios = pickle.load(f)
            with open("cuentas.pkl", "rb") as f:
                cuentas = pickle.load(f)
        else:
            usuarios, cuentas = {}, {}
        return usuarios, cuentas


if __name__ == "__main__":
    root = tk.Tk()
    app = BancoApp(root)
    root.mainloop()

