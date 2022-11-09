import json
import os

from flask import Flask, render_template, request, jsonify

import classifier
import config


def get_base_url(current_port):
    try:
        info = json.load(open(os.path.join(os.environ['HOME'], '.smc', 'info.json'), 'r'))
        project_id = info['project_id']
        url = f'/{project_id}/port/{current_port}/'
    except Exception as e:
        print(f'Server is probably running in production, so a base url does not apply: \n{e}')
        url = '/'
    return url


def get_prediction(req):
    try:
        file = req.files['image']
        filename = file.filename
        file_path = "".join([config.TEMP_FOLDER, filename])
        file.save(file_path)
        prediction = image_predictor.get_prediction_for_image(file_path)
        os.remove(file_path)
        return prediction
    except:
        return "Error"


port = 80  # or 443
base_url = get_base_url(port)

image_predictor = classifier.Classifier()

if base_url == '/':
    app = Flask(__name__)
else:
    app = Flask(__name__, static_url_path=base_url + 'static')


@app.route(f'{base_url}', methods=["GET", "POST"])
def home():
    output = get_prediction(request)
    return render_template('index.html', output=output)


@app.route(f'{base_url}/api', methods=["POST"])
def api():
    output = get_prediction(request)
    return jsonify(output)


if __name__ == '__main__':
    website_url = ''
    print(f'Try to open\n\n    https://{website_url}' + base_url + '\n\n')
    app.run(host='0.0.0.0', port=port, debug=True)
