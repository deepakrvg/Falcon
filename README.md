# Falcon
A web application to share your views and opinions and chat with others.
This is youtube link for [short demo of the project](https://youtu.be/YstsvnbNGVQ).

## Getting Started
You need to install flask for this web app to run.
Use `pip install` on requirements.txt  file to download all the dependencies.

## Setting up the Database
I have used sqlite3 database included in the cs50 library.
Once installed sqlite3, then you need to create a database using `sqlite3 falcon.db` on your terminal in same directory where you are running the project.
Then you need to create two tables, running following command one by one will create it...
- `CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, password TEXT NOT NULL);`
- `CREATE TABLE posts (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT NOT NULL, name TEXT NOT NULL, text TEXT NOT NULL, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, title TEXT, FOREIGN KEY(user_id) REFERENCES users(id));`
This will setup the database.

## Starting the Project
Once you have install all the dependencies then you need to run `flask run` command to start your flask server. 
In the terminal you will be provided with a link which is by default `https://127.0.0.1:5000/`. Open this on your browser.

#### Now you are ready to run falcon locally on your machine.

## Short Description of this project
There is a login page where you will be redirected anytime you try to visit any other page except register page. You need to register first and then login to be redirected to home page.

Once you are in you can see others posts. There's an link to posts where you can see your posts (if any), you can create a post and/or you can delete a post by providing post number.
