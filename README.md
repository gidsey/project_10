# Todo API with Flask

A set of APIs that serve a Angular.js Todo app, combined with a user model for authentication.

## Parameters

Users must be authenticated in order to create, edit or delete tasks.
Tasks can only be edited or deleted by their owner.

Anonymous users will see all tasks listed. 
Logged in user will see their own tasks.

## Resources
URIs relative to http://127.0.0.1:5000/ 

### Users 
Method    | Endpoint        |Data                   | Description              | Auth Req? | Rate Limited? 
----------|-----------------|-----------------------|--------------------------|----------------|--------
|GET      | api/v1/users           |                       | list all users           | yes             | no           
|POST     | api/v1/users           |username<br>email<br>password<br>verify_password  | create user  | no |10/day
|GET      | api/v1/users/id        |                        | return username          | yes                 |no

### Todos
Method    | Endpoint        |Data                   | Description              | Auth Req? | Rate Limited? 
----------|-----------------|-----------------------|--------------------------|----------------|--------
|GET      | api/v1/todos    |                       | return all tasks     | no              |no           
|POST     | api/v1/todos    |name                   | create task         | yes             |100/hour
|GET      | api/v1/todos/id |id                     | return task detail       | no   |no
|PUT      | api/v1/todos/id |name<br>edited<br>completed<br>updated_at| edit todo  | yes -task owner only |100/hour
|DELETE   |api/v1/todos/id  |                 |delete selected task  | yes -task owner only |100/hour


## Unit tests



## Running Locally

```bash
git clone https://github.com/gidsey/project_10.git
```

From within project folder:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

```bash
 python3 app.py
```