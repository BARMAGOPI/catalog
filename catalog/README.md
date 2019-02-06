# Item-Catlog

## Aim of the Application ##
This is the fourth project for the Udacity Full Stack Nanodegree. The Item Catalog project consists of developing an application that provides a list of items within a variety of categories, as well as provide a user registration and authentication system.

A user does not need to be logged in order to read the categories or items uploaded. However, users who created an item are the only users allowed to update or delete the item that they created.

This program uses third-party auth with Google. Some of the technologies used to build this application include Flask, Bootsrap and SQLite.


## Skills used for this project
1. Python
2. HTML
3. CSS
4. Flask
5. SQLAchemy
6. OAuth
7. Google Login

## Some things you might need
- [Vagrant](https://www.vagrantup.com/)
- [Udacity Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)

## Steps to run this application ##
## Getting Started
* While running this project make sure that you have proper internet connection.
* Have Vagrant and Virtual Box installed on your machine.
* Unzip the file and put the contents in the vagrant directory.
* Launch the Vagrant box (VM).

	`$ vagrant up`
	
	`$ vagrant ssh`
* To Initialize Database and To initialize the SQLite database 

	`$ python Dbcreation.py`
* To load the initial sporting categories

	`$ python Items.py`
	
	Now categories and some items belong to that category are added.
### To start the application or to run the project on the server
	`$ python MainFile.py`
* The web app will be running on your localhost at port 9000 ( http://localhost:9000/ )
* Open the above mentioned link to use the web app.
* You can only view the catalog without signing in.
* To create, update and delete the items in the catlog, sign in using Google+.
* To login using Google+
	http://localhost:9000/login to login to the app
### To Use Google Authentication Services
	We will need a client_secret.json file.
We can create an application to use Google's OAuth service at https://console.developers.google.com.
After creating and downloading client_secret.json file, move it to the directory where it is accessible to the project file.
This project uses persistent data storage to create a web application that allows users to perform Create, Read, Update, and Delete operations.
