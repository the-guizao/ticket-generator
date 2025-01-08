from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

def generate_tickets(image_path, output_dir, font_path, start_num=1, end_num=400):
    # Carregar a imagem do ingresso
    ticket_image = Image.open(image_path)
    width, height = ticket_image.size

    # Fonte para os números e o superscript
    font = ImageFont.truetype(font_path, 40)  # Tamanho da fonte principal
    font_superscript = ImageFont.truetype(font_path, 30)  # Tamanho menor para o superscript
    color = "#ffe1be"  # Cor desejada

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Criar os ingressos numerados
    for i in range(start_num, end_num + 1):
        img_copy = ticket_image.copy()
        draw = ImageDraw.Draw(img_copy)

        text_main = f"ASSENTO N"  # Parte principal do texto
        text_number = str(i)  # O número do assento

        text_image = Image.new('RGBA', (600, 400), (255, 255, 255, 0))  # Criação de uma imagem para o texto
        text_draw = ImageDraw.Draw(text_image)

        text_draw.text((0, 0), text_main, font=font, fill=color)

        text_draw.text((240, -10), "o", font=font_superscript, fill=color)

        text_draw.text((255, 0), f". {text_number}", font=font, fill=color)

        text_image = text_image.rotate(90, expand=1)

        position = (width - 150, height // 2 -400) 

        img_copy.paste(text_image, position, text_image)

        img_copy.save(f"{output_dir}/ticket_{i}.png")

def create_pdf(output_pdf, image_dir, image_path, start_num=1, end_num=400):
    c = canvas.Canvas(output_pdf, pagesize=A4)
    a4_width, a4_height = A4

    # Carregar a imagem do ingresso para obter suas dimensões originais
    ticket_image = Image.open(image_path)
    ticket_width, ticket_height = ticket_image.size

    # Calcular a altura de cada ingresso, mantendo a proporção
    scale_factor = a4_width / ticket_width
    scaled_ticket_width = a4_width
    scaled_ticket_height = ticket_height * scale_factor

    for i in range(start_num, end_num + 1, 4):
        # Para cada página, inserimos 3 ingressos
        y_offset = a4_height - scaled_ticket_height  # Começa a desenhar do topo

        for j in range(4):
            ticket_num = i + j
            if ticket_num > end_num:
                break
            # Carregar o ingresso numerado
            ticket_path = f"{image_dir}/ticket_{ticket_num}.png"
            if os.path.exists(ticket_path):
                c.drawImage(ticket_path, 0, y_offset, scaled_ticket_width, scaled_ticket_height)
            y_offset -= scaled_ticket_height + 15

        c.showPage()  # Criar nova página após 3 ingressos

    c.save()

# Caminhos dos arquivos
image_path = "modelo_ingresso.png"  # Caminho da imagem do ingresso
output_dir = "ingressos_numerados"
font_path = "Montserrat-Regular.ttf"  # Fonte TTF para os números
output_pdf = "ingressos_numerados.pdf"

# Gerar ingressos numerados de 1 a 400
generate_tickets(image_path, output_dir, font_path, start_num=1, end_num=416)

# Criar PDF com ingressos 3 por página, mantendo a proporção
create_pdf(output_pdf, output_dir, image_path, start_num=1, end_num=416)
