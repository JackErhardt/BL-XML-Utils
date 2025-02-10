from flask import Flask, request, render_template, jsonify
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_xml', methods=['POST'])
def process_xml():
    if 'file1' not in request.files or 'file2' not in request.files:
        return jsonify({'error': 'Both files must be uploaded'}), 400

    xml_file1 = request.files['file1'].read()
    xml_file2 = request.files['file2'].read()

    try:
        root1 = ET.fromstring(xml_file1)
        root2 = ET.fromstring(xml_file2)
    except ET.ParseError:
        return jsonify({'error': 'Invalid XML format'}), 400

    return jsonify({
        'message': 'XML files processed successfully!',
        'root_tag_file1': root1.tag,
        'root_tag_file2': root2.tag
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
