from flask import Flask, request, send_file
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

# Définit la taille maximale du fichier à 5MB (5 * 1024 * 1024 octets)
MAX_FILE_SIZE = 5 * 1024 * 1024

# Route principale qui affiche un message de bienvenue
@app.route('/')
def index():
    return "Welcome to the Background Removal API! Use /remove-bg to upload an image."

# Route pour uploader et traiter l'image
@app.route('/remove-bg', methods=['POST'])
def remove_background():
    # Vérifie si une image a été uploadée
    if 'image' not in request.files:
        return "No image uploaded.", 400
    
    file = request.files['image']
    
    # Vérifie la taille du fichier
    file.seek(0, io.SEEK_END)
    file_size = file.tell()
    if file_size > MAX_FILE_SIZE:
        return f"File too large. Maximum size allowed is {MAX_FILE_SIZE / (1024 * 1024)}MB.", 413
    
    # Remet le curseur au début du fichier et ouvre l'image
    file.seek(0)
    input_image = Image.open(file.stream).convert("RGBA")
    
    # Supprime l'arrière-plan avec rembg
    output_image = remove(input_image)
    
    # Sauvegarde l'image en mémoire (pas sur disque)
    img_io = io.BytesIO()
    output_image.save(img_io, 'PNG')
    img_io.seek(0)
    
    # Envoie l'image traitée au client
    return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='image_without_background.png')

# Démarre l'application en mode debug si exécutée directement
if __name__ == '__main__':
    app.run(debug=True)