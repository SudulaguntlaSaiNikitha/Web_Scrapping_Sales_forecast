from flask import Flask, jsonify, request
import csv

app = Flask(__name__)


# Function to read CSV data
def read_csv():
    data = []
    with open("dataaaa.csv", newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data


# Function to write CSV data
def write_csv(data):
    header = ["Brand", "Color",
              "Primary material", "Rating", "Seating height", "Top material",
              "Warranty", "Price", "Sales", "Height", "Weight", "Depth"]

    with open("dataaaa.csv", 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=header)
        csv_writer.writeheader()
        csv_writer.writerows(data)


# Endpoint to get all data or specific columns with conditions
@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        conditions = request.args.to_dict()
        if not conditions:
            data = read_csv()
        else:
            data = read_csv()
            data = [row for row in data if all(row[key] == value for key, value in conditions.items())]

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


# Endpoint to add new data
@app.route('/api/data', methods=['POST'])
def add_data():
    try:
        new_data = request.get_json()

        # Ensure new data has the required fields
        required_fields = ["Brand", "Color", "Primary material", "Rating", "Seating height", "Top material",
                           "Warranty", "Price", "Sales", "Height", "Weight", "Depth"]
        for field in required_fields:
            if field not in new_data:
                return jsonify({"error": f"Field '{field}' is required."}), 400

        current_data = read_csv()
        current_data.append(new_data)
        write_csv(current_data)

        return jsonify({"message": "Data added successfully."}), 201

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)