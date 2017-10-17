# Totally NOT a Walmart Scraper...

[![N|Solid](https://news.bitcoin.com/wp-content/uploads/2016/05/Walmart-logo.png)](https://www.walmart.com/)

Dollar_Drop is a simple program capable of finding retail arbitrage oppurtunities in a specific, unnamed, low priced department store.  Any implied affiliations with said store are purely coincidental, and no relationship exists between the creators of this program and this hypothetical department store.

This program is not valid with the following stores:

  - Petsmart
  - Kmart
  - Deal Mart

Nor is it valid with any other stores that share similar endings or pronounciation.

# New Features!

  - Literally every single feature is new


If you're making commits to this repo:
  - NO REGEX
  - re.sub(r'\d+', '', 'D130O N12OT 31U31S32E 7RE890G8E899X')
  - 'Do Not' + re.sub(r'\d+', '',' 08I3M1PO13R1T R31E8G0E809X2')
  - NO REGEX


> Each Wal-Mart store should 
> reflect the values of its
> customers and support the
> vision they hold for their community. 

~ Sam Walton of the Walmart Family Empire (Any implied relation is purely coincidental)



### Tech

Dollar_Drop uses a number of open source projects to work properly:

* Literally only Python



### Installation

~~Dollar_Drop requires you to clone [this repo](https://github.com/theriley106/Dollar_Drop) to run.~~

~~Individually go through and pip install everything or make a Requirements.txt and commit it to the repo~~

#### Windows/Linux/OSX Installation

You'll need to first install Python and [add it to your system path](https://pythongisandstuff.wordpress.com/2013/07/10/locating-python-adding-to-path-and-accessing-arcpy/)

Clone or download this Repo by either running
```
git clone https://github.com/theriley106/Dollar_Drop
```
or by downloading it from Github directroy.  I **HIGHLY** recommend downloading it using the Git command, as it allows you to update the repository with a single line of code.

Afterwards, try to run:
```
pip freeze
```
And if an error is returned you will need to install python-pip on your system by downloading [get-pip.py](https://bootstrap.pypa.io/get-pip.py) and running 
```
cd $DOWNLOADFOLDERPATH
python get-pip.py
``` 

You can exit out of this terminal, and open up a new terminal inside of the dollar_drop directory.

After this, you'll need to install all of the python modules this package depends on.  You can either do it manually or you can run

```
pip install -r requirements.txt
```

After all the requirements are installed, you'll need to start up the flask server by running 

```
python app.py
```
Afterwards, open up a web browser and go to http://0.0.0.0:8000

You can also access this site on any computer that is connected to your network by accessing http://YOURIPADDRESS:8000 from another computer.

You can find your local IP address by running

```
ipconfig
```

### Reminder

```sh
$ #Don't 
$ #Use
$ #Regex
```
