import json
import requests
import inspect
from app import dashboard, app
from pathlib import Path
import pytest

# API_URL = "http://127.0.0.1:5000"


# def make_request(
#     endpoint, expected_code, method="get", data=None, decode_json=True, level=0
# ):
#     prefix = "  " * level
#     print(f"{prefix}{method.upper()} {endpoint} (expecting {expected_code})...")
#     kwargs = {}
#     func = getattr(requests, method)

#     if data:
#         kwargs["json"] = data
#         print(f"{prefix} > Data provided", data)

#     status = True
#     data = ""

#     try:
#         resp = func(API_URL + endpoint, **kwargs)
#         if resp.status_code == 200 and decode_json:
#             data = resp.json()
#         else:
#             data = resp.text
#     except json.decoder.JSONDecodeError:
#         data = "Cannot decode JSON from API."
#         status = False
#     except (requests.exceptions.ConnectionError,):
#         data = "Connection error."
#         status = False
#     else:
#         if resp.status_code != expected_code:
#             print(
#                 f"{prefix}  Status code should be {expected_code}, got {resp.status_code}."
#             )
#             status = False

#     return status, data


# def homepage():
#     """Checks the HTML homepage"""
#     status, data = make_request("/", 200, decode_json=False)
#     if not status:
#         print("  !!! NOK", data)
#         return


@pytest.fixture()
def client():
    return app.test_client()


def test_valid_admin_user(client):
    response = client.post("/admin/dashboard",
                           data={"email": "hello"})
    assert response.status_code == 200


def check():
    funcs = [
        # homepage,
        test_valid_admin_user
    ]

    for func in funcs:
        print("=" * 80)
        print(inspect.getdoc(func))
        print("-" * 80)
        func()
        print()


if __name__ == "__main__":
    check()
