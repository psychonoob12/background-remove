from flask import Flask, request, jsonify, send_file
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    # Vérifier si un fichier est présent dans la requête
    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier trouvé"}), 400

    file = request.files['file']

    # Lire l'image
    input_image = Image.open(file.stream)

    # Supprimer l'arrière-plan
    output_image = remove(input_image)

    # Convertir l'image en bytes
    img_byte_arr = io.BytesIO()
    output_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    # Renvoyer l'image sans arrière-plan
    return send_file(img_byte_arr, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)