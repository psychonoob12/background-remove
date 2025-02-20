from flask import Flask, request, send_file
from rembg import remove
import os

app = Flask(__name__)

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'file' not in request.files:
        return "Aucun fichier téléchargé", 400

    file = request.files['file']
    input_path = "input_image.png"
    output_path = "output_image.png"

    # Sauvegarder l'image téléchargée
    file.save(input_path)

    # Supprimer l'arrière-plan
    with open(input_path, 'rb') as i:
        with open(output_path, 'wb') as o:
            input = i.read()
            output = remove(input)
            o.write(output)

    # Renvoyer l'image sans arrière-plan
    return send_file(output_path, mimetype='image/png')

if __name__ == '__main__':
    # Utiliser le port fourni par Render ou 5000 par défaut (local)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)