from flask import Flask, request, send_file
from rembg import remove
import os
import logging

app = Flask(__name__)

# Configurer les logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'file' not in request.files:
        return "Aucun fichier téléchargé", 400

    file = request.files['file']
    input_path = "input_image.png"
    output_path = "output_image.png"

    file.save(input_path)
    with open(input_path, 'rb') as i:
        with open(output_path, 'wb') as o:
            input = i.read()
            output = remove(input)
            o.write(output)

    return send_file(output_path, mimetype='image/png')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Démarrage de l'application sur le port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
else:
    # Quand Gunicorn est utilisé, loguer le port
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Gunicorn démarré, écoute sur 0.0.0.0:{port}")