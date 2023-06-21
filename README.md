# InsightVM-Python

Rapid7 InsightVM Postgres Reporting built in Python and PostgreSQL
Rapid7 InsightVM API tools using Python
PaloAlto Cortex XDR API

## API References

1. [InsightVM API](https://help.rapid7.com/insightvm/en-us/api/index.html)
2. [Palo Alto Cortex XDR API](https://docs-cortex.paloaltonetworks.com/r/Cortex-XDR/Cortex-XDR-API-Reference/APIs-Overview)
3. [Secureworks Taegis API Docs](https://api-docs.taegis.secureworks.com)
4. [Secureworks Taegis Docs](https://docs.ctpx.secureworks.com/taegis/)

## api_pa_xdr_auth.py

The `api_pa_xdr_auth.py` script is a Python script that provides authentication for the PaloAlto Cortex XDR API. This script requires the `requests` library to be installed.

### Description

The `api_pa_xdr_auth.py` script is designed to provide authentication for the PaloAlto Cortex XDR API. It allows users to authenticate their API credentials using the `config.json` file. This script is useful for developers who want to automate their Cortex XDR API authentication process.

### How to Use

To use the `api_pa_xdr_auth.py` script, follow these steps:

1. Install the `requests` library.
2. Create a `config.json` file in the following format:
