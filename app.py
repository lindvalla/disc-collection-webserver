from xml_to_data import backup_then_parse

# app.py
from flask import Flask, render_template, request, jsonify


app = Flask(__name__)

IMAGE_FILES = [
    'DVD_video_logo_20px.png',
    'Blu_ray_logo_20px.png',
    'UHD_Blu-ray_logo_20px.png'
]
SOURCES = [ f'<img src="/static/{fname}"/>' for fname in IMAGE_FILES ]

# Function to load data from the text file
def load_data(filepath="data.txt"):
    data = []
    try:
#        with open(filepath, 'r', encoding='utf-8') as f:
        with open(filepath, 'r', encoding='iso-8859-1') as f:
            for line in f:
                if line.strip():  # Only process non-empty lines
                    #data.append(line.strip().split(';'))
                    a = line.strip().split(';')
                    #print("a=", a)
                    b = a[1:4]
                    #print("b=", b)
                    s = ' '.join([ SOURCES[idx] for idx,val in enumerate(b) if val.lower()=='true' ]).strip()
                    #print("s=", s)
                    c = [ a[0], s ]
                    c.extend(a[4:])
                    #print("c=", c)
                    data.append(c)
                    #break
    except FileNotFoundError:
        print(f"Warning: data.txt not found at {filepath}. Please create it.")
    return data

@app.route('/')
def index():
    # Load data initially when the page is requested
    items = load_data()
    return render_template('index.html', items=items)


@app.route('/search', methods=['GET'])
def search_data():
    query = request.args.get('query', '').lower()
    #onlyhavedvd = request.args.get('hidedvd', 'false').lower()=='false'
    #includebluray = request.args.get('hidebluray', 'false').lower()=='false'
    #include4k = request.args.get('hide4k', 'false').lower()=='false'
    all_items = load_data()
    filtered_items = []

    if query:
        for item in all_items:
            # Check if query is in any part of the item (e.g., any column)
            if any(query in col.lower() for col in item):
                #if onlyhavedvd:
                #    if not (bool(item[2]) or bool(item[3])):
                #        filtered_items.append(item)
                #else:
                #    filtered_items.append(item)
                filtered_items.append(item)
    else:
        # If no query, return all items
        filtered_items = all_items

    return jsonify(filtered_items)


@app.route('/upload',  methods=['POST'])
def upload_file():
    # Check if file is part of the request
    if 'data_file' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400

    file = request.files['data_file']

    if file.filename == '':
        return jsonify({'message': 'No file selected'}), 400

    try:
        # --- YOUR PARSING LOGIC HERE ---
        # Example: Read text file contents
        backup_then_parse(file)

        #file_contents = file.read().decode('utf-8')

        # Simulate a parsing failure condition if needed
        #if "invalid" in file_contents:
        #    raise ValueError("Invalid data format detected inside file.")

        # Save data or update your database here
        # ---------------------------------

        return jsonify({'message': 'File parsed and data updated successfully!'}), 200

    except Exception as e:
        # Return the specific parsing error message to the frontend
        return jsonify({'message': f'Failed to parse file. Error: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
    #load_data()

