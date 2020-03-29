import os
import json
import sys

from urllib import quote
from nameko.rpc import rpc, RpcProxy
from incoming import datatypes, PayloadValidator

RISK_LABELS = { 0: "economic", 1: "regular", 2: "regular", 3: "responsible" }

def error(msg):
    """Return a Exception object

    This function is a reuse function to handle exceptions
    """
    raise Exception(msg)

# def get_disability_risk(payload):
    

def get_prediction(payload):
    """Return a Weather object

    This call consumes the open Weather Map API to retreive the weather
    information about some geographi coordinate or city name.
    """

    result = { }

    # disability = get_disability_risk(payload)

    return result

def get_risk_label(risk_score):
    if risk_score in range(3):
        return RISK_LABELS[risk_score]
    else:
        error("Unknow")

class PayloadValidation(PayloadValidator):

    age = datatypes.Integer()
    dependents = datatypes.Integer()
    house = datatypes.Function('validate_house_ownership',
                                      error=('House ownership year must be owned'
                                             ' or  married.'))
    income = datatypes.Integer()
    marital_status = datatypes.Function('validate_marital_status',
                                      error=('Marital status must be single'
                                             ' or  mortgaged.'))
    risk_questions = datatypes.Array()
    vehicle = datatypes.Function('validate_vehicle_year',
                                      error=('Marital status must be an Integer'))

    @staticmethod
    def validate_house_ownership(val, *args, **kwargs):
        if val["ownership_status"] in ['owned', 'mortgaged']:
            return True
        else:
            return False

    @staticmethod
    def validate_marital_status(val, *args, **kwargs):
        if val in ['single', 'married']:
            return True
        else:
            return False
    
    @staticmethod
    def validate_vehicle_year(val, *args, **kwargs):
        if isinstance(val["year"], int):
            return True
        else:
            False

class RiskService:
    """Risk Service

    Returns:
        object: (dict): A Dict (auto, disability, home, life,
    """

    name = "risk"

    zipcode_rpc = RpcProxy('risksservice')

    @rpc
    def predict(self, payload):
        """[summary]

        Arguments:
            payload  (dict): A Dict (age, dependents, house, income,
            marital_status, risk_questions, vehicle)

        Returns:
            object: (dict): A Dict (auto, disability, home, life)
        """
        try:
            data = json.loads(payload)
            # Check if is passed args
            if data is None:
                error("Missing parameter")

            result, errors = PayloadValidation().validate(data)
            assert result and errors is None, error(json.dumps(errors, indent=2))

            predict = get_prediction(data)

            return predict
        except Exception as e:
            return str({'Error': str(e)})
