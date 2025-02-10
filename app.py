from flask import Flask, request, render_template, jsonify
import xml.etree.ElementTree as ET
from collections import defaultdict

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

    def extract_items(root):
        items_dict = defaultdict(int)  # Dictionary to store items with counts
        for item in root.findall("ITEM"):
            item_id = item.find("ITEMID").text
            color = item.find("COLOR").text
            min_qty = int(item.find("MINQTY").text)
            key = (item_id, color)  # Unique identifier for comparison
            items_dict[key] += min_qty  # Accumulate MINQTY count
        return items_dict

    # Extract items from both XMLs
    items1 = extract_items(root1)
    items2 = extract_items(root2)

    common_items = {}
    unique_to_1 = {}
    unique_to_2 = {}

    for key in set(items1.keys()).union(items2.keys()):
        qty1 = items1.get(key, 0)
        qty2 = items2.get(key, 0)

        if qty1 > 0 and qty2 > 0:
            common_qty = min(qty1, qty2)
            common_items[key] = common_qty
            if qty1 > common_qty:
                unique_to_1[key] = qty1 - common_qty
            if qty2 > common_qty:
                unique_to_2[key] = qty2 - common_qty
        elif qty1 > 0:
            unique_to_1[key] = qty1
        elif qty2 > 0:
            unique_to_2[key] = qty2

    def format_items(items):
        return [
            {"ITEMID": key[0], "COLOR": key[1], "MINQTY": qty}
            for key, qty in items.items()
        ]

    return jsonify({
        'message': 'Comparison complete!',
        'common_items': format_items(common_items),
        'unique_to_1': format_items(unique_to_1),
        'unique_to_2': format_items(unique_to_2)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
