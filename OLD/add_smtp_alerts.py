import requests
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

IVM_AUTH = os.getenv('IVM_AUTH')
IVM_CONNECTION = os.getenv('IVM_CONNECTION')
SMTP_HOST = os.getenv('SMTP_HOST')
SMTP_SENDER = os.getenv('SMTP_SENDER')

smtp_config = {}

if not SMTP_HOST:
    raise ValueError("SMTP_HOST environment variable not set")
smtp_config["host"] = SMTP_HOST

if not SMTP_SENDER:
    raise ValueError("SMTP_SENDER environment variable not set")
smtp_config["sender"] = SMTP_SENDER

if not IVM_AUTH:
    raise ValueError("IVM_AUTH environment variable not set")

if not IVM_CONNECTION:
    raise ValueError("IVM_CONNECTION environment variable not set")


def get_alert_ids(siteID):
    alerts = requests.get(
        f"{IVM_CONNECTION}sites/{siteID}/alerts/smtp", verify=True, auth=(IVM_AUTH, ''))
    alerts.raise_for_status()
    alertIDs = []
    for alert in alerts.json()["resources"]:
        alertIDs.append(alert["id"])
    return alertIDs


def add_smtp_alert(siteID, name, recipients, alertID=None, enabled=True, enabledScanEvents=None, enabledVulnerabilityEvents=None,
                   maximumAlerts=1, notification="SMTP", relayServer=smtp_config["host"], senderEmailAddress=smtp_config["sender"]):
    if not name or not recipients:
        raise ValueError("Name of alert or alert recipients are missing")

    if not enabledScanEvents:
        enabledScanEvents = {"failed": False, "paused": False,
                             "resumed": False, "started": False, "stopped": False}

    if not enabledVulnerabilityEvents:
        enabledVulnerabilityEvents = {
            "confirmedVulnerabilities": True,
            "potentialVulnerabilities": True,
            "unconfirmedVulnerabilities": True,
            "vulnerabilitySeverity": "any_severity"
        }

    params = {
        "name": name,
        "enabled": enabled,
        "enabledScanEvents": enabledScanEvents,
        "enabledVulnerabilityEvents": enabledVulnerabilityEvents,
        "notification": notification,
        "recipients": recipients,
        "relayServer": relayServer,
        "senderEmailAddress": senderEmailAddress,
        "maximumAlerts": maximumAlerts
    }

    if alertID:
        params["id"] = alertID
        smtp_alert = requests.put(
            f"{IVM_CONNECTION}sites/{siteID}/alerts/smtp", verify=True, auth=(IVM_AUTH, ''), json=params)
    else:
        smtp_alert = requests.post(
            f"{IVM_CONNECTION}sites/{siteID}/alerts/smtp", verify=True, auth=(IVM_AUTH, ''), json=params)

    smtp_alert.raise_for_status()

    if "id" in smtp_alert.json().keys():
        alertID = smtp_alert.json()["id"]

    print(f"Created alert for site {siteID}: {alertID}")


alertIDs = get_alert_ids(70)

if alertIDs:
    for id in alertIDs:
        print(id)
        add_smtp_alert(70, "Test", ["testloop@rapid7.com"], enabled=False, alertID=id, enabledScanEvents={
                       "failed": True, "paused": False, "resumed": False, "started": False, "stopped": False})
else:
    add_smtp_alert(70, "Test", ["testtesttest@rapid7.com"], enabled=True)
