import tkinter as tk
from tkinter import Toplevel, Label
import pygame
import random
from PIL import Image, ImageTk

# Lista de alienígenas e imagens (substitua pelos seus arquivos de imagem)
aliens = [
    {"name": "Quatro Braços", "image": "icones/quatro braços.png", "popup": "popup/quatro braços.png"},
    {"name": "Chama", "image": "icones/chama.png", "popup": "popup/chama.png"},
    {"name": "XLR8", "image": "icones/xlr8.png", "popup": "popup/xlr8.png"},
    {"name": "Diamante", "image": "icones/diamante.png", "popup": "popup/diamante.png"},
    {"name": "Fantasmático", "image": "icones/fantasmatico.png", "popup": "popup/fantasmatico.png"},
    {"name": "Bala de Canhão", "image": "icones/bala de canhão.png", "popup": "popup/bala de canhão.png"},
    {"name": "Aquático", "image": "icones/aquatico.png", "popup": "popup/aquatico.png"},
    {"name": "Insectóide", "image": "icones/insectoide.png", "popup": "popup/insectoide.png"},
    {"name": "Besta", "image": "icones/besta.png", "popup": "popup/besta.png"},
    {"name": "Massa Cinzenta", "image": "icones/massa cinzenta.png", "popup": "popup/massa cinzenta.png"},
    {"name": "Ultra T", "image": "icones/ultra t.png", "popup": "popup/ultra t.png"},
    {"name": "LobisBen", "image": "icones/lobisben.png", "popup": "popup/lobisben.png"},
    {"name": "Cipo Selvagem", "image": "icones/wildvine.png", "popup": "popup/wildvine.png"},
    {"name": "Ben Vicktor", "image": "icones/benvictor.png", "popup": "popup/benvictor.png"},
    {"name": "Ben Mumia", "image": "icones/benmumia.png", "popup": "popup/benmumia.png"},
    {"name": "Glutão", "image": "icones/glutao.png", "popup": "popup/glutao.png"},
    {"name": "Ditto", "image": "icones/ditto.png", "popup": "popup/ditto.png"},
    {"name": "Sandboks", "image": "icones/sandboks.png", "popup": "popup/Sandboks.png"},
    {"name": "Mega Olhos", "image": "icones/mega olhos.png", "popup": "popup/mega olhos.png"},
    {"name": "Gigante", "image": "icones/waybig.png", "popup": "popup/waybig.png"}
]

spin_sounds = [
    "sounds/spin1.mp3",
    "sounds/spin2.mp3",
    "sounds/spin3.mp3",
    "sounds/spin4.mp3",
    "sounds/spin5.mp3",
    "sounds/spin6.mp3",
    "sounds/spin7.mp3",
    "sounds/spin8.mp3",
    "sounds/spin9.mp3",
    "sounds/spin10.mp3",
    "sounds/spin11.mp3",
    "sounds/spin12.mp3",
    "sounds/spin13.mp3"
]

pygame.mixer.init()
transformation_sound = pygame.mixer.Sound("sounds/omnitrix-transform.mp3")

class OmnitrixSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Omnitrix Simulator")
        self.root.iconbitmap("icones/icon.ico")

        self.selected_alien_index = 0
        self.current_angle = 0  # Ângulo inicial do disco
        
        # Carregar a imagem base do Omnitrix (base fixa)
        self.base_image = Image.open("omnitrix/omnitrix_base.png")  # Imagem da base do Omnitrix
        self.base_image = self.base_image.resize((300, 300), Image.Resampling.LANCZOS)

        # Carregar a imagem do disco (que será rotacionada)
        self.disc_image = Image.open("omnitrix/omnitrix_disc.png")  # Imagem separada do disco
        self.disc_image = self.disc_image.resize((140, 140), Image.Resampling.LANCZOS)

        # Carregar as imagens dos alienígenas
        self.load_images()

        # Canvas para mostrar o Omnitrix e o alien selecionado
        self.canvas = tk.Canvas(root, width=300, height=300)
        self.canvas.pack(pady=0)

        # Bind para clique no disco
        self.canvas.bind("<Button-1>", self.on_click)  # Vincula o clique esquerdo ao disco

        # Mostrar a imagem inicial do Omnitrix com o disco
        self.show_disc(self.current_angle)

    def load_images(self):
        self.alien_images = []
        for alien in aliens:
            image = Image.open(alien["image"])
            image = image.resize((50, 50), Image.Resampling.LANCZOS)  # Redimensiona a imagem do alien
            self.alien_images.append(ImageTk.PhotoImage(image))
        
    def show_disc(self, angle):
        # Girar o disco e colocar a imagem do alien no centro
        rotated_disc = self.disc_image.rotate(angle, resample=Image.Resampling.BICUBIC)

        # Inserir a imagem do alien no centro do disco
        alien_image = Image.open(aliens[self.selected_alien_index]['image']).resize((50, 50), Image.Resampling.LANCZOS)
        rotated_disc.paste(alien_image, (43, 43), alien_image)

        # Atualizar o canvas com a combinação da base e do disco
        self.update_canvas(rotated_disc)
    
    def update_canvas(self, rotated_disc):
        # Combinar a imagem da base com o disco rotacionado
        final_image = self.base_image.copy()
        final_image.paste(rotated_disc, (52, 52), rotated_disc)  # Posicionar o disco central na base

        # Atualizar o canvas com a nova imagem combinada
        self.combined_image_tk = ImageTk.PhotoImage(final_image)
        self.canvas.create_image(150, 150, image=self.combined_image_tk)

    def on_click(self, event):
        """colocando uma inputbox no disco"""
        # Coordenadas do centro do disco (ajustadas para a nova posição)
        disc_center_x = 117  # 52 + metade da largura do disco
        disc_center_y = 117  # 52 + metade da altura do disco
        disc_radius = 70  # Raio do disco (metade da largura da imagem do disco)

        # Calcular a distância do clique até o centro do disco
        dist_x = event.x - disc_center_x
        dist_y = event.y - disc_center_y
        distance = (dist_x ** 2 + dist_y ** 2) ** 0.5

        if distance <= disc_radius:
            # Se o clique estiver dentro do disco, definir ação
            if event.x < disc_center_x - 40:  # Clique à esquerda
                self.spin_left()
            elif event.x > disc_center_x + 40:  # Clique à direita
                self.spin_right()
            else:  # Clique no centro do disco
                self.transform()

    
    def animate_spin(self, target_angle):
        """Anima o giro do disco em pequenos incrementos até o ângulo desejado."""
        # Calcular a diferença de ângulo restante
        delta_angle = (target_angle - self.current_angle) % 360
        
        # Decidir a direção (se a diferença é maior que 180 graus, invertemos a rotação)
        if delta_angle > 180:
            delta_angle -= 360
        
        # Definir o passo da rotação
        step = 5 if delta_angle > 0 else -5

        # Atualizar o ângulo atual
        self.current_angle = (self.current_angle + step) % 360
        self.show_disc(self.current_angle)
        
        # Continuar a animação enquanto o disco não chegar ao ângulo alvo
        if abs(delta_angle) > abs(step):
            self.root.after(15, self.animate_spin, target_angle)
        else:
            # Garantir que o ângulo final seja exato
            self.current_angle = target_angle % 360
            self.show_disc(self.current_angle)

    def play_random_sound(self):
        # Escolhe um som aleatoriamente da lista
        selected_sound = random.choice(spin_sounds)
        
        # Carrega e toca o som selecionado
        spin_sound = pygame.mixer.Sound(selected_sound)
        spin_sound.play()

    def spin_left(self):
        # Calcular o novo ângulo alvo (45 graus para a esquerda)
        target_angle = (self.current_angle + 45) % 360
        self.selected_alien_index = (self.selected_alien_index - 1) % len(aliens)
        self.animate_spin(target_angle)
        self.play_random_sound()

    def spin_right(self):
        # Calcular o novo ângulo alvo (45 graus para a direita)
        target_angle = (self.current_angle - 45) % 360
        self.selected_alien_index = (self.selected_alien_index + 1) % len(aliens)
        self.animate_spin(target_angle)
        self.play_random_sound()

    
    def transform(self):
        selected_alien = aliens[self.selected_alien_index]["name"]
        image_path = aliens[self.selected_alien_index]["popup"]
        transformation_sound.play()
        
        # Cria uma nova janela sem som
        top = Toplevel(self.root)
        top.title("Transformação")
        top.iconbitmap("icones/icon.ico")

        # Carregar e exibir a imagem
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        
        # Cria um label para a imagem
        image_label = Label(top, image=photo)
        image_label.image = photo  # Manter uma referência à imagem
        image_label.pack()
        
        # Cria um label para o texto
        text_label = Label(top, text=f"Você se transformou no {selected_alien}!")
        text_label.pack()

        # Adiciona um botão para fechar a janela
        close_button = tk.Button(top, text="Ebaa!!", command=top.destroy)
        close_button.pack()

# Inicializa a janela principal
root = tk.Tk()
app = OmnitrixSimulator(root)
root.mainloop()
