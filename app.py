from flask import Flask, request, render_template, jsonify
import xml.etree.ElementTree as ET
import xml.dom.minidom
from collections import defaultdict

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def extract_items(root):
    items_dict = defaultdict(int)
    for item in root.findall("ITEM"):
        item_type = item.find("ITEMTYPE").text
        item_id = item.find("ITEMID").text
        color = item.find('COLOR').text if item.find('COLOR') is not None else None
        min_qty = int(item.find("MINQTY").text)
        key = (item_type, item_id, color)
        if key not in items_dict :
            items_dict[key] += min_qty
        items_dict[key] += min_qty
    return items_dict

def compare_xml(items1, items2):
    common_items = {}
    unique_to_xml1 = {}
    unique_to_xml2 = {}

    for key in set(items1.keys()).union(items2.keys()):
        qty1 = items1.get(key, 0)
        qty2 = items2.get(key, 0)

        if qty1 > 0 and qty2 > 0:
            common_qty = min(qty1, qty2)
            common_items[key] = common_qty
            if qty1 > common_qty:
                unique_to_xml1[key] = qty1 - common_qty
            if qty2 > common_qty:
                unique_to_xml2[key] = qty2 - common_qty
        elif qty1 > 0:
            unique_to_xml1[key] = qty1
        elif qty2 > 0:
            unique_to_xml2[key] = qty2

    return common_items, unique_to_xml1, unique_to_xml2

def create_xml_string(items):
    root = ET.Element("INVENTORY")
    for key, qty in items.items():
        item = ET.SubElement(root, "ITEM")
        ET.SubElement(item, "ITEMTYPE").text = key[0]
        ET.SubElement(item, "ITEMID").text = key[1]
        if key[2] is not None :
            ET.SubElement(item, "COLOR").text = key[2]
        ET.SubElement(item, "MINQTY").text = str(qty)
    
    raw_xml = ET.tostring(root, encoding='unicode')
    parsed_xml = xml.dom.minidom.parseString(raw_xml)
    pretty_xml = parsed_xml.toprettyxml(indent="  ")
    return pretty_xml

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

    items1 = extract_items(root1)
    items2 = extract_items(root2)

    common_items, unique_to_xml1, unique_to_xml2 = compare_xml(items1, items2)

    return jsonify({
        'message': 'Comparison complete!',
        'common_items_xml': create_xml_string(common_items),
        'unique_to_1_xml': create_xml_string(unique_to_xml1),
        'unique_to_2_xml': create_xml_string(unique_to_xml2)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    # app.run(debug=True)  # Enables auto-reloading on file changes