<h1 align="center">Melp Restaurants API</h1>

Restful API for managing restaurants. Written in Python using FastAPI.
<br>

### Live Demo
https://melp-restaurants-api.onrender.com

<br>

## Table of Content 📑
---
- [Project Folder Structure 📂](#project-folder-structure-📂)
- [Features 🚀](#features-🚀)
    - [Endpoints 🌐](#endpoints-🌐)
- [How to run the code 🏃‍♂️](#how-to-run-the-code-🏃‍♂️)
    - [Installation 🔧](#installation-🔧)
- [Installing project's dependencies 📚](#installing-projects-dependencies-📚)
- [How to run locally ⚙️](#how-to-run-locally-⚙️)
- [Built with 🛠️](#built-with-🛠️)

<br>

## Project Folder Structure 📂
---

```
.
├── alembic             # Migration tool.
│   └── versions        # Migrations made.
├── app                 # Main app folder.
│   ├── api             # Api related folder (routes, deps, versioning, etc.).
│   │   └── v1
│   │       └── routes  # Route folder where are all routes located for current version.
│   ├── core            # Core where locate all app configs,
│   │   └── settings    # like app settings, logging, etc.
│   ├── infrastructure  # Infrastructure related configs like databases, external resources, etc.
│   ├── models          # Entities representation of the data.
│   ├── repositories    # Code with database interaction (CRUD).
│   ├── schemas         # Pydantic schemas for validating and deserializing data.
│   ├── services        # Business logic like use cases.
│   └── utils           # Utils used in the app.
└── tests               # Test cases for the app.
```

## Features 🚀
---

1. All endpoints created for implementing CRUD (Create, Read, Update, Delete) operations.
2. Specific business logic use case for retrieving the following fields:
    * `count`: Count of restaurants that fall inside the circle with center [x,y] and radius z.s
    * `avg`: Average rating of restaurant inside the circle.
    * `std`: Standard deviation of rating of restaurants inside the circle.

### Endpoints 🌐

`GET /`

Retrieves a list of all restaurants.

`GET /statistics?latitude=x&longitude=y&radius=z`

Retrieves the count, average of rating and standard deviation of restaurants within a given radius of a location. Parameters include:

    latitude: float - the latitude of the location
    longitude: float - the longitude of the location
    radius: int - the radius (in meters) to search for restaurants

`GET /{id}`

Retrieves a specific restaurant by ID.

`POST /`

Creates a new restaurant. The request body should include a `RestaurantCreate` model.

`POST /bulk_create`

Creates multiple new restaurants. The request body should include a list of `RestaurantCreate` models.

`POST /bulk_create_from_csv`

Creates multiple new restaurants from a CSV file. The file should be included in the request body as a `UploadFile` model.

`PUT /{id}`

Updates an existing restaurant. The request body should include a `RestaurantUpdate` model.

`DELETE /{id}`

Deletes an existing restaurant.

`Error Handling`

In case of error, an `HTTPException` will be raised with a message and status code.

<br>

## How to run the code 🏃‍♂️
---
### Installation 🔧

You will need to install [Poetry](https://python-poetry.org/) to install project's dependencies

```bash
$ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
```

Locate where Poetry is installed

```bash
$ whereis poetry
```

Copy and replace poetry's path to this line and added it at the end of the `.bashrc` file

```bash
$ export PATH="$HOME/.poetry/bin:$PATH"
```

<br>

## Installing project's dependencies 📚
---

Clone the repository

  ```bash
  $ git clone https://github.com/Arkemix30/melp_restaurant_api
  ```

Enter into project's root folder and run:

```bash
$ poetry install
```

It should create a `.venv` folder, generating a virtual enviroment with all project's dependencies

<br>

## How to run locally ⚙️
---

* To run the project, you need to activate the virtual environment.
  For that, you can run this command:

  ```bash
  $ poetry shell
  ```

* And finally, to run the server:

  ```bash
  $ uvicorn main:app --reload
  ```

## Built with 🛠️

* [FastAPI](https://fastapi.tiangolo.com/) - The framework used
* [Uvicorn](https://www.uvicorn.org/) - The light-fast ASGI server
* [Pydantic](https://docs.pydantic.dev/) - Data Validator using Python type annotations
* [SQLModel](https://sqlmodel.tiangolo.com/) - Database ORM based in SQLAlchemy and Pydantic
* [GeoAlchemy2](https://geoalchemy-2.readthedocs.io/en/latest/index.html) - Provides extensions to SQLAlchemy for working with spatial databases.
* [Alembic](https://alembic.sqlalchemy.org/en/latest/front.html) - Database migration tool

---

README ⌨️ with ❤️ by [Arkemix30](https://github.com/Arkemix) 😊
