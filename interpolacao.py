import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import numpy as np
from PIL import Image, ImageTk, UnidentifiedImageError
from Class_vizinho import VizinhoMaisProximo
from Class_bilinear import Bilinear

class InterpolationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interpolação de Imagens")
        
        self.image_path = None
        self.original_image = None  # PIL Image (grayscale)
        self.processed_image = None
        
        self.create_widgets()
        self.toggle_controls(False)
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Controles de imagem
        ttk.Button(main_frame, text="Importar Imagem", command=self.load_image).grid(row=0, column=0, pady=5)
        
        # Comboboxes
        self.method_var = tk.StringVar()
        self.scale_type_var = tk.StringVar()
        
        ttk.Label(main_frame, text="Método:").grid(row=1, column=0, sticky="w")
        self.method_combo = ttk.Combobox(main_frame, textvariable=self.method_var, 
                                       values=["Vizinho Mais Próximo", "Bilinear"], state="readonly")
        self.method_combo.grid(row=2, column=0, pady=5)
        
        ttk.Label(main_frame, text="Escala:").grid(row=3, column=0, sticky="w")
        self.scale_combo = ttk.Combobox(main_frame, textvariable=self.scale_type_var, 
                                      values=["ampliação (2x)", "redução (0.5x)"], state="readonly")
        self.scale_combo.grid(row=4, column=0, pady=5)
        
        # Botões
        self.process_button = ttk.Button(main_frame, text="Aplicar Interpolação", 
                                       command=self.apply_interpolation, state="disabled")
        self.process_button.grid(row=5, column=0, pady=5)
        
        
        # Área de visualização
        self.original_label = ttk.Label(main_frame, text="Nenhuma imagem carregada")
        self.original_label.grid(row=0, column=1, rowspan=7, padx=10)
        
        self.processed_label = ttk.Label(main_frame, text="Resultado aparecerá aqui")
        self.processed_label.grid(row=0, column=2, rowspan=7, padx=10)
        
        # Labels de tamanho
        self.original_size = ttk.Label(main_frame, text="Tamanho: -")
        self.original_size.grid(row=7, column=1, sticky="n", pady=5)
        
        self.processed_size = ttk.Label(main_frame, text="Tamanho: -")
        self.processed_size.grid(row=7, column=2, sticky="n", pady=5)

    def toggle_controls(self, enable=True):
        state = "normal" if enable else "disabled"
        self.method_combo.configure(state=state)
        self.scale_combo.configure(state=state)
        self.process_button.configure(state=state)

    def load_image(self):
        try:
            self.image_path = filedialog.askopenfilename(
                filetypes=[("Imagens", "*.jpg *.jpeg *.png *.bmp")]
            )
            if not self.image_path:
                return

            self.original_image = Image.open(self.image_path).convert("L")
            self.show_image(self.original_image, self.original_label)
            self.toggle_controls(True)
            self.clear_processed()
            self.update_size_labels()

        except UnidentifiedImageError:
            messagebox.showerror("Erro", "Formato de imagem não suportado ou arquivo corrompido")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar imagem:\n{str(e)}")

    def update_size_labels(self):
        if self.original_image:
            w, h = self.original_image.size
            self.original_size.config(text=f"Original: {w}x{h}")
        else:
            self.original_size.config(text="Original: -")
            
        if self.processed_image:
            w, h = self.processed_image.size
            self.processed_size.config(text=f"Processada: {w}x{h}")
        else:
            self.processed_size.config(text="Processada: -")

    def apply_interpolation(self):
        try:
            validation_errors = self.validate_inputs()
            if validation_errors:
                messagebox.showerror("Erro de Validação", "\n".join(validation_errors))
                return

            original_array = np.array(self.original_image, dtype=np.uint8)
            
            if self.method_var.get() == "Vizinho Mais Próximo":
                interpolator = VizinhoMaisProximo(original_array)
            else:
                interpolator = Bilinear(original_array)
            
            if "ampliação" in self.scale_type_var.get():
                processed_array = interpolator.ampliar()
            else:
                processed_array = interpolator.reduzir()
            
            self.processed_image = Image.fromarray(processed_array)
            self.show_image(self.processed_image, self.processed_label)
            self.update_size_labels()

        except IndexError as e:
            messagebox.showerror("Erro", f"Problema nos índices da matriz:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao processar imagem:\n{str(e)}")
            self.clear_processed()

    def show_image(self, image, label):
        try:
            width, height = image.size
            ratio = min(300/width, 300/height)
            display_size = (int(width*ratio), int(height*ratio))
            
            display_image = image.resize(display_size, Image.NEAREST)
            photo = ImageTk.PhotoImage(display_image)
            
            label.configure(image=photo, text="")
            label.image = photo
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao exibir imagem:\n{str(e)}")
            label.configure(image=None, text="Erro na visualização")

    def validate_inputs(self):
        errors = []
        if not self.method_var.get():
            errors.append("Selecione um método de interpolação")
        if not self.scale_type_var.get():
            errors.append("Selecione o tipo de escala")
        return errors

    def clear_processed(self):
        self.processed_label.configure(image=None, text="Resultado aparecerá aqui")
        self.processed_image = None
        self.update_size_labels()

if __name__ == "__main__":
    root = tk.Tk()
    app = InterpolationApp(root)
    root.mainloop()