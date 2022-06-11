# Cloudflare Pub/Sub examples

This repository contains examples of using Cloudflare Pub/Sub with different languages, and instructions to use clients. It is not affiliated with Cloudflare in any way.
Note that these examples were made during the beta, so they may not work anymore if the API changes.

The `create_required_info.py` file can be used to create a `.env` with the information needed to use the examples. To use this program, set the following environment variables:

- `CF_API_EMAIL`: The email address associated with your Cloudflare account
- `CF_API_KEY`: The Global API Key associated with your Cloudflare account (this may change after the beta)
- `CF_ACCOUNT_ID`: The Account ID associated with your Cloudflare account

This program also support `.env` files, so you can copy the `.env.example` and set the apporpriate values.

## List of examples

- Python (using [`paho-mqtt`](https://pypi.org/project/paho-mqtt))
- NodeJS (Both typescript and javascript, using [`mqtt`](https://www.npmjs.com/package/mqtt))

## List of guides

- [MQTTX](https://mqttx.app)
