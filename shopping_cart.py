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
    print("Shopping Cart Interface")
    print("-----------------------")
    products = GetProducts()
    #print(products)
    print("Inventory Updated")
    print()
    check = True
    while check == True:
        print("MAIN MENU")
        choice = input("Please input 'new cart' or 'update inventory' or 'exit': ")
        choice = choice.lower()
        if choice == "new cart" or choice == "newcart":
            cart = Cart(products)
            SubTotal = GetTotal(cart)
            Tax = TaxTotal(SubTotal)
            Total = SubTotal+Tax
            SubTotalUSD = to_usd(SubTotal)
            TaxUSD = to_usd(Tax)
            TotalUSD = to_usd(Total)
            for i in cart:
                input()
                print(cart)
                i["price"] = to_usd(float(i["price"]))
                print(cart)
            #CommandLineOutput(cart, SubTotalUSD,TaxUSD,TotalUSD)
            #WriteReceiptFile(cart, SubTotalUSD,TaxUSD,TotalUSD)
            choice2 = input("Would you like an email receipt? ")
            choice2 = choice2.lower()
            if choice2 == "yes" or choice2 == "y":
                TO_ADDRESS = input("Email: ")
                SendEmail(TO_ADDRESS, SubTotalUSD,TaxUSD,TotalUSD, cart)
                choice3 = input("Would you like to opt-in to the customer loyalty program?")
                choice3 = choice3.lower()
                if choice3 == "yes" or choice3 == "y":
                    OptIn(TO_ADDRESS)
            print("Thank you for shopping with us today!")
        elif choice == "update inventory" or choice == "updateinventory":
            products = GetProducts()
            print("Inventory Updated")
        elif choice == "exit":
            check = False
        else:
            print("Invalid selection.")






def to_usd(my_price):
    return f"${my_price:,.2f}" #> $12,000.71

def GetTotal(cart):
    prices = [item["price"] for item in cart]
    SubTotal = sum(prices)
    return SubTotal

def TaxTotal(TotalPrice):
    TAX_RATE = os.getenv("TAX_RATE", default="OOPS, please set env var called 'TAX_RATE'")
    if TAX_RATE == "OOPS, please set env var called 'TAX_RATE'":
        print(TAX_RATE)
    else:
        Tax = TotalPrice*float(TAX_RATE)
        return Tax

def Cart(products):
    check = True
    cart = []
    print(products)
    ids = [item["id"] for item in products]
    while check == True:
        selectionid = input("Please input a product identifier (input 'done' when finished): ")
        if selectionid == "done" or selectionid == "DONE" or selectionid == "Done":
            check = False
        elif selectionid in ids:
            selectionl = [item for item in products if item["id"] == int(selectionid)]
            selection = selectionl[0]
            if selection["price_per"] == "pound":
                pounds = input("Pounds? ")
                print(selection["price"])
                selection["price"] = float(pounds)*(selection["price"])
                print(selection["price"])
            cart.append(selection)
            print(selection["name"], "added to cart.")
        else:
            "Invalid identifier."
    print(cart)
    return cart

def CommandLineOutput(cart, SubTotalUSD,TaxUSD,TotalUSD):
    return

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
    # print(rows)
    # for row in rows:
    #     print(row) #> <class 'dict'>
    return rows

def OptIn(TO_ADDRESS):

    DOCUMENT_ID = os.getenv("GOOGLE_SHEET_ID2", default="OOPS")
    SHEET_NAME = os.getenv("SHEET_NAME2", default="Customer Emails")

    CREDENTIALS_FILEPATH = os.path.join(os.path.dirname(__file__), "auth", "google-credentials.json")

    AUTH_SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets", #> Allows read/write access to the user's sheets and their properties.
        "https://www.googleapis.com/auth/drive.file" #> Per-file access to files created or opened by the app.
    ]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILEPATH, AUTH_SCOPE)
    print("CREDS:", type(credentials)) #> <class 'oauth2client.service_account.ServiceAccountCredentials'>

    client = gspread.authorize(credentials)
    print("CLIENT:", type(client)) #> <class 'gspread.client.Client'>
    doc = client.open_by_key(DOCUMENT_ID)
    print("DOC:", type(doc), doc.title) #> <class 'gspread.models.Spreadsheet'>

    sheet = doc.worksheet(SHEET_NAME)
    print("SHEET:", type(sheet), sheet.title)#> <class 'gspread.models.Worksheet'>

    rows = sheet.get_all_records()
    print("ROWS:", type(rows)) #> <class 'list'>
    print(rows)
    for row in rows:
        print(row) #> <class 'dict'>
    #
    # WRITE VALUES TO SHEET
    #
    # see: https://gspread.readthedocs.io/en/latest/api.html#gspread.models.Worksheet.insert_row

    # print("-----------------")
    # print("NEW ROW...")
    #
    auto_incremented_id = len(rows) + 1 # TODO: should change this to be one greater than the current maximum id value
    new_row = TO_ADDRESS
    print(new_row)
    #
    # print("-----------------")
    # print("WRITING VALUES TO DOCUMENT...")
    #
    # # the sheet's insert_row() method wants our data to be in this format (see docs):
    new_values = [new_row]
    #
    # # the sheet's insert_row() method wants us to pass the row number where this will be inserted (see docs):
    next_row_number = len(rows) + 2 # number of records, plus a header row, plus one
    #
    response = sheet.insert_row(new_values, next_row_number)
    #
    print("RESPONSE:", type(response)) #> dict
    print(response) #> {'spreadsheetId': '____', 'updatedRange': "'Products-2021'!A9:E9", 'updatedRows': 1, 'updatedColumns': 5, 'updatedCells': 5}

def SendEmail(TO_ADDRESS, SubTotalUSD,TaxUSD, TotalUSD, cart):
    ## Email code
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", default="OOPS, please set env var called 'SENDGRID_API_KEY'")
    SENDGRID_TEMPLATE_ID = os.getenv("SENDGRID_TEMPLATE_ID", default="OOPS, please set env var called 'SENDGRID_TEMPLATE_ID'")
    SENDER_ADDRESS = os.getenv("SENDER_ADDRESS", default="OOPS, please set env var called 'SENDER_ADDRESS'")

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    # this must match the test data structure
    template_data = {
        "total_price_usd": SubTotalUSD,
        "tax": TaxUSD,
        "total_price_usd_wtax": TotalUSD,
        "human_friendly_timestamp": dt_string,
        "products": cart
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
