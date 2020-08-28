#!/usr/bin/env python
"""
    intersight_compute.py -  provides a class to support Cisco Intersight
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

    secretKeyFileName: Path to user's API secret key file
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=[
                        'assignManagementMode', 'blades', 'physical',
                        'rackUnits'])
    parser.add_argument('--apiKeyId')
    parser.add_argument('--managementMode',
                        choices=['Intersight', 'IntersightStandalone', 'UCSM'])
    parser.add_argument('--secretKeyFileName')

    args = parser.parse_args()

    return args


def assign_mgmt_mode(**kwargs):
    """Assign compute management mode"""

    auth = kwargs['auth']
    args = kwargs['args'].__dict__

    mgmt_mode = args['managementMode']

    if mgmt_mode is None:
        print('--managementMode should not be None')
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

        payload = {"ManagementMode": mgmt_mode}

        response = requests.request(
            'POST', url, auth=auth, headers=HEADERS, data=json.dumps(payload))

        if response.status_code == 200:
            results = {'status_code': response.status_code,
                       'moid': moid, 'name': item['Name'],
                       'obj_type': obj_type,
                       'mgmt_mode': mgmt_mode, 'serial': item['Serial']}
            print(json.dumps(results))
        else:
            print(json.dumps(response.json()))


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

    action_lookup = {'assignManagementMode': assign_mgmt_mode, 'blades': blades,
                     'rackUnits': rack_units, 'physical': physical}
    action = action_lookup[args.action]

    action(args=args, auth=auth)


if __name__ == "__main__":
    main()
