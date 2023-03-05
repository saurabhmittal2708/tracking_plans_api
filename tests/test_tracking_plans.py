import pytest
import requests
from aws_controller import generate_key
TEST_TRACKING_PLANS = [
    {
        "display_name": "Tracking Plan",
        "rules": {
		"events": [{
			"name": f"{generate_key()}",
			"description": "Whose order viewed",
			"rules": {
				"$schema": "http://json-schema.org/draft-07/schema#",
				"type": "object",
				"properties": {
					"type": "object",
					"properties": {
						"product": {
							"type": ["string"]
						},
						"price": {
							"type": ["number"]
						},
						"currency": {
							"type": ["string"]
						}
					},
					"required": [
						"product",
						"price",
						"currency"
					]
				}
			}
		}]
	}
    },
    {
	    "display_name": "Tracking Plan1"
    }
]

TEST_BASE_URL = r"http://localhost:5000"

def repr_fun(payload: dict) -> str:
    return payload['display_name']

@pytest.mark.parametrize(TEST_TRACKING_PLANS, 'tracking_plan_payload', ids=repr_fun)
def test_create_plan(tracking_plan_payload: dict):
    url = f'{TEST_BASE_URL}/tracking_plans'
    res = requests.post(json=tracking_plan_payload)
    assert res.status_code == 200

def test_get_plans():
    url = f'{TEST_BASE_URL}/tracking_plans'
    res = requests.get(url)
    assert res.status_code == 200
    assert len(res.json())


