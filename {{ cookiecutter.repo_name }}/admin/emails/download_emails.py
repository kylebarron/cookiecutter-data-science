#! /usr/bin/env python3
"""
---------------------------------------------------------------------
Project: {{ cookiecutter.project_name }}
Program: download_emails.py
Author:  Kyle Barron <barronk@mit.edu>
Purpose: Download project emails from Gmail for future reference
Outputs: Emails in current directory

First, follow the instructions at https://github.com/kylebarron/gmail_download
to set up the authentication.

Gmail query options explained here:
https://support.google.com/mail/answer/7190?hl=en
"""

from gmail_download import gmail_query

g_query = """\
query
"""

q = gmail_query(
    email_address='',
    outdir='.',
    client_secret_path='~/.config/gmail-download/client_secret.json',
    credential_path='~/.credentials/gmail_download.json')
q.query(
    begin_date='2018-02-03',
    end_date='today',
    g_query=g_query,
    tz_locale='America/New_York')
