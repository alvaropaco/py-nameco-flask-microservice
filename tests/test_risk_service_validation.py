# -*- coding: utf-8 -*-
import unittest
import requests
import json
import os

from ..api import app


class RiskTestCase(unittest.TestCase):
    """This class represents the Weather test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        #  Setting parameters to Flask app
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False

        # Setting test client
        self.app = app.test_client()
        self.app.testing = True

        # Check configurations
        self.assertEqual(app.debug, False)

    def test_insurance_without_age(self):
        """Test to get Insurance risk"""

        url = 'http://127.0.0.1:5000/insurance/risk'

        data = {
            "dependents": 2,
            "house": {"ownership_status": "owned"},
            "income": 0,
            "marital_status": "married",
            "risk_questions": [0, 1, 0],
            "vehicle": {"year": 2018}
        }

        res = self.app.post(
            url,
            data=json.dumps(data))

        jsonObj = json.loads(res.data)

        assert res.status == '200 OK'
        assert jsonObj == """Exception {'age': ['Expecting a value for this
            field.']}"""

    def test_insurance_dependents_integer(self):
        """Test to get Insurance risk"""

        url = 'http://127.0.0.1:5000/insurance/risk'

        data = {
            "age": 30,
            "dependents": "ksajdhlkasd",
            "house": {"ownership_status": "owned"},
            "income": 0,
            "marital_status": "married",
            "risk_questions": [0, 1, 0],
            "vehicle": {"year": 2018}
        }

        res = self.app.post(
            url,
            data=json.dumps(data))

        jsonObj = json.loads(res.data)

        assert res.status == '200 OK'
        assert jsonObj == """Exception {u'dependents': ['Invalid data. Expected
            an integer.']}"""

    def test_insurance_wrong_ownership_status(self):
        """Test to get Insurance risk with wrong ownership_status"""

        url = 'http://127.0.0.1:5000/insurance/risk'

        data = {
            "age": 30,
            "dependents": 2,
            "house": {"ownership_status": "test"},
            "income": 0,
            "marital_status": "married",
            "risk_questions": [0, 1, 0],
            "vehicle": {"year": 2018}
        }

        res = self.app.post(
            url,
            data=json.dumps(data))

        jsonObj = json.loads(res.data)

        assert res.status == '200 OK'
        assert jsonObj == """Exception {u'house': ['House ownership year must
        be owned or  married.']}"""

    def test_insurance_marital_status(self):
        """Test to get Insurance risk with wrong Marital status"""

        url = 'http://127.0.0.1:5000/insurance/risk'

        data = {
            "age": 30,
            "dependents": 2,
            "house": {"ownership_status": "owned"},
            "income": 0,
            "marital_status": "x",
            "risk_questions": [0, 1, 0],
            "vehicle": {"year": 2018}
        }

        res = self.app.post(
            url,
            data=json.dumps(data))

        jsonObj = json.loads(res.data)

        assert res.status == '200 OK'
        assert jsonObj == """Exception {u'marital_status': ['Marital status must
        be single or  mortgaged.']}"""

    def test_insurance_without_risk_questions(self):
        """Test to get Insurance risk without questions"""

        url = 'http://127.0.0.1:5000/insurance/risk'

        data = {
            "age": 30,
            "dependents": 2,
            "house": {"ownership_status": "owned"},
            "income": 0,
            "marital_status": "single",
            "vehicle": {"year": 2018}
        }

        res = self.app.post(
            url,
            data=json.dumps(data))

        jsonObj = json.loads(res.data)

        assert res.status == '200 OK'
        assert jsonObj == """Exception {'risk_questions': ['Expecting a value
        for this field.']}"""

    def tearDown(self):
        """teardown all initialized variables."""
        pass


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
