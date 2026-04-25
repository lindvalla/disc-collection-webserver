# app.py
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Function to load data from the text file
def load_data(filepath="data.txt"):
    data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():  # Only process non-empty lines
                    data.append(line.strip().split(';'))
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
    all_items = load_data()
    filtered_items = []

    if query:
        for item in all_items:
            # Check if query is in any part of the item (e.g., any column)
            if any(query in col.lower() for col in item):
                filtered_items.append(item)
    else:
        # If no query, return all items
        filtered_items = all_items

    return jsonify(filtered_items)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')

