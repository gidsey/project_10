# Todo API with Flask

A set of APIs that serve a Angular.js Todo app.

## Resources
URIs relative to http://127.0.0.1:5000/ 

### Users 
Method    | Endpoint        |Data                   | Description              | Auth Req? | Rate Limited? 
----------|-----------------|-----------------------|--------------------------|----------------|--------
|GET      | users           |                       | list all users           | wip             | wip           
|POST     | users           |username<br>email<br>password<br>verify_password  | create user  | wip |wip
|GET      | users/id        |                        | return username          | wip                 |wip

### Todos
Method    | Endpoint        |Data                   | Description              | Auth Req? | Rate Limited? 
----------|-----------------|-----------------------|--------------------------|----------------|--------
|GET      | api/v1/todos    |                       | return all todos         | wip              |wip           
|POST     | api/v1/todos    |name                   | create todo              | wip             |wip
|GET      | api/v1/todos/id |id                     | return todo detail       | wip              |wip
PUT      | api/v1/todos/id |name<br>edited<br>completed<br>updated_at| edit todo             | wip             |wip
|DELETE   |api/v1/todos/id  |                       | immediately delete selected todo  | wip           |wip

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