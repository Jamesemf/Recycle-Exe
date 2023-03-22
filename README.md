# Introduction

Rec-Ex is a web application that promotes sustainability on the University of Exeter Streatham Campus by encouraging
and helping users to recycle. It contains information on products including their name, weight, material, and whether
they can be recycled or not. It helps users by allowing them to scan the barcode of a product, and navigating them
to a nearby bin on campus where the product can be recycled. Users may also view the map page to see where all bins on 
campus are located. The application encourages users to recycle products in this way by rewarding them with points each 
time they recycle an item at one of the bins located on campus. These points then determine a user's position on the
leaderboard, so that they may compete with other users to gain the most points from recycling products. 
The points can also be spent in the shop to gain real world rewards. The application also stores statistics about a 
user's recycling habits and allows a user to set themselves goals about the number of products that they would like to 
recycle. Finally, the application provides a gamekeeper page for staff members to access where they can create new bin
locations, new goals for users to choose from, and new shop items for users to purchase.

## Open Source Barcode Reader : Educational Use 

Note within the directory ```staticfiles``` there is a directory named ```BCscanner```. This is open source that has an Apache License 
meaning we are able to use it for educational uses and modify it as need be (which we have done). This software provides 
a barcode reader in our project. Here is the GitHub source where we have source this open source software ```https://github.com/mebjas/html5-qrcode```.

## Usage

- To run this application, please use Python 3.11 or visit ```https://www.bytebrigade.net``` where it is hosted

- EXECUTING CODE:
To run this application locally, navigate to the bytebrigade directory and run:

   python manage.py runserver

   Then go to ```http://127.0.0.1:8000/```


- NAVBAR: 
The navbar located at the top of the page is the main method of navigation for the application. It can be used
to navigate to the leaderboard, how to work, map, gamekeeper (if the user has staff permissions), and account pages. 
Clicking on the account dropdown menu will allow the user to select their profile page, the shop page, or log out of
their account.


- LOGIN PAGE:
This page allows a user to enter a username and password to login, or click "Sign Up!" to be redirected
the registration page where they may register an account.


- HOME PAGE: 
The home page contains a daily feed where users may view the most recent items recycled. Each transaction
contains the time that the item was recycled, the user that recycled the item, the product that was recycled, and the
name of the bin that the product was recycled at. Users may also like these transactions and the number of likes will be
displayed next to the transaction. The home page also contains a "Scan Item" button which will navigate to the scanner
page.


- LEADERBOARD: 
The leaderboard page contains a table with the ranking of users based on the number of points they have
from recycling. A user may also enter a username in the search bar to search for a user's ranking on the leaderboard.


- HOW TO WORK?: 
The "How to work?" or "About Me" page is an instructional page that will give users some guidance on how
to use the application. It contains some advice on basic usage of the applications, including recycling items and adding
goals to the profile page. There are also images demonstrating how to use the different features that the app provides.


- SCANNER: 
The scanner page allows users to scan an item that they wish to recycle. Clicking the "Scan Item" button on
the home page will redirect the user to a page requesting camera permission. The user can then select a camera and click
"Start Scanning" which will bring up a video feed. The user then simply has to position a barcode in the scanning area,
and it will be automatically detected. If the product has not yet been registered in the application's database, the 
user  will be redirected to a page where they can enter a new product. Once they have entered the product's name and 
weight, and selected the material and whether it can be recycled or not, they will then be redirected to the product's
page. If the product has already been registered, then the user will be redirected straight to the product's page.


- PRODUCT PAGE:
The product page contains information about a product, including its name, weight, whether It's
recyclable or not, and which bin it should be put in. The user can press the "Would you like to Recycle?" button in
order to recycle the product. They will then be navigated to the map page where a bin has been selected for them to
recycle the product in, and a button is displayed with the text "Would you like to start your adventure?". They will
then be redirected to the navigation page.


- NAVIGATION PAGE: 
The navigation page directs a user to a selected bin. It contains an arrow pointing them to the bin
and tells them the distance that they currently are from the bin. When the user reaches the bin, they will be navigated
to the recycle confirm page in order to confirm the transaction.


- MAP: 
The map page contains a map of the bins on campus. A user can select one of the bins to view information about it
, or they can filter bins based on the type of items the recycle to only view bins of a certain type using the drop-down
menu at the bottom of the page.


- PROFILE: 
The profile page allows users to view information about their recycling habits, including their points, 
carbon footprint, and their recent recycling habits. A user may also use the profile page to manage their account
settings (such as changing their password or their profile picture). Additionally, the account page allows users
to set up to three goals for themselves. The user can select a goal using the "Add a goal!" widget where they can choose
which goal number they would like to edit, the number of items that they would like to recycle, and the type of item
that they would like to recycle. Finally, the profile page contains information about where a user is in relation to
other users in terms of amount recycled. It compares recycling over the past week, month, and year.


- SHOP: 
The shop page is where users can spend their points gained from recycling on a range of rewards that will be
listed on the page. The user can purchase an item from the shop, provided that they have enough points to buy it, 
causing this number of points to be deducted from their account. They will then receive an email containing a QR code
and instructions on how to redeem their reward at a shop on campus.


