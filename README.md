"# bdcalling_task" 

--- How To Setup MySql ---
First of all- If you do not have mysql installed here is the link: https://dev.mysql.com/downloads/mysql/


1. If on linux 

    run: sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
2. If on Windows
    You might need to install Visual Studio Build Tools or use pre-compiled binaries.
    (Link: https://visualstudio.microsoft.com/visual-cpp-build-tools/)

3. Create a new database for your Django project:
    run: CREATE DATABASE your_database_name;
4. Create user and give permissions:

    run: CREATE USER 'your_username'@'localhost' IDENTIFIED BY 'your_password';

    run: GRANT ALL PRIVILEGES ON your_database_name.* TO 'your_username'@'localhost';

    run: FLUSH PRIVILEGES;

5. In the root directory of Django project (where manage.py is located), create a file named .env

6. Then add these fields:

DB_NAME=your_database_name

DB_USER=your_username

DB_PASSWORD=your_password

DB_HOST=localhost

DB_PORT=3306



7. In your virtual environment of your django project

    Run: pip install mysqlclient


8. In settings.py change your database like:


DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),  
        'PORT': config('DB_PORT', default='3306'),    

    }

}



--- How To Run the Django project ---
1. Make sure you have python installed
2. Open terminal in your desired folder and and create a virtual environment (For my case, I used pipenv)
3. Run: pip install -r requirements.txt
4. Run: python manage.py makemigrations
5. Run: python manage.py migrate
6. Run: python manage.py runserver