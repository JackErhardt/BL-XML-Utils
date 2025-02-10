from flask import Flask, request, render_template, jsonify
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_xml', methods=['POST'])
def process_xml():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    xml_file = request.files['file'].read()
    root = ET.fromstring(xml_file)
    
    return jsonify({'message': f'XML processed successfully! Root tag: {root.tag}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
