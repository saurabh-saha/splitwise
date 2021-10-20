# splitwise
##SETUP
###DB
* psql --version
* start [postgres](https://ooxygenated.wordpress.com/2021/02/19/start-local-postgres-server/)
* vi scripts/run_db_command.sh  
* source scripts/run_db_command.sh {edit credentials here}

###DJANGO
* pip install -r requirements.txt
* cd src
* python manage.py makemigrations
* python manage.py migrate
* python manage.py runserver

###API
* [POSTMAN LINK](https://www.getpostman.com/collections/0e4e1f7bcdeaf96a1787)
* Create User - [Register 2 -3 Users]
```bash
/api/person/register

Request
{
    "first_name" : "Ab",
    "last_name" : "B",
    "email" : "saurabh.saha123@gmail.com"
}

```

* Add an expense - {Hint: Use the user_ids returned from /register}
```bash
api/person/expense/user_id

amount
lender_id - the id of the person who lends the expense (not necessarily the person who is creating identified by user_id )
borrow_ids - list of friends who share the expense [due to simplicity no addtion of friends of supported, we directly use an /expense API to mark people as friends]
ptype
    1 - Equally shared
    2 - Percentage Shared
share_ratio - list of ratio of expense of borrowers e.x [.5, .3] , hence the lender will pay .2

Request
{
    "amount" : 4000,
    "lender_id" : 4,
    "borrow_ids" : [5,7],
    "ptype" : 2,
    "share_ratio" : [0.25,0.75]
}

```

* Find friends - Finds people in transaction with user
No seperate friends addition API is needed, friends are fetched from transaction, which check for valid
user when adding to DB
```bash
api/person/friends/user_id

Request
user_id - find friends for this user

Response:
List of people who have lended money or borrowed money from
- first_name
- last_name
- amount 
    +(positive) if money has been lended to friend
    -(negative) if money has been borrowed from friend
[
    "{\"first_name\": \"A\", \"last_name\": \"B\", \"email\": \"saurabh.saha1@gmail.com\", \"amount\": -2000}",
    "{\"first_name\": \"A\", \"last_name\": \"B\", \"email\": \"saurabh.saha@gmail.com\", \"amount\": 3000}",
    "{\"first_name\": \"Ab\", \"last_name\": \"B\", \"email\": \"saurabh.saha12@gmail.com\", \"amount\": 3000}"
]
```

* Logs - simple logs of date & value added. User might or might not be lender but is owner 
of transaction
```bash
api/person/logs/user_id
```

* Settle - Settles the expense, frontend will return the amount as returned from /friends API
Positive amount means friend is returning money
```bash
api/person/settle/user_id

Request
{
    "amount" : 4000,
    "friend_id" : 5
}
```