- GAMEKEEPER: 
The gamekeeper page is a page only available to users with staff permissions. The user can use this page
to create to add new bins, goals, and shop items, as well as delete existing ones. The purpose of this page is to
provide an easy way for administrators and other approved individuals to manage the applications database.


## Static/Templates File Structure

Within this repository the django staticfiles model have been used. Therefore, the static file structure is following 
Django staticfiles distribution.
```
  FOR EACH APPLICATION:
  <application folder>
    ├── static                      # Static file for specific application(JS/CSS and figures etc.).
    ├── templates                   # Templates file for specific application.
    ├── ...
  
  FOR GENERAL STATIC(BASE_DIR / "statics"):
  statics
    ├── assets                      # General boostrap css/js been used.
    ├── figures                     # General use figures (database, icon etc.).
    ├── style                       # General style css that modified for overriding boostrap.
    ├── templates                   # General template to be inheritant by other app templates. (navbar.html etc.)
    └── favicon.ico                 # favicon
    
  FOR PRODUCTION COLLECTED STATIC: All static file (both under application folder and statics folder) need to be collected
  into STATIC_ROOT folder for publish. (with DEBUG=False) Follow command need to be used:
```
**Command:**   ```py manage.py collectstatic```



## File Structure

Within this repository there is a complex file structure. In the main directory it contains all GitHub files, Django Files,
and Document Files

```
  .
  ├── .github                       # All GitHub files, including action files.
  ├── bytebrigade                   # All Django files, Applications and Root file.
  ├── Requirements.md               # Our Requirements file containing all dependencies needed in order for the system to function.
  ├── Byte_Brigade_Privacy_Policy   # Our Privacy Policy file detailing how we manage and process users data.
  ├── LICENSE.md                    # Out License file, contain our legal obligations.
  └── README.md                     # Our README file which details how the system functions from a developers point of view.

  bytebrigade
  ├── account                       # This application directory contains all files referring to user and admin accounts in the system.
  ├── barcodereader                 # This application barcodereader, contains all models and functions which this application uses.
  ├── bins                          # This application bins, it contains all models and functions which this application uses.
  ├── bytebrigade                   # This application directory contains all files referring to the root file.
  ├── gamekeeper                    # This application gamekeeper, contains all models and functions which this application uses.
  ├── home                          # This application home, contains all models and functions which this application uses.
  ├── products                      # This application products, contains all models and functions which this application uses.
  └── shop                          # This application shop, contains all models and functions which this application uses.
```
## Application Structure

The application is structured into 7 separate applications each with a devoted purpose. 

The application structured is following this pattern:
```
  <application folder>
    ├── migrations                 # Database schema migration files
    ├── static                     # Static files (CSS, JS, images, etc.)
    ├── templates                  # HTML templates for rendering views
    ├── __init__.py                # Empty file to mark this as a Python package
    ├── admin.py                   # Customize the admin interface for models
    ├── apps.py                    # Application configuration settings
    ├── forms.py                   # Form classes for handling user input
    ├── models.py                  # Define application models (fields and methods)
    ├── tests.py                   # Test cases for the application
    ├── urls.py                    # URL routing for the application
    └── views.py                   # View functions to handle user requests
```

- ACCOUNT:
The account application is responsible for all account registration and management function. It also
provides the function for creating user goals and changing user statistics. It contains the templates for 
user profiles, account registration and logging in/out, and password changing/resetting. The models contained within
the application are that of user statistics, goals that users can choose from, and a users individual goals.


- BARCODE READER:
The barcode reader application contains the functionality for scanning a barcode and redirecting to the correct
page depending on if the product exists in the database or not. It also contains the functionality for when a
recycling transaction takes place and adding the points gained for a transaction to a user's statistics. The application
contains the template for the scanner page, and provides no models for the application.


- BIN:
The bin application contains functionality for the bin map and bin navigation aspects of the site. The templates
provided by this application are the bin map page, the bin navigation page, and the page for when a user has arrived at
the destination bin. This application also provides the model for storing data about bins.


- GAMEKEEPER:
This gamekeeper application contains the functionality for all actions exclusively performed by users with staff
permissions such as creating and deleting bins, goals, and shop items. It also contains the template for the 
gamekeeper page. This application provides no models, as its functionality only involves accessing and updating
the models from other applications.


- HOME:
This application contains the functionality for the transactions located on the home page, as well as displaying the
leaderboard and instruction pages. It is also responsible for initialising many of the values used throughout the
application as well as resetting them when an operation has been complete. The application provides the templates for
the home page, the leaderboard page, and the about me page. The application also contains the model for user
transactions.


- PRODUCTS:
This application contains the functionality for creating products and viewing product information. It also contains
the functionality for identifying which bin a product should be recycled into. This application provides the templates
for viewing product information (product info and pokedex) and creating new products. The product model is also
contained within this application.


- SHOP:
This application contains the functionality for the shop page, including displaying shop items and processing
purchases. The application contains the templates for the shop page, and the email a user will receive upon purchasing
an item. This application also contains the model for a shop item that will be displayed in the shop.


## Testing

This application was tested using the django TestCase and Client modules. The tests are located in each application's
tests.py file. To run the tests, enter:

```python manage.py test```

in the terminal.

We have also included our tests with GitHub Actions. Anytime you pull or push from the main the command above will execute.

## Appendix

GitHub: https://github.com/Jamesemf/ECM2434---Group-13
