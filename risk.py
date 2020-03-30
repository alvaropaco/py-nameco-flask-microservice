# coding: utf-8

import os
import json
import sys
import datetime

from urllib import quote
from nameko.rpc import rpc, RpcProxy
from incoming import datatypes, PayloadValidator

RISK_LABELS = {0: "economic", 1: "regular", 2: "regular", 3: "responsible"}


def error(msg):
    """Return a Exception object

    This function is a reuse function to handle exceptions
    """
    raise Exception(msg)


def increment_eligible(eligible, fields, qty, result):
    for field in fields:
        if field in eligible:
            result[field] = result[field] + qty
    return result


def decrement_eligible(eligible, fields, qty, result):
    for field in fields:
        if field in eligible:
            result[field] = result[field] - qty
    return result


def remove_eligible(eligible, elig):
    for i in range(len(eligible) - 1):
        if eligible[i] == elig:
            eligible.pop(i)


def get_prediction(eligible, data):
    """Return a Risk prediction object

    This method returns a object containing the risk prediction in a scale from
    0 to 3 of auto, disability, home and life insurance.
    """
    result = {
        "auto": 3,
        "disability": 3,
        "home": 3,
        "life": 3
    }

    try:
        """If the user doesn t have income, vehicles or houses, she is
        ineligible for disability, auto, and home insurance, respectively."""
        income, vehicle, house = data["income"], data["vehicle"], data["house"]

        if income and vehicle and house is None:
            remove_eligible(eligible, "disability")
            remove_eligible(eligible, "auto")
            remove_eligible(eligible, "home")

        """If user is over 60 years old, she is ineligible for disability and
        life insurance"""
        age = data["age"]

        if age > 60:
            remove_eligible(eligible, "disability")
            remove_eligible(eligible, "life")

        """If the user is under 30 years old, deduct 2 risk points from all
        lines of insurance. If she is between 30 and 40 years old, deduct 1"""
        if age < 30:
            fields = ["auto", "disability", "home", "life"]
            result = decrement_eligible(eligible, fields, 2, result)
        elif 30 <= age <= 40:
            fields = ["auto", "disability", "home", "life"]
            result = decrement_eligible(eligible, fields, 1, result)

        """If her income is above $200k, deduct 1 risk point from all lines of
        insurance."""
        income = data["income"]

        if income > 200000:
            fields = ["auto", "disability", "home", "life"]
            result = decrement_eligible(eligible, fields, 1, result)

        """the user's house is mortgaged, add 1 risk point to her home score
        and add 1 risk point to her disability score."""
        house = data["house"]

        if house["ownership_status"] is "mortgaged":
            fields = ["home"]
            result = decrement_eligible(eligible, fields, 1, result)

        """If the user has dependents, add 1 risk point to both the disability
        and life scores."""
        dependents = data["dependents"]

        if dependents > 0:
            fields = ["disability", "life"]
            result = increment_eligible(eligible, fields, 1, result)

        """If the user is married, add 1 risk point to the life score and
        remove 1 risk point from disability."""
        marital_status = data["marital_status"]

        if marital_status == "married":
            fields = ["life"]
            result = increment_eligible(eligible, fields, 1, result)
            fields = ["disability"]
            result = decrement_eligible(eligible, fields, 1, result)

        """If user's vehicle was produced in the last 5 years, add 1 risk point
        to that vehicle’s score"""
        vehicle = data["vehicle"]

        current_year = int(datetime.datetime.now().year)

        if vehicle["year"] >= current_year - 5:
            fields = ["auto"]
            result = increment_eligible(eligible, fields, 1, result)

        return result
    except Exception as err:
        print(err)
        return {}


class PayloadValidation(PayloadValidator):
    required = False

    age = datatypes.Integer(required=True)
    dependents = datatypes.Integer(required=True)
    house = datatypes.Function('validate_house_ownership',
                               error=('House ownership year must be owned'
                                      ' or  married.'))
    income = datatypes.Integer(required=True)
    marital_status = datatypes.Function('validate_marital_status',
                                        error=('Marital status must be single'
                                               ' or  mortgaged.'),
                                        required=True)
    risk_questions = datatypes.Array(required=True)
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


def get_risk_label(risk_score):
    if risk_score > 3:
        risk_score = 3
    if risk_score < 0:
        risk_score = 0

    if risk_score in range(4):
        return RISK_LABELS[risk_score]
    else:
        error("Unknow")


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
        data = json.loads(payload)

        if data is None:
            error("Missing parameter")

        result, errors = PayloadValidation().validate(data)
        assert result and errors is None, error(errors)

        eligible = [
            "auto",
            "disability",
            "home",
            "life"
        ]

        predict_scores = get_prediction(eligible, data)

        result = {}

        for elig in eligible:
            result[elig] = get_risk_label(predict_scores[elig])

        return result
