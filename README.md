# OverPath

## About
OverPath - it is a blog representing the platform for those who want to share the travel with other people.
Here you can create an own post, having told about the place which you visited.\
Create categories for the posts - so it will be easier for other users to find content interesting them.\
Add the photo to share the impressions and to inspire others on new adventures. \
OverPath - the perfect place for those who like to travel and look for new places for a research.

## Content
[About](#about)

[Common](#common)

[Features](#features)

[Installation](#installation)

[Extra Dependences](#extra-dependences)

[Model](#model)

[Django Admin](#django-admin)

[Databases](#databases)

[Admin Panel](#admin-panel)

[Tests](#tests)

[License](#license)

## Common
A Django (ver. 3.2) based blogging application with PostgreSQL management.

## Features
- Register/Login new author
- Create posts, setting certain tags and photos
- Browse the feed, consisting of different posts


## Installation
123

## Extra Dependences
[transliterate](http://pypi.com) - An additional package which gives an opportunity for the translation of the text from Latin in Cyrillics

## Model
The application the blog consists of three main models: Profile, Tag and Post.

`Profile` is based on One-To-One Django User Model and expanding it. Profile is the User, but who specified additional information on himself and also added the image of a profile.

`Tag` is representation of Posts category and also consists with a post in the Many-To-Many relation. Tags serve for improvement of navigation and search of relevant posts.

`Post` is the main model of information representation. Consists of the title and the contents. The author of the post is the registered and authorized user. Contains the obligatory image for the preview, and optional images for content. Tags are optional, but recommended.

## Django Admin
Django Admin is available on `http://host/admin` route. \
In administrator panel are registered and available to use (display and search) of the fields in `Tag` and `Post` models.

## Databases
By default in the app the PostgreSQL is used.\
The database configuration is defined in the `settings.py` file and by default makes:
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.DB_NAME,
        'USER': env.DB_USER,
        'PASSWORD': secrets.DB_PASSWORD,
        'HOST': env.DB_HOST,
        'PORT': env.DB_PORT,
    }
}
```
The best method of vars storage - not to specify variables directly, but to use variable environments

(https://) /best practice

```bash
intall
```

## Tests
Tests of the application use a Python standard library module: unittest. This module defines tests using a class-based approach.

Application works under a PostgreSQL system, therefore for carrying out tests it is necessary to configure creation of the test database.
By default system PostgreSQL does not permit the common user to create base, it is the opportunity it is necessary to specify obviously. For this purpose it is possible to use the command `ALTER USER *your_db_user* CREATEDB;`to the your owner of the database.

Then use:

`./manage.py test blog` run all tests,

Or:

`./manage.py test blog.tests.test_models, ./manage.py test blog.tests.test_views, ./manage.py test blog.tests.test_urls` running to chosen functionality in test_models, test_views, test_urls files.


## License
OverPath is released under the MIT License.