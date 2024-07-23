# OTEL PROJECT 
### Description
Hi. This is a simple Flask (python) application that makes database calls to store "Users" and "Couches".

DBs are stores in the `instance` folder. You can specify a new one by changing the string in `app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test1.db"` in the main python file to "sqlite:///<whatever-name>.db".

It is broken down into two suites of endpoints -- one for Users, one for Couches

1. list things
    * /users
    * /couches

2. create thing
    * /users/create
    * /couches/create

3. delete thing (the first 2 delete the given ID, second 2 give a form asking for an id to delete)
    * /user/id/delete
    * /couch/id/delete
    * /users/delete
    * /couches/delete

4. get specific thing
    * /user/id
    * /couch/id

Then finally there's a `/bootstrap` endpoint that will populate a new DB with values
> note that calling this twice for the same DB will cause an error as entries must be unique. that being said, if you're testing APM, this is an easy way to generate errors!

### Dependencies
`pip install flask`
`pip install -U Flask-SQLAlchemy`
`pip install sqlalchemy`
`pip install sqlalchemy.orm`