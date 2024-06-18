# Hypertrophy-App
Devyn and Hayden's Food app

### Start MySQL from scratch
    To create the table type in MySQL:

        DROP DATABASE foodprojectdb;
        CREATE DATABASE foodprojectdb;
        USE foodprojectdb;
    You must also sign into mysql as root and...
        create a user named: food
        with password: p@$$w0rd
    It needs permissions:
        GRANT CREATE, ALTER, DROP, CREATE VIEW, INSERT, UPDATE, DELETE, SELECT, REFERENCES, RELOAD on *.* TO 'food'@'localhost' WITH GRANT OPTION;
    To access the virtual environment make sure you are in:
        /FoodProject408
    There make sure to type:
        source ./venv/bin/activate
    You should see a (venv) next to your name now.
    Then enter:
        python3 frontend.py
    To run the program.


### Virtual environment setup
    Old version:
        venv/bin/python3.10 <example.py>
    Better version:
        source ./venv/bin/activate
    Turn off better version:
        deactivate

### MySQL stuff
    sudo mysql -u root -p
    USE <Database Name>;

### Resources
    https://pythonhow.com/python-tutorial/flask/Adding-CSS-styling-to-your-website/
    https://getbootstrap.com/docs
    https://chapman.udemy.com/course/the-python-mega-course
    https://chapman.udemy.com/course/the-web-developer-bootcamp
    https://chapman.udemy.com/course/web-developer-bootcamp-flask-python
    https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3#step-6-displaying-a-single-post
    https://jinja.palletsprojects.com/en/3.0.x/templates/




### Main Components
    Bootstrap
    Flask
    HTML
    PYTHON
    MYSQL

