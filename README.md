# Todo API with Flask

A set of APIs that serve a Angular.js Todo app.

## Resources
URIs relative to http://0.0.0.0:8000/

### Users 
Method    | Endpoint        |Data                   | Description              | Auth Req? | Rate Limited? 
----------|-----------------|-----------------------|--------------------------|----------------|--------
|GET      | users           |                       | list all users           | ✖             | ✖           
|POST     | users           |username<br>email<br>password<br>verify_password  | create user  | ✖ |✔
|GET      | users/id        |                        | return username          | ✖                 |✔

### Todos
Method    | Endpoint        |Data                   | Description              | Auth Req? | Rate Limited? 
----------|-----------------|-----------------------|--------------------------|----------------|--------
|GET      | api/v1/todos    |                       | return all todos         | ✖              |✖           
|POST     | api/v1/todos    |name                   | create todo              | ✔             |✔
|GET      | api/v1/todos/id |id                     | return todo detail       | ✖              |✖
|PUT      | api/v1/todos/id |name<br>edited<br>completed<br>updated_at| edit todo             | ✔             |✔
|DELETE   |api/v1/todos/id  |                       | immediately delete selected todo  | ✔           |✔

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