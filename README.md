# Restaurant API


This is an aiohttp project.


## Project layout


```
├── conftest.py
├── mypy.ini
├── README.md
├── requirements.txt
└── restaurants
    ├── app.py
    ├── dev.py
    ├── __init__.py
    └── tests
        ├── __init__.py
        └── test_restaurants.py

```

`conftest.py` contains _pytest's fixtures_ and configuration.

`restaurant/app.py` contains application's code.

the tests are stored into `restaurant/tests`. I used `pytest`. Into the proper python environment and the root directory, running `pytest .` should run them.

`mypy.ini` configures `mypy`, used for static type analysis.

`restaurant/dev.py` is kind of a shorcut to start the development server as a Python module.


## Design considerations

I wanted to keep it simple, this is why I used `aiohttp`.

If I had to do this again, but with more relational constrains, I'll probably go with Django (and _django-rest-framework_).

I used SQLite for storage. The whole database is backed in memory. This is really fast but lacks of persistency across restarts - it spends usually a little more than 1ms to query something.

By declaring an env. var named `SQLITE_DB`, we can use a file to enable persistency, eg:

```
$ export SQLITE_DB=$(pwd)/db.sqlite
```

## What's missing in this implementation


- YAML/JSON configuration (and/or env vars support)
- Logging
- HTTP-related security features (body size limit, authentication, authorizations, rate-limit...)
- maybe a more concurrent database (it currently uses SQLite)
- Swagger / OpenAPI "on the fly" documentation (eg, using [aiohttp-swagger](https://github.com/cr0hn/aiohttp-swagger))




## Setup & run


- 0/ initialize and enter a new _virtualenv_
- 1/ clone this repository
- 2/ run `pip install -r requirements.txt`
- 3/ run `python -m restaurants.dev` to start a local HTTP server


## Tests

Into the same _virtualenv_,

- `pytest .` tests (from `restaurants/tests`)
- `mypy .` static type checking
