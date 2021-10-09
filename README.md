# calculate_cashflow


## Scope
1. User manually enters events into Google calendar
    1. Income - <Payer> $AMOUNT
    2. Due - <Payee> $AMOUNT
2. User enters
    1. Date range for calculations
    2. Cash on hand (optional, only if date range is from TODAY)
3. Calculate_cashflow returns
    1. The total return amount for that time period
        - IE. Total income, total bills, $xyz surplus/defecit
        - The daily and weekly breakdown of that amount


## How To Use
1. Set up your recurring income and bills in calendar with 'Income' and 'Due' in the relevant event names
2. Register for Oauth2.0 authentication through google's API console: https://developers.google.com/calendar/api/guides/auth
3. Download the credential file they gave you to this directory, save it as credentials.json
4. Execute the script
    - --end_date - REQUIRED - example: 2021-10-31
    - --coh (cash on hand) - OPTIONAL - example: 1500
    - Example: python3 calculate_cashflow.py --end_date 2021-11-15 -coh 1500

