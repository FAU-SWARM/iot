from flask import Flask, request, jsonify

app = Flask(__name__)

db = [
    {
        'Temperature': 0,
        'Humidity': 0
    }
]

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/pi', methods=['POST'])
def pi():
	pi_data = request.get_json()
	db.append(pi_data)
	print('Value on server {}'.format(pi_data))
	return jsonify(pi_data)
	
@app.route('/pi/data')
def get_pi_data():
	return jsonify({'data': db})

if __name__ == '__main__':
	app.run(debug=True)
