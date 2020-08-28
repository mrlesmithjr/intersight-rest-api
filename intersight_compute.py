#!/usr/bin/env python
"""
    intersight_compute.py -  provides a class to support Cisco Intersight
    interactions

    author: Larry Smith Jr. (mrlesmithjr@gmail.com)
"""

import json
import argparse
import requests

from intersight_auth import IntersightAuth

# Intersight REST API Base URL
BURL = 'https://www.intersight.com/api/v1'

HEADERS = {'Accept': 'application/json',
           'Content-Type': 'application/json'}


def cli_args():
    """
    Provides CLI argument options

    action: Action to take using API

    apiKeyId: User's API key ID for auth

    secretKeyFileName: Path to user's API secret key file
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['blades', 'physical', 'rackUnits'])
    parser.add_argument('--secretKeyFileName')
    parser.add_argument('--apiKeyId')

    args = parser.parse_args()

    return args


def blades(**kwargs):
    """Returns a JSON list of blades"""

    auth = kwargs['auth']

    url = f'{BURL}/compute/Blades'
    response = requests.request('GET', url, auth=auth)

    print(json.dumps(response.json()))


def physical(**kwargs):
    """Returns a JSON list of physical compute summaries"""

    auth = kwargs['auth']

    url = f'{BURL}/compute/PhysicalSummaries'
    response = requests.request('GET', url, auth=auth)

    print(json.dumps(response.json()))


def rack_units(**kwargs):
    """Returns a JSON list of rack units"""

    auth = kwargs['auth']

    url = f'{BURL}/compute/RackUnits'
    response = requests.request('GET', url, auth=auth)

    print(json.dumps(response.json()))


def main():
    """Main execution"""

    args = cli_args()

    auth = IntersightAuth(
        secret_key_filename=args.secretKeyFileName,
        api_key_id=args.apiKeyId
    )

    action_lookup = {'blades': blades,
                     'rackUnits': rack_units, 'physical': physical}
    action = action_lookup[args.action]

    action(args=args, auth=auth)


if __name__ == "__main__":
    main()
