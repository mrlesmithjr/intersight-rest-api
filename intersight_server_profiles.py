#!/usr/bin/env python
"""
    intersight_server_profiles.py -  provides a class to support Cisco
    Intersight interactions

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
    parser.add_argument('action', choices=[
                        'createDefaultBiosPolicy',
                        'createDefaultBootPolicy',
                        'createDefaultNtpPolicy',
                        'getBootPolicies',
                        'getBiosPolicies',
                        'getNtpPolicies',
                        'getProfiles'])
    parser.add_argument('--secretKeyFileName')
    parser.add_argument('--apiKeyId')

    args = parser.parse_args()

    return args


def create_default_bios_policy(**kwargs):
    """Creates a default BIOS Policy"""

    auth = kwargs['auth']

    payload = {'Name': 'default-bios-policy',
               'Description': 'Default BIOS policy'}

    url = f'{BURL}/bios/Policies'

    response = requests.request(
        'POST', url, auth=auth, headers=HEADERS, data=json.dumps(payload))

    print(json.dumps(response.json()))


def create_default_boot_policy(**kwargs):
    """Creates a default boot Policy"""

    auth = kwargs['auth']

    payload = {'Name': 'default-boot-policy',
               'Description': 'Default boot policy',
               "BootDevices": [
                   {
                       "ObjectType": "boot.LocalDisk",
                       "Enabled": True, "Name": "boot",
                                        "Slot": "SAS"
                   },
                   {
                       "ObjectType": "boot.LocalCdd",
                       "Enabled": True, "Name": "vmedia"
                   }
               ]}

    url = f'{BURL}/boot/PrecisionPolicies'

    response = requests.request(
        'POST', url, auth=auth, headers=HEADERS, data=json.dumps(payload))

    print(json.dumps(response.json()))


def create_default_ntp_policy(**kwargs):
    """Creates a default NTP Policy"""

    auth = kwargs['auth']

    payload = {'Name': 'default-ntp-policy',
               'Description': 'Default NTP policy',
               'Enabled': True,
               'NtpServers': ['pool.ntp.org'],
               'Tags': []}

    url = f'{BURL}/ntp/Policies'

    response = requests.request(
        'POST', url, auth=auth, headers=HEADERS, data=json.dumps(payload))

    print(json.dumps(response.json()))


def get_bios_policies(**kwargs):
    """Returns a JSON list of all server profiles"""

    auth = kwargs['auth']

    url = f'{BURL}/bios/Policies'
    response = requests.request('GET', url, auth=auth)

    print(json.dumps(response.json()))


def get_boot_policies(**kwargs):
    """Returns a JSON list of all server profiles"""

    auth = kwargs['auth']

    url = f'{BURL}/boot/PrecisionPolicies'
    response = requests.request('GET', url, auth=auth)

    print(json.dumps(response.json()))


def get_ntp_policies(**kwargs):
    """Returns a JSON list of all NTP policies"""

    auth = kwargs['auth']

    url = f'{BURL}/ntp/Policies'
    response = requests.request('GET', url, auth=auth)

    print(json.dumps(response.json()))


def get_profiles(**kwargs):
    """Returns a JSON list of all server profiles"""

    auth = kwargs['auth']

    url = f'{BURL}/server/Profiles'
    response = requests.request('GET', url, auth=auth)

    print(json.dumps(response.json()))


def main():
    """Main execution"""

    args = cli_args()

    auth = IntersightAuth(
        secret_key_filename=args.secretKeyFileName,
        api_key_id=args.apiKeyId
    )

    action_lookup = {'createDefaultBiosPolicy': create_default_bios_policy,
                     'createDefaultBootPolicy': create_default_boot_policy,
                     'createDefaultNtpPolicy': create_default_ntp_policy,
                     'getBiosPolicies': get_bios_policies,
                     'getBootPolicies': get_boot_policies,
                     'getNtpPolicies': get_ntp_policies,
                     'getProfiles': get_profiles}
    action = action_lookup[args.action]

    action(args=args, auth=auth)


if __name__ == "__main__":
    main()
