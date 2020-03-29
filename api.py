from flask import Flask, request, jsonify
from nameko.standalone.rpc import ClusterRpcProxy

CONFIG = {'AMQP_URI': "amqp://guest:guest@localhost:5672"}
app = Flask(__name__)


@app.route('/insurance/risk', methods=['POST'])
def insurance():
    """
    Micro Service to predict an insurance risk score
    This API is made with Flask and Nameko
    ---
    parameters:
      - name: age
        in: body
        required: true
        schema:
          type: integer
        description: Age of the User
      - name: dependents
        in: body
        required: true
        schema:
          type: integer
        description: Number of dependents
      - name: house
        in: body
        required: true
        schema:
          type: object
        description: House representation with ownnership status
      - name: income
        in: body
        required: true
        schema:
          type: integer
        description: Income
      - name: marital_status
        in: body
        required: true
        schema:
          type: integer
        description: Marital status like single or mmarried
      - name: risk_questions
        in: body
        required: true
        schema:
          type: array
        description: A collection with questions response
      - name: vehicel
        in: body
        required: true
        schema:
          type: object
        description: Vehicle object with manufactory year 
    responses:
      200:
        description: Location data
    """
    with ClusterRpcProxy(CONFIG) as rpc:
        # Consuming Nameko service
        try:
          result = rpc.risk.predict(request.data)
          return jsonify(result), 200
        except Exception as err:
          return jsonify(err), 500


if __name__ == "__main__":
    """Start Flask app to serve mircoservices"""
    app.run(host='0.0.0.0')
