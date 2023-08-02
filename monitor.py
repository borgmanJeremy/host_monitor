"""This application checks if a service is up and sends a push notification if it is down"""
import argparse
import urllib
import urllib.request
import http.client
import json
import os
import sys

def get_tokens(json_file):
    """Loads the user tokens from a json file"""
    with open(json_file, encoding="UTF-8") as json_file:
        data = json.load(json_file)
        app_token = data["APP_TOKEN"]
        user_key = data["USER_TOKEN"]
        return {"app_token": app_token, "user_token": user_key}


def service_is_up(url: str) -> bool:
    """Checks if the service is up by looking to see if the response code is 200"""
    try:
        response = urllib.request.urlopen(url, timeout=10)
        code = response.code
    except urllib.error.HTTPError as error:
        code = error.code
    return bool(code == 200)


if __name__ == "__main__":

    full_path = os.path.join(sys.path[0], "keys.json")
    tokens = get_tokens(full_path)

    parser = argparse.ArgumentParser(description="Checks if a service is up")
    parser.add_argument("-u", "--url", required=True, help="The url to check")
    parser.add_argument("-n", "--name", required=True, help="The name of the service")

    args = parser.parse_args()

    if service_is_up(args.url) is False:
        print(f"{args.name} is down")
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request(
            "POST",
            "/1/messages.json",
            urllib.parse.urlencode(
                {
                    "token": tokens["app_token"],
                    "user": tokens["user_token"],
                    "message": f"{args.name} is down!",
                }
            ),
            {"Content-type": "application/x-www-form-urlencoded"},
        )
        conn.getresponse()
    else:
        print(f"{args.name} is up")
