from unittest.mock import DEFAULT
import requests
import os
import argparse
from dotenv import load_dotenv

load_dotenv()


def getenv_safe(key):
    value = os.getenv(key)
    if value is None:
        raise Exception(f'enviornment variable {key} is not set')
    return value


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('namespace', help='Name of the namespace to create')
    parser.add_argument('broker', help='Name of the broker to create')
    parser.add_argument(
        '--just-creds', help='Only create the creds', action='store_true')
    parser.add_argument(
        '--number', help='Amount of keys to generate', default=1, type=int)

    args = parser.parse_args()

    CF_API_EMAIL = getenv_safe('CF_API_EMAIL')
    CF_API_KEY = getenv_safe('CF_API_KEY')
    CF_ACCOUNT_ID = getenv_safe('CF_ACCOUNT_ID')

    headers = {
        'X-Auth-Email': f"{CF_API_EMAIL}",
        'X-Auth-Key': f"{CF_API_KEY}",
    }

    if not args.just_creds:
        print(f'Creating namespace {args.namespace}')
        response = requests.post(
            f'https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/pubsub/namespaces', headers=headers, json={
                'name': args.namespace
            })

        response_json = response.json()
        if (not response_json['success']):
            print(response_json['errors'])
            raise Exception(f'Failed to create namespace {args.namespace}')

        print(f'Creating broker {args.broker}')
        response = requests.post(
            f'https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/pubsub/namespaces/{args.namespace}/brokers', headers=headers, json={
                'name': args.broker,
                'authType': 'TOKEN',
            })

        response_json = response.json()
        if (not response_json['success']):
            print(response_json['errors'])
            raise Exception(f'Failed to create broker {args.broker}')
        endpoint = response_json['result']['endpoint']

    print(f'Creating {args.number} credentials')
    response = requests.get(
        f'https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/pubsub/namespaces/{args.namespace}/brokers/{args.broker}/credentials', headers=headers, params={
            'number': f'{args.number}',
            'type': 'TOKEN',
            'topicAcl': '',
        })
    response_json = response.json()

    if (not response_json['success']):
        print(response_json['errors'])
        raise Exception(f'Failed to create credentials')

    print("Successfully created credentials")
    if not args.just_creds:
        print(f'Endpoint: {endpoint}')
    for (idx, client_id) in enumerate(response_json['result'].keys()):
        print(f'{idx+1}.')
        print(f'  Client ID: {client_id}')
        print(f'  Credential ID: {response_json["result"][client_id]}')

    if not args.just_creds:
        first_broker_id = next(iter(response_json['result'].keys()))
        print("Writing to .env file...")
        with open('.env', 'a') as f:
            f.write(f'\n\n# PubSub Credentials\n')
            f.write(
                f'PUBSUB_ENDPOINT="{":".join(endpoint.split(":")[0:2])}"\n')
            f.write(f'PUBSUB_PORT="{endpoint.split(":")[2]}"\n')
            f.write(
                f'PUBSUB_URI="{endpoint.strip("mqtts://").split(":")[0]}"\n')
            f.write(f'DEFAULT_NAMESPACE="{args.namespace}"\n')
            f.write(f'BROKER_NAME="{args.broker}"\n')
            f.write(f'BROKER_CLIENT_ID="{first_broker_id}"\n')
            f.write(
                f'BROKER_TOKEN="{response_json["result"][first_broker_id]}"\n')
    print("Done!")
