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

    def test_insurance_risk_happy_flow(self):
        """Test to get Insurance risk"""

        url = 'http://127.0.0.1:5000/insurance/risk'

        data = {
            "age": 35,
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
        assert jsonObj == {'auto': 'responsible', 'life': 'responsible',
                           'disability': 'regular', 'home': 'regular'}

    def test_insurance_risk_age_over_60_happy_flow(self):
        """Test to get Insurance risk"""

        url = 'http://127.0.0.1:5000/insurance/risk'

        data = {
            "age": 70,
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
        assert jsonObj == {'auto': 'responsible', 'life': 'responsible',
                           'home': 'responsible'}

    def test_insurance_risk_age_under_30_happy_flow(self):
        """Test to get Insurance risk"""

        url = 'http://127.0.0.1:5000/insurance/risk'

        data = {
            "age": 30,
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
        assert jsonObj == {'auto': 'responsible', 'life': 'responsible',
                           'disability': 'regular', 'home': 'regular'}

    def test_insurance_risk_age_above_30_and_under_40_happy_flow(self):
        """Test to get Insurance risk"""

        url = 'http://127.0.0.1:5000/insurance/risk'

        data = {
            "age": 35,
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
        assert jsonObj == {'auto': 'responsible', 'life': 'responsible',
                           'disability': 'regular', 'home': 'regular'}

    def test_insurance_risk_income_above_200k_happy_flow(self):
        """Test to get Insurance risk"""

        url = 'http://127.0.0.1:5000/insurance/risk'

        data = {
            "age": 40,
            "dependents": 2,
            "house": {"ownership_status": "owned"},
            "income": 400000000,
            "marital_status": "married",
            "risk_questions": [0, 1, 0],
            "vehicle": {"year": 2018}
        }

        res = self.app.post(
            url,
            data=json.dumps(data))

        jsonObj = json.loads(res.data)

        assert res.status == '200 OK'
        assert jsonObj == {'auto': 'regular', 'life': 'responsible',
                           'disability': 'regular', 'home': 'regular'}

    def test_insurance_risk_ownership_status_mortgaged_happy_flow(self):
        """Test to get Insurance risk"""

        url = 'http://127.0.0.1:5000/insurance/risk'

        data = {
            "age": 40,
            "dependents": 2,
            "house": {"ownership_status": "mortgaged"},
            "income": 10000,
            "marital_status": "married",
            "risk_questions": [0, 1, 0],
            "vehicle": {"year": 2018}
        }

        res = self.app.post(
            url,
            data=json.dumps(data))

        jsonObj = json.loads(res.data)

        assert res.status == '200 OK'
        assert jsonObj == {'auto': 'responsible', 'life': 'responsible',
                           'disability': 'regular', 'home': 'regular'}

    def test_insurance_risk_dependents_0_happy_flow(self):
        """Test to get Insurance risk"""

        url = 'http://127.0.0.1:5000/insurance/risk'

        data = {
            "age": 40,
            "dependents": 0,
            "house": {"ownership_status": "mortgaged"},
            "income": 10000,
            "marital_status": "married",
            "risk_questions": [0, 1, 0],
            "vehicle": {"year": 2018}
        }

        res = self.app.post(
            url,
            data=json.dumps(data))

        jsonObj = json.loads(res.data)

        assert res.status == '200 OK'
        assert jsonObj == {'auto': 'responsible', 'life': 'responsible',
                           'disability': 'regular', 'home': 'regular'}

    def test_insurance_risk_marital_status_single_happy_flow(self):
        """Test to get Insurance risk"""

        url = 'http://127.0.0.1:5000/insurance/risk'

        data = {
            "age": 40,
            "dependents": 0,
            "house": {"ownership_status": "mortgaged"},
            "income": 10000,
            "marital_status": "single",
            "risk_questions": [0, 1, 0],
            "vehicle": {"year": 2018}
        }

        res = self.app.post(
            url,
            data=json.dumps(data))

        jsonObj = json.loads(res.data)

        assert res.status == '200 OK'
        assert jsonObj == {'auto': 'responsible', 'life': 'regular',
                           'disability': 'regular', 'home': 'regular'}

    def test_insurance_risk_vehicle_more_than_5_years_happy_flow(self):
        """Test to get Insurance risk"""

        url = 'http://127.0.0.1:5000/insurance/risk'

        data = {
            "age": 40,
            "dependents": 0,
            "house": {"ownership_status": "mortgaged"},
            "income": 10000,
            "marital_status": "single",
            "risk_questions": [0, 1, 0],
            "vehicle": {"year": 2010}
        }

        res = self.app.post(
            url,
            data=json.dumps(data))

        jsonObj = json.loads(res.data)

        assert res.status == '200 OK'
        assert jsonObj == {'auto': 'regular', 'life': 'regular',
                           'disability': 'regular', 'home': 'regular'}

    def tearDown(self):
        """teardown all initialized variables."""
        pass


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
