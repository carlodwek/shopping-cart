# Python Shopping Cart Project for OPIM 243

## Summary

This is a Python applciation that acts as a supermarket checkout machine, outputting a receipt.

## Setup

### Repo Setup

Clone this repo to your computer.

After cloning the repo, navigate there from the command-line:

```sh
cd ~/[File Location]/shopping-cart
```

### Environment Setup

Create and activate a new project-specific Anaconda virtual environment:

```sh
conda create -n shopping-env python=3.8 # (first time only)
conda activate shopping-env
```

Download the required packages (first time only):

```sh
pip install -r requirements.txt
```

### Files not Included in the Git Repo

#### Enviroment Variables

In order to run the code, a .env file containing the variables TAX_RATE (decimal format), GOOGLE_SHEET_ID (1v8Xv_xGytBmDlpLokqatS55fCl9SnA8WhXWlmC06Bx0), GOOGLE_SHEET_ID2 (1dybCYFjFJpNoD1oDB04W3u2xdp_2vCRa6gbo2ajz4iI), SENDGRID_TEMPLATE_ID (d-8ff5185e8fab423799abc8a5593e397f), SENDER_ADDRESS and SENDGRID_API_KEY must be set up.

First, [sign up for a SendGrid account](https://signup.sendgrid.com/), then follow the instructions to complete your "Single Sender Verification", clicking the link in a confirmation email to verify your account.

Then [create a SendGrid API Key](https://app.sendgrid.com/settings/api_keys) with "full access" permissions. We'll want to store the API Key value in the enviroment variable `SENDGRID_API_KEY`.

Set `SENDER_ADDRESS` to be the same email address as the single sender address you just associated with your SendGrid account (e.g. "abc123@gmail.com").

#### Google Credentials

In order to run the code, a google-credentials.json file must be added in an auth folder in the local repo folder. This file contains the private API information required to read and write on the Goodle Sheets.

Visit the [Google Developer Console](https://console.developers.google.com/cloud-resource-manager). Create a new project, or select an existing one. Click on your project, then from the project page, search for the "Google Sheets API" and enable it. Also search for the "Google Drive API" and enable it.

From either API page, or from the [API Credentials](https://console.developers.google.com/apis/credentials) page, follow a process to create and download credentials to use the APIs:
  1. Click "Create Credentials" for a "Service Account". Follow the prompt to create a new service account named something like "spreadsheet-service", and add a role of "Editor".
  2. Click on the newly created service account from the "Service Accounts" section, and click "Add Key" to create a new "JSON" credentials file for that service account. Download the resulting .json file (this might happen automatically).
  3. Move a copy of the credentials file into your project repository, typically into the root directory or perhaps a directory called "auth", and note its filepath. For the example below, we'll refer to a file called "google-credentials.json" in an "auth" directory (i.e. "auth/google-credentials.json").

Finally, modify the google sheets' sharing settings to grant "edit" privileges to the "client email" address specified in the credentials file.

## Instructions

Run the program from the command-line:

```sh
python shopping_cart.py
```

On opening, the application will automatically sync its inventory of available items to the Google Sheet Inventory management system found [here.](https://docs.google.com/spreadsheets/d/1v8Xv_xGytBmDlpLokqatS55fCl9SnA8WhXWlmC06Bx0/edit?usp=sharing)

### Main Menu

You will then enter the main menu and be prompted to select either "new cart", "sync inventory" or "exit". The commands are not case sensitive and can be entered without a space.
* "sync inventory" will update the code's inventory list to match the one in the provided Google Sheets.
* "exit" is the required step if you want to exit the program.
* "new cart" will start a new cart run the rest of the code's functionality.

### New Cart

You will now be prompted to enter the product identifiers for the products you require.
* A confirmation message will tell you what item you've added to the cart.
* If your identifier was not found in the inventory, you will be notified and prompted to try again.
* If you input the identifier of a product with a price per pound, you will be prompted to enter the amount of pounds you are purchasing.

As the prompt will repeat to you, please input "done" (not case sensitive) to complete the cart.

### Receipt

The system will then output your receipt in the command line, and save a timestamped copy to the receipts folder for safekeeping.

It will then prompt you on whether you would like your receipt emailed to you. Enter "yes" or "y" (not case sensitive) to proceed. Entering anything else will end the portion of the program.
* If you decide to proceed, you will be prompted to enter your email.
* You will then be asked if you want your email to be stored in the [Customer Email Database.](https://docs.google.com/spreadsheets/d/1dybCYFjFJpNoD1oDB04W3u2xdp_2vCRa6gbo2ajz4iI/edit?usp=sharing) Again "yes" or "y" (not case sensitive) will work and anything else will move on.

### Conclusion

Finally, you will be sent back to the Main Menu, ready for another shopper. Remember to enter "exit" to exit the program entirely.

Thanks for your attention!
