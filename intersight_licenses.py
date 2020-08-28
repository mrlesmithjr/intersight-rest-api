#!/usr/bin/env python
"""
    intersight_licenses.py -  provides a class to support Cisco Intersight
    interactions

    author: Larry Smith Jr. (mrlesmithjr@gmail.com)
"""

import json
import argparse
import sys
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

    licenseType: License type to apply

    secretKeyFileName: Path to user's API secret key file
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=[
                        'accountLicenses', 'applyLicenses', 'resourceLicenses']
                        )
    parser.add_argument('--apiKeyId')
    parser.add_argument(
        '--licenseType', choices=['Base', 'Essentials', 'Advantage', 'Premier']
    )
    parser.add_argument('--secretKeyFileName')

    args = parser.parse_args()

    return args


def account_licenses(**kwargs):
    """Returns a JSON list of account licenses and info"""

    auth = kwargs['auth']

    url = f'{BURL}/license/AccountLicenseData'
    response = requests.request('GET', url, auth=auth)

    print(json.dumps(response.json()))


def apply_licenses(**kwargs):
    """Applies a license to all rack units."""

    auth = kwargs['auth']
    args = kwargs['args'].__dict__

    license_type = args['licenseType']

    if license_type is None:
        print('--licenseType should not be None')
        sys.exit(1)

    url = f'{BURL}/compute/PhysicalSummaries'
    response = requests.request('GET', url, auth=auth)

    json_results = response.json()['Results']
    for item in json_results:
        moid = item['Moid']
        obj_type = item['SourceObjectType']

        if obj_type == 'compute.Blade':
            url = f'{BURL}/compute/Blades/{moid}'
        elif obj_type == 'compute.RackUnit':
            url = f'{BURL}/compute/RackUnits/{moid}'
        else:
            pass

        payload = {
            "Tags": [
                {
                    "Key": "Intersight.LicenseTier",
                    "Value": license_type
                }]
        }

        response = requests.request(
            'POST', url, auth=auth, headers=HEADERS, data=json.dumps(payload))

        if response.status_code == 200:
            results = {'status_code': response.status_code,
                       'moid': moid, 'name': item['Name'], 'obj_type': obj_type,
                       'license_type': license_type, 'serial': item['Serial']}
            print(json.dumps(results))
        else:
            print(json.dumps(response.json()))


def resource_licenses(**kwargs):
    """Returns a JSON list of resource licenses and info"""

    auth = kwargs['auth']

    url = f'{BURL}/resource/LicenseResourceCounts'
    response = requests.request('GET', url, auth=auth)

    print(json.dumps(response.json()))


def main():
    """Main execution"""

    args = cli_args()

    auth = IntersightAuth(
        secret_key_filename=args.secretKeyFileName,
        api_key_id=args.apiKeyId
    )

    action_lookup = {'accountLicenses': account_licenses,
                     'applyLicenses': apply_licenses,
                     'resourceLicenses': resource_licenses}
    action = action_lookup[args.action]

    action(args=args, auth=auth)


if __name__ == "__main__":
    main()
