from __future__ import print_function
import datetime
from os import error
import os.path
import json
from requests import api
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import argparse
import re

## TODO: Parse decimal dollar values
## TODO: Gracefully handle DUE/INCOME events with no dollar value


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

parser = argparse.ArgumentParser(description="A tool to export UP transactions in a CSV file")
parser.add_argument('--end_date', type=str)
parser.add_argument('--start_date', type=str)
parser.add_argument('--coh', type=str)
args = parser.parse_args()


def main():
    income = 0
    due = 0.0
    try:
        dtdate = datetime.datetime.strptime(args.end_date, '%Y-%m-%d')
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('calendar', 'v3', credentials=creds)

        if args.start_date:
            startdate = datetime.datetime.strptime(args.start_date, '%Y-%m-%d')
            now = startdate.isoformat() + 'Z'
        else:
            now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                            maxResults=150, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            date_start = datetime.datetime.strptime(start, '%Y-%m-%d')

            if date_start < dtdate:
                if 'Income' in event['summary']:
                    value = re.findall('[0-9]+', event['summary'])
                    income = income + int(value[0])

                if 'Due' in event['summary']:
                    value = re.findall('[0-9]+', event['summary'])
                    due = due + int(value[0])
        
        delta = date_start - dtdate
        days = delta.days

        cashflow = income - due
        if args.coh:
            cashflow = cashflow + int(args.coh)
        print(days)
        daily_spend = round(cashflow / days)
        weekly_spend = round(daily_spend * 7)
        
        print('Bills: ${} \nIncome: ${}'.format(due, income))
        print('Spare Cash: ${}'.format(cashflow))
        if cashflow > 0:
            print('Daily Spend: ${}'.format(daily_spend))
            print('Weekly Spend: ${}'.format(weekly_spend))
        else:
            print('You\'re fucking broke dude')


        

    except error as E:
        print(E)

if __name__ == '__main__':
    main()