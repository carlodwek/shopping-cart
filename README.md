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

## Files not Included in the Git Repo

### Enviroment Variables

In order to run the code, a .env file containing the Tax Rate, the Google Sheets IDs for both the Inventory Management dataset and the Customer Emails collector, and the Sendgrid API Key, Template ID and Sender Address must be added to the local repo folder. If you require my .env file or elements of my .env file to run the code, please let me know I would be happy to send it privately.

### Google Credentials

In order to run the code, a google-credentials.json file must be added in an auth folder in the local repo folder. This file contains the private API information required to read and write on the Goodle Sheets. Again, if you require my google-credentials.json file or elements of my google-credentials.json file to run the project, I would be happy to send it privately.

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
