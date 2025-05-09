# Library Management System

Welcome to the Book Haven! This reading platform provides users with the ability to explore books.

## Introduction
The Book Spot platform boasts a user-friendly interface.
Frontend: Crafted with HTML/CSS and Bootstrap, guaranteeing an engaging and adaptable experience for users. It enables effortless navigation and book list management.

Backend: Driven by Python's Flask framework and Flask-SQLAlchemy for efficient database handling. Stores user, book, and book section list data.libraian  can effectively manage books via the backend.

## User Actions

- Search: Users can search for books.
- book Management: user send a request to libraian to read a book.
- user activty : Access statistics.


## Libraian  Actions
Dashboard: Monitor app statistics such as total users and books.
Libraian activty : Access statistics.
Book Management: Ability to remove books.
section Managment : Ability to remove section.


## Installation

Clone the repository: Navigate to the project directory.

```bash
  pip install -r requirements.txt
```

## How to use
Before we could use the web app, we need to setup the environment and servers for it.
1) <b>Setting up  virtual environment : <b>
    - In a new Linux terminal tab, activate a virtual environment
            source myenv/bin/activate
          
2) <b>Setting up the Flask server :</b>   
   - In a new Linux terminal tab, start the Flask server by typing 

             python3 main.py

3) <b> Setting up Redis server : </b>    
    - In a new Linux terminal tab, start the redis server by typing 

          redis-server
    
4) <b> Setting up Celery Worker and Celery Beat : </b>
    - In a new Linux terminal tab, start the Celery Workers and Beat together by typing 
    
          celery -A tasks.celery worker --loglevel INFO    

5) for checking whether the reports have been sent or not - 'MailHog'
