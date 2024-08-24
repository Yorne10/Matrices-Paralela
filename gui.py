# gui.py

import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar
from database import create_connection, save_matrix, get_matrices

def save_matrix_to_db(matrix):
    conn = create_connection()
    save_matrix(conn, str(matrix))
    conn.close()
    messagebox.showinfo("Guardado", "Matriz guardada con éxito")

def show_saved_matrices():
    conn = create_connection()
    matrices = get_matrices(conn)
    conn.close()

    # nueva ventana para mostrar las matrices
    window = tk.Toplevel()
    window.title("Matrices Guardadas")

    scrollbar = Scrollbar(window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = Listbox(window, yscrollcommand=scrollbar.set, width=50, height=15)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    for matrix in matrices:
        listbox.insert(tk.END, f"ID {matrix[0]}: {matrix[1]}")

    scrollbar.config(command=listbox.yview)

def create_gui():
    root = tk.Tk()
    root.title("Ingreso de Matriz")

    # entrada de filas y columnas
    frame_input = tk.Frame(root, padx=10, pady=10)
    frame_input.pack(padx=20, pady=20)

    tk.Label(frame_input, text="Número de Filas:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    row_entry = tk.Entry(frame_input)
    row_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_input, text="Número de Columnas:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    col_entry = tk.Entry(frame_input)
    col_entry.grid(row=1, column=1, padx=5, pady=5)

    generate_button = tk.Button(frame_input, text="Generar Matriz", command=lambda: generate_matrix(row_entry, col_entry))
    generate_button.grid(row=2, column=0, columnspan=2, pady=10)

    # botones 
    frame_actions = tk.Frame(root, padx=10, pady=10)
    frame_actions.pack(padx=20, pady=10)

    show_button = tk.Button(frame_actions, text="Ver Matrices Guardadas", command=show_saved_matrices)
    show_button.grid(row=0, column=0, padx=5, pady=5)

    root.mainloop()

def generate_matrix(row_entry, col_entry):
    rows = int(row_entry.get())
    cols = int(col_entry.get())
    matrix = []

    # nueva ventana para los valores de la matriz
    window = tk.Toplevel()
    window.title("Ingresar Valores de la Matriz")

    for i in range(rows):
        for j in range(cols):
            tk.Label(window, text=f"Elemento ({i+1},{j+1}):").grid(row=i, column=j*2, padx=5, pady=5, sticky=tk.W)
            cell_value = tk.StringVar()
            entry = tk.Entry(window, textvariable=cell_value)
            entry.grid(row=i, column=j*2+1, padx=5, pady=5)
            matrix.append(cell_value)

    def save():
        matrix_values = [[cell.get() for cell in matrix[i*cols:(i+1)*cols]] for i in range(rows)]
        save_matrix_to_db(matrix_values)

    save_button = tk.Button(window, text="Guardar Matriz", command=save)
    save_button.grid(row=rows, column=0, columnspan=cols*2, pady=10)

if __name__ == '__main__':
    create_gui()

