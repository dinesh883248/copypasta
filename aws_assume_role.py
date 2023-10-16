#!/usr/bin/python3

import subprocess
import sys
import json
from textwrap import dedent

def get_credentials(role_arn):
    session = role_arn.split("/")[-1]
    cmd = f"""\
    aws sts assume-role \
        --role-arn {role_arn} \
        --role-session-name {session} \
        --region eu-west-2 \
        --output json
    """
    cmd = dedent(cmd)
    creds = subprocess.check_output(cmd, shell=True, text=True)
    creds = json.loads(creds)
    return creds

def print_credentials(creds):
    access_key = creds["Credentials"]["AccessKeyId"]
    secret_key = creds["Credentials"]["SecretAccessKey"]
    token = creds["Credentials"]["SessionToken"]

    env_vars = f"""
    export AWS_ACCESS_KEY_ID={access_key}
    export AWS_SECRET_ACCESS_KEY={secret_key}
    export AWS_SESSION_TOKEN={token}
    """
    print(dedent(env_vars))

if len(sys.argv) > 1:
    role = sys.argv[1]
else:
    print("Please provide role.")
    print("Usage: assume-role arn:aws:iam::123456789:role/example")
    sys.exit(1)

creds = get_credentials(role)
print_credentials(creds)
