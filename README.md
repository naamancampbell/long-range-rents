# long-range-rents
Lists rentals on domain.com.au by available date<br />
_Created by Naaman Campbell_

## Domain API Access
[Register](https://developer.domain.com.au) for a Domain developer account and
create a new Project.<br />Once created, add the Agents & Listings - Free 
(non-sandbox) API via the **API Access** menu.

An API Key is also required for long-range-rents.  A key can be generated via
the **Credentials** menu.

The API Key is required to be set as the `DOMAIN_API_KEY` environment variable 
before running long-range-rents.

## search.json
Build property searches using the Domain Search Parameters model:
https://developer.domain.com.au/docs/apis/pkg_agents_listings/references/listings_detailedresidentialsearch

## Python environment setup
long-range-rents uses the `requests` package in addition to the standard Python
packages.

`pip install requests` (optionally in a 
[virtualenv](https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv))

## Generating rental lists
`python long-range-rents.py` will generate `long-range-rents.csv` containing
rentals ordered by available date in the following format:

|Listing ID|Available Date|Address|Price|Domain Listing URL|
|----------|--------------|-------|-----|------------------|