import csv
import json
import os
import re
import requests
import sys
from datetime import date

'''
    File name: long-range-rents-rea.py
    Author: Naaman Campbell
    Date created: 2022-10-30
    Date last modified: 2022-10-30
    Python Version: 3.10
'''

with open('search.json', 'r') as f:
    search_json = json.load(f)

endpoint = 'https://api.domain.com.au/v1/listings/residential/_search'
request_headers = {
    'X-API-Key': os.getenv('DOMAIN_API_KEY'),
    'Content-Type': 'application/json'}
search_json = json.dumps(search_json)
results = requests.post(endpoint, data=search_json, headers=request_headers)
headers = results.headers
status_code = results.status_code
results = results.json()

if status_code >= 400:
    message = results.get('message', '')
    print(f'{status_code} - {message}')
    sys.exit(1)

# retrieve and print API rate limit and warning
if headers.get('X-RateLimit-Limit'):
    match = re.search(r'per (.*)$', headers['X-RateLimit-Limit'])
    rate_limit = match.group(1)
    rate_limit_remaining = headers['X-RateLimit-Remaining']
    total_count = headers['X-Total-Count']
    print(f'{rate_limit_remaining} remaining API calls in {rate_limit} period')
    if int(total_count) > int(rate_limit_remaining):
        print(f'Total items ({total_count}) exceeds rate limit. Exiting..')
        sys.exit(1)

# retrieve each detailed listing
csv_data = []
csv_columns = ['ID', 'Available', 'Address', 'Price', 'URL']
for listing in results:
    listing_id = listing['listing']['id']
    endpoint = f'https://api.domain.com.au/v1/listings/{listing_id}'
    headers = {'X-API-Key': os.getenv('DOMAIN_API_KEY')}
    full_listing = requests.get(endpoint, headers=headers)
    full_listing = full_listing.json()

    price = 0
    if not full_listing['priceDetails'].get('price'):
        valid_price = False
        if full_listing['priceDetails'].get('displayPrice'):
            price = full_listing['priceDetails']['displayPrice']
            match = re.search(r'\$(\d+)', price)
            if match:
                valid_price = True
                price = match.group(1)
        if not valid_price:
            print(f'Skipping ID#{listing_id} - no prices')
            continue
    else:
        price = full_listing['priceDetails']['price']

    if not full_listing.get('dateAvailable'):
        # set today's date for missing available dates
        today = date.today()
        full_listing['dateAvailable'] = today.strftime("%Y-%m-%d")

    csv_data.append({
        'ID': listing_id, 
        'Available': full_listing['dateAvailable'], 
        'Address': full_listing['addressParts']['displayAddress'], 
        'Price': price, 
        'URL': full_listing['seoUrl']
    })

# sort CSV data by available date
csv_data = sorted(csv_data, key=lambda x: x['Available'], reverse=True)

with open('long-range-rents.csv', 'w', newline='') as f:
    csv_writer = csv.DictWriter(f, fieldnames=csv_columns)
    csv_writer.writeheader()
    for entry in csv_data:
        csv_writer.writerow(entry)