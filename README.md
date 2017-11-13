# TechLurker


### About Our Product
TechLurker is an app which gives up to date information on all of the latest news in the tech industry. We use a web crawler to get the news from various tech sites and return it to our users in an interesting and easy to understand manner. Choose from one of our built in starting points or input your own favorite site and see what interesting information gets returned to you.

### Meet the Team
[Han Bao](https://github.com/han8909227)

[Phillip Werner](https://github.com/philipwerner)

[Brian Wheeler](https://github.com/PoundsXD)

[Max Wolff](https://github.com/maxawolff)

##**Routes:**

| Route | Route Name | Description |
| --- | --- | --- |
| /  | home | the home page |
| /results | results | Display results from web scrape |
| /results/{id:\d+} | saved_results | Display historical data from prior scrapes |
| /about | about | Information on dev team |

##**Set Up and Installation:**
Clone this repository to your local machine.
```
$ git clone https://github.com/han8909227/TechLurker.git
```
Once downloaded, cd into the ```TechLurker``` directory.
```
$ cd Techlurker
```
Begin a new virtual environment with Python 3 and activate it.
```
TechLurker $ python3 -m venv ENV
TechLurker $ source ENV/bin/activate
```
[pip](https://pip.pypa.io/en/stable) install this package as well as the testing set of extras into your virtual enviroment.
```
(ENV) TechLurker $ pip install -e .[testing]
```
Create a Postgress datatbase for use with this application. Export an environment variable pointing to the location of your data configuration.
```
(ENV) TechLurker $ createdb 
(ENV) TechLurker $ export DATABASE_URL='postgress://localhost:5432/'
(ENV) TechLurker $ initdb development.ini
```
Once the package is installed and the database is created, serve the application using the ```pserve``` command.
```
(ENV) TechLurker $ pserve development.ini
```
##**To Test**
If you have the testing extras installed, testing is simple. If you're in the same directory as setup.py type the following:
$ py.test TechLurker

##**Built With:**
[Pyramid Framework](https://trypyramid.com)
[Cookiecutter-PyPackage](https://github.com/audreyr/cookiecutter)
[Start Bootstrap](https://startbootstrap.com/template-overviews/bare/)
