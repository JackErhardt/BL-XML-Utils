from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/')
def home():
    return "XML Processing Service is running!"

@app.route('/process_xml', methods=['POST'])
def process_xml():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    xml_file = request.files['file'].read()
    root = ET.fromstring(xml_file)
    
    # Modify XML here (example: return root tag)
    return jsonify({'message': 'XML processed successfully', 'root_tag': root.tag})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)  # Render uses port 10000
