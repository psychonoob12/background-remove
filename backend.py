from flask import Flask, request, send_file, jsonify
from rembg import remove
from PIL import Image
import io
import os

# Initialise l'application Flask
app = Flask(__name__)

# Limite la taille des fichiers uploadés (par exemple, 5MB)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB

# Endpoint pour vérifier que l'API est en ligne
@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'OK',
        'message': 'API de suppression d\'arrière-plan est en ligne !',
        'endpoint': '/remove-bg (POST)'
    }), 200

# Endpoint pour supprimer l'arrière-plan d'une image
@app.route('/remove-bg', methods=['POST'])
def remove_background():
    # Vérifie si une image est présente dans la requête
    if 'image' not in request.files:
        return jsonify({'error': 'Aucune image envoyée. Utilisez le champ "image".'}), 400
    
    file = request.files['image']
    
    # Vérifie que le fichier n'est pas vide
    if file.filename == '':
        return jsonify({'error': 'Fichier vide.'}), 400
    
    # Vérifie le type de fichier (optionnel)
    if not file.mimetype.startswith('image/'):
        return jsonify({'error': 'Le fichier doit être une image.'}), 415
    
    try:
        # Ouvre l'image avec Pillow
        input_image = Image.open(file.stream)
        
        # Convertit en RGBA si nécessaire (pour transparence)
        if input_image.mode != 'RGBA':
            input_image = input_image.convert('RGBA')
        
        # Supprime l'arrière-plan avec rembg
        output_image = remove(input_image)
        
        # Sauvegarde l'image en mémoire
        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)
        
        # Renvoie l'image traitée
        return send_file(
            img_io,
            mimetype='image/png',
            as_attachment=True,
            download_name='image-sans-fond.png'
        )
    
    except Exception as e:
        return jsonify({'error': f'Erreur lors du traitement : {str(e)}'}), 500

# Gestion des erreurs pour la limite de taille
@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': 'Fichier trop volumineux. Limite : 5MB.'}), 413

if __name__ == '__main__':
    # Pour tester localement
    app.run(debug=True, host='0.0.0.0', port=5000)