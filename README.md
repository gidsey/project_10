# Todo API with Flask

A set of APIs that serve a Angular.js Todo app.

## Resources
URIs relative to http://127.0.0.1:5000/ 

### Users 
Method    | Endpoint        |Data                   | Description              | Auth Req? | Rate Limited? 
----------|-----------------|-----------------------|--------------------------|----------------|--------
|GET      | users           |                       | list all users           | yes             | no           
|POST     | users           |username<br>email<br>password<br>verify_password  | create user  | no |10/day
|GET      | users/id        |                        | return username          | yes                 |no

### Todos
Method    | Endpoint        |Data                   | Description              | Auth Req? | Rate Limited? 
----------|-----------------|-----------------------|--------------------------|----------------|--------
|GET      | api/v1/todos    |                       | return all tasks     | no              |no           
|POST     | api/v1/todos    |name                   | create task         | yes             |100/hour
|GET      | api/v1/todos/id |id                     | return task detail       | no   |no
|PUT      | api/v1/todos/id |name<br>edited<br>completed<br>updated_at| edit todo  | yes -task owner only |100/hour
|DELETE   |api/v1/todos/id  |              §   | immediately delete selected todo  | yes -task owner only |100/hour

### Model Fields
Name   | Type        |Required? |
----------|-----------------|---|
|id|Primary Key|required (auto-set)|
|name|Text|required|
|edited|Boolean|not required|
|completed|Boolean|not required|
|created_at|Datetime|required (auto-set)|
|updated_at|Datetime|not required (auto-set)|

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