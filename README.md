# Large Scale Data Driven WSGI Application
<br />
<br />
<br />
## Pre-requisites
• Python 3.6.0 environment with having Flask and PyMongo modules are required.<br />
• For data formation and filtration script to be executed, Java SDK and JRE are must.<br />
• MongoDB 3.4.2 must be installed.

## System Deploying Guide
First of all, fork this project and then run the **_CSV_TO_JSON.java_** program while keeping the **_bbc_dataset.csv_** file in the same directory where you run this program. Eventually, you will get the **_bbc_dataset.json_** file which you will import into MongoDB by using the collection name as _‘bbc_test’_ while keeping the db name as _‘data’_. For the purpose of ease, I’ve already kept this _bbc_dataset.json_ file in this repository. <br />
After importing the produced JSON file into MongoDB, navigate to the app directory and just run this command in your command prompt **_‘python app.py’_**. After this, you can access this webbased system in your browser by typing the URL _‘127.0.0.1:5000’_. Moreover, you can also run on the specific host and port by mentioning it in the app.py file.



