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

[Model](#model)

[Django Admin](#django-admin)

[Databases](#databases)

[Admin Panel](#admin-panel)

[Tests](#tests)

[License](#license)

## Common
A Django (ver. 4.2) based blogging application with PostgreSQL management.

## Features
- Register/Login new author
- Create posts, setting certain tags and photos
- Browse the feed, consisting of different posts


## Installation & Run
Copy project from repo with git:
```bash
git clone https://github.com/Maltsew/OverPath.git
```
### Docker
#### Prerequisites

You need to have Docker Engine and Docker Compose on your machine.

#### Running
Starting working with Docker you need to use the following commands:

```bash
docker-compose build
```
After you see the message about successful build, like

`=> => writing image sha256:`\
`=> => naming to docker.io/library/`

it is possible to start the app. Run command
```bash
docker-compose up
```
At successful start the message in the console will be like:

For Django app

`washere-washere-1   | Django version 4.2.1, using settings 'WasHere.settings'`

`washere-washere-1   | Starting development server at http://0.0.0.0:8000/'`

`washere-washere-1   | Quit the server with CONTROL-C.`

For database

`washere-database-1  | 2023-05-22 21:16:42.977 UTC [1] LOG:  database system is ready to accept connections
`

After successful app launch it is necessary to run database migrations. With terminal run:

`docker-compose run --rm washere sh -c "python manage.py migrate"`

And create superuser for Django Admin

`docker-compose run --rm washere sh -c "python manage.py createsuperuser"`

Django development server is ready to work at `http://0.0.0.0:8000/`

## Model
The application the blog consists of three main models: Profile, Tag and Post.

`Profile` is based on One-To-One Django User Model and expanding it. Profile is the User, but who specified additional information on himself and also added the image of a profile.

`Tag` is representation of Posts category and also consists with a post in the Many-To-Many relation. Tags serve for improvement of navigation and search of relevant posts.

`Post` is the main model of information representation. Consists of the title and the contents. The author of the post is the registered and authorized user. Contains the obligatory image for the preview, and optional images for content. Tags are optional, but recommended.

## Django Admin
Django Admin is available on `http://0.0.0.0:8000/admin` route. \
In administrator panel are registered and available to use (display and search) of the fields in `Tag` and `Post` models.

## Databases
App using PostgreSQL management.

## Tests
Tests of the application use a Python standard library module Unittest

Run tests with `docker-compose up`:

`docker-compose run --rm washere sh -c "python manage.py test"`

## License
OverPath is released under the MIT License.