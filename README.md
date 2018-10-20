# Question-Answer App
### Technologies
* Python
* Flask
* SQLite3
* HTML
* Bootstrap 3

### About the App
This app enable a user to ask and answer questions. Depending what user access
the admin provided - If a user is a 'regular' user, the only ability he or she has is to ask questions.
If a user is an 'expert' user, the only ability that he or she has is to answer questions.

An admin can promote regular users to an expert via the 'User Set Up' page. The main homepage shows the list of 
questions that have been answered as well as information on which user has asked/answered the questions.


### Reflection
Things I've learnt with this app:

* Creating schema to accommodate the assignment of user roles (admin, expert, regular user)
* Login/Register access and storing information on the POST request to SQLite3 database
* Python library makes easy! With the library werkzeug.security, it is very simple to hash and verify users password

```
from werkzeug.security import generate_password_hash, check_password_hash
```

```
from flask import Flask, session
```

* Injecting the real QUERY style looking SQL query to the app.py application.

```
    db = get_db()
    answer_cur = db.execute('''
                    SELECT
                        q.id AS id, q.question_text AS question_text, 
                        q.answer_text AS answer_text, u.name AS asked_user , 
                        u2.name AS expert_user
                    FROM
                        questions q
                        JOIN users u ON u.id = q.asked_by_id
                        JOIN users u2 ON u2.id = q.expert_id
                    WHERE
                        q.id = ?                
    ''', [question_id])
    answer_result = answer_cur.fetchone()
</code>
```
* Putting constraint so that the same user cannot register to the app twice
* Protecting routes so only logged-in user can access

### Preview #1

![alt text](https://github.com/promie/question-answer/blob/master/static/img/1.png "Main App")

### Preview #2

![alt text](https://github.com/promie/question-answer/blob/master/static/img/2.png "Main App")

### Preview #3

![alt text](https://github.com/promie/question-answer/blob/master/static/img/3.png "Main App")

### Preview #4

![alt text](https://github.com/promie/question-answer/blob/master/static/img/4.png "Main App")

### Preview #5

![alt text](https://github.com/promie/question-answer/blob/master/static/img/5.png "Main App")


