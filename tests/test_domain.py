import pytest
import json
import os
import sys

from long_range_rents import domain_results


@pytest.fixture(scope="module")
def domain_api():
    if not os.getenv('DOMAIN_API_KEY'):
        print('DOMAIN_API_KEY environment variable not found. Exiting..')
        sys.exit(1)

    endpoint = 'https://api.domain.com.au/v1/listings/residential/_search'
    headers = {
        'X-API-Key': os.getenv('DOMAIN_API_KEY'),
        'Content-Type': 'application/json'
    }

    return endpoint, headers


@pytest.fixture(scope="module")
def search_json():
    with open('search.json', 'r') as f:
        search_json = json.load(f)

    return json.dumps(search_json)    


def test_domain_results_default(search_json, domain_api):
    results, headers, status_code = domain_results(search_json, domain_api[0], domain_api[1])
    assert status_code < 400