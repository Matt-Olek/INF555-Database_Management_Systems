# Pubmed Database Management System - WebApp with database connection and queries in Django + PostreSQL

## Description

This project is a web application developed using Python and Django for the INF555 Database Management Systems course in Polytechnique. It aims to demonstrate the implementation of a database management system for a specific use case : the pubmed database, which contains informations about scientific publications in journals. 

## Features

- Search for **Journals**
- Search for **Authors** that have published in a specific journal
- Search for **Articles** that have been published by a specific author

## Installation

1. Clone the repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Create and configure the .env file with the database password (see .env.template). Note that it is assuming that the database named 'pubmed' is already created and populated with a user named 'postgres' (if not change it in views.py line 13). See my last submission for the database dump.
4. Run the django server using `python manage.py runserver`.
5. Access the application through the local URL : http://127.0.0.1:8000/inf553/

## Usage

1. Access the application through the local URL : http://127.0.0.1:8000/inf553/
2. Follow the on-screen instructions to perform various actions. Please note that the **search bar** is ready to us for journals and authors.
3. Explore the database using the various links and buttons.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

Matthieu OLEKHNOVITCH - Student at Ecole Polytechnique 

Mail : matthieu.olekhnovitch.2021@polytechnique.org

