# shopping_cart.py
import os
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime

load_dotenv()

def main():

    while check == True:
        print("Shopping Cart Interface")
        print("-----------------------")
        print()
        choice = input(Would you like to )
    products = GetProducts()
    print(products)






    prices = [item["price"] for item in products]
    TotalPrice = sum(prices)

    TAX_RATE = os.getenv("TAX_RATE", default="OOPS, please set env var called 'TAX_RATE'")
    if TAX_RATE == "OOPS, please set env var called 'TAX_RATE'":
        print(TAX_RATE)
    else:
        TotalPriceWTax = TotalPrice*(1+float(TAX_RATE))

    #output = FormatOutput(products)
    TotalPriceWTaxUSD = to_usd(TotalPriceWTax)
    TotalPriceUSD = to_usd(TotalPrice)

    TO_ADDRESS = input("Email? ")
    SendEmail(TO_ADDRESS, TotalPriceUSD,TotalPriceWTaxUSD, products)


def to_usd(my_price):
    return f"${my_price:,.2f}" #> $12,000.71

def GetProducts():

    DOCUMENT_ID = os.getenv("GOOGLE_SHEET_ID", default="OOPS")
    SHEET_NAME = os.getenv("SHEET_NAME", default="Products-2021")

    CREDENTIALS_FILEPATH = os.path.join(os.path.dirname(__file__), "auth", "google-credentials.json")

    AUTH_SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets", #> Allows read/write access to the user's sheets and their properties.
        "https://www.googleapis.com/auth/drive.file" #> Per-file access to files created or opened by the app.
    ]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILEPATH, AUTH_SCOPE)
    print("CREDS:", type(credentials)) #> <class 'oauth2client.service_account.ServiceAccountCredentials'>

    client = gspread.authorize(credentials)
    print("CLIENT:", type(client)) #> <class 'gspread.client.Client'>

    #
    # READ SHEET VALUES
    #

    print("-----------------")
    print("READING DOCUMENT...")

    doc = client.open_by_key(DOCUMENT_ID)
    print("DOC:", type(doc), doc.title) #> <class 'gspread.models.Spreadsheet'>

    sheet = doc.worksheet(SHEET_NAME)
    print("SHEET:", type(sheet), sheet.title)#> <class 'gspread.models.Worksheet'>

    rows = sheet.get_all_records()
    print("ROWS:", type(rows)) #> <class 'list'>
    print(rows)
    for row in rows:
        print(row) #> <class 'dict'>
    return rows
    #
    # WRITE VALUES TO SHEET
    #
    # see: https://gspread.readthedocs.io/en/latest/api.html#gspread.models.Worksheet.insert_row

    # print("-----------------")
    # print("NEW ROW...")
    #
    # auto_incremented_id = len(rows) + 1 # TODO: should change this to be one greater than the current maximum id value
    # new_row = {
    #     "id": auto_incremented_id,
    #     "name": "Oreos",
    #     "aisle": "cookies cakes",
    #     "department": "snacks",
    #     "price": 4.99
    # }
    # print(new_row)
    #
    # print("-----------------")
    # print("WRITING VALUES TO DOCUMENT...")
    #
    # # the sheet's insert_row() method wants our data to be in this format (see docs):
    # new_values = list(new_row.values())
    #
    # # the sheet's insert_row() method wants us to pass the row number where this will be inserted (see docs):
    # next_row_number = len(rows) + 2 # number of records, plus a header row, plus one
    #
    # response = sheet.insert_row(new_values, next_row_number)
    #
    # print("RESPONSE:", type(response)) #> dict
    # print(response) #> {'spreadsheetId': '____', 'updatedRange': "'Products-2021'!A9:E9", 'updatedRows': 1, 'updatedColumns': 5, 'updatedCells': 5}

def FormatOutput(input):

    return str(input)

def SendEmail(TO_ADDRESS, TotalPriceUSD,TotalPriceWTaxUSD, products):
    ## Email code
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", default="OOPS, please set env var called 'SENDGRID_API_KEY'")
    SENDGRID_TEMPLATE_ID = os.getenv("SENDGRID_TEMPLATE_ID", default="OOPS, please set env var called 'SENDGRID_TEMPLATE_ID'")
    SENDER_ADDRESS = os.getenv("SENDER_ADDRESS", default="OOPS, please set env var called 'SENDER_ADDRESS'")

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    # this must match the test data structure
    template_data = {
        "total_price_usd": TotalPriceUSD,
        "total_price_usd_wtax": TotalPriceWTaxUSD,
        "human_friendly_timestamp": dt_string,
        "products": products
    }

    client = SendGridAPIClient(SENDGRID_API_KEY)
    print("CLIENT:", type(client))

    message = Mail(from_email=SENDER_ADDRESS, to_emails=TO_ADDRESS)
    message.template_id = SENDGRID_TEMPLATE_ID
    message.dynamic_template_data = template_data
    print("MESSAGE:", type(message))

    try:
        response = client.send(message)
        print("RESPONSE:", type(response))
        print(response.status_code)
        print(response.body)
        print(response.headers)

    except Exception as err:
        print(type(err))
        print(err)


main()
