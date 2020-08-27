#!/usr/bin/env python
"""
    intersight_devices.py -  provides a class to support Cisco Intersight
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

    claimId: The short lived claim ID to use for claiming

    deviceID: The device ID which will be used for claiming

    secretKeyFileName: Path to user's API secret key file
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['claim', 'registrations'])
    parser.add_argument('--apiKeyId')
    parser.add_argument('--claimId')
    parser.add_argument('--deviceId')
    parser.add_argument('--secretKeyFileName')

    args = parser.parse_args()
    if args.action == 'claim':
        if args.deviceId is None or args.claimId is None:
            print('Both --deviceId and --claimid are REQUIRED')
            sys.exit(1)

    return args


def claim(**kwargs):
    """Sends a claim request to claim new devices"""

    args = kwargs['args']
    auth = kwargs['auth']

    url = f'{BURL}/asset/DeviceClaims'
    payload = {
        'SecurityToken': args.claimId,
        'SerialNumber': args.deviceId
    }
    response = requests.request(
        'POST', url, auth=auth, headers=HEADERS, data=json.dumps(payload))

    print(json.dumps(response.json()))


def registrations(**kwargs):
    """Returns a JSON list of device registrations"""

    auth = kwargs['auth']

    url = f'{BURL}/asset/DeviceRegistrations'
    response = requests.request('GET', url, auth=auth)

    print(json.dumps(response.json()))


def main():
    """Main execution"""

    args = cli_args()

    auth = IntersightAuth(
        secret_key_filename=args.secretKeyFileName,
        api_key_id=args.apiKeyId
    )

    action_lookup = {'claim': claim, 'registrations': registrations}
    action = action_lookup[args.action]

    action(args=args, auth=auth)


if __name__ == "__main__":
    main()
