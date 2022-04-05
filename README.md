# JSC Order Tracker

[![CodeFactor](https://www.codefactor.io/repository/github/sandboxed-thoughts/jsc-order-tracking/badge)](https://www.codefactor.io/repository/github/sandboxed-thoughts/jsc-order-tracking)&emsp;![django workflow](https://github.com/sandboxed-thoughts/jscorder/actions/workflows/django.yml/badge.svg)

A django application designed to track concrete and gravel deliveries from the perspective of a middleman. Clients call into the company and place an order requesting a specific date and time of delivery. The company then places the orders with the same specifications to the supplier. Once the order has been placed with the supplier, a delivery schedule is updated with the order, who's delivering it, and the progress of the delivery.

---

❗ Attention

  This project uses [PostgreSQL](https://www.postgresql.org/download/) to run its database. Please, be sure to have PostgreSQL installed and running with the proper permissions loaded on a postgres user to manage your development database.
  
  This project also assumes you have a basic understanding and the ability to run a django application in development. If you are not sure of the basic development settings, I highly encourage you to [read the documentation](https://www.djangoproject.com/).

  You can read information about setting up a basic django app using PostgreSQL in [this](https://www.section.io/engineering-education/django-app-using-postgresql-database/) section.io article. The following instructions will **not** cover every requirement to build your development environment.
  
  If you need some additional assistance in making heads-or-tails of the directory structure, please take a look at Simple is Better Than Complex's article [How to Start a Production-Ready Django Project](https://simpleisbetterthancomplex.com/tutorial/2021/06/27/how-to-start-a-production-ready-django-project.html).

---

## Getting Started

### Initial Setup

1. Set up the PostgreSQL database and user

   1. Create your database

      `CREATE DATABASE dbname;`

   1. Create your user

      `CREATE USER dbuser WITH ENCRYPTED PASSWORD password;`

   1. Grant your user access to the database

      `GRANT ALL PRIVILEGES ON DATABASE dbname TO dbuser;` \

   1. Give your local user the ability to CREATE databases (used to build the test database)

      `ALTER USER dbuser CREATEDB`

1. Clone this repository

   `git clone git@github.com:sandboxed-thoughts/jscorder.git`

1. Navigate into the project directory

1. Copy `.env.example` to a new file `.env` in the same folder

1. Install and activate your virtualenvironment

   `python -m virtualenv ./env`

   `. ./env/bin/activate`

1. Install the required packages

   `python -m pip install -r requirements/local.txt`

1. Navigate into `project/`

1. Migrate the data structures to your database

   `python manage.py migrate`

1. Update your `.env` file with the appropriate information to suit your development environment.

---

#### Helpful Links on Concrete

- [all about concrete](http://deeconcrete.com/concrete/)
