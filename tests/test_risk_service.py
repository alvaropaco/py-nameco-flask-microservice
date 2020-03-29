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
        assert len(jsonObj) > 0

    def tearDown(self):
        """teardown all initialized variables."""
        pass


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
