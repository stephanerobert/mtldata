[![Build Status](https://travis-ci.org/stephanerobert/mtldata.svg?branch=master)](https://travis-ci.org/stephanerobert/mtldata)

mtldata
========

Extract and make sense of Montreal open data.
This small project is really just used for educational purpose

Object of this project
----------------------

For the moment, we only provide information about trees as given by the montreal open data service.


Development
-----------

Unit tests and linting:
```sh
tox
```

equivalent to
```sh
tox -e py37
tox -e flake8
```

How to use it
=============

Launching these commands should bring up your environment.

```sh
docker-compose build
docker-compose up
```

Endpoints
---------

The API is versioned so every useful endpoint starts with "/\<version\>/"

---
Providing a list of 'cities' and the 'species' available in the area.
```sh
0.0.0.0:8084/v1/trees
```

---
Providing a list of 'cities'.
```sh
0.0.0.0:8084/v1/cities
```

---
Providing a list of trees (all 'species' included) in this 'city'
```sh
0.0.0.0:8084/v1/cities/<city>/trees
```
WARNING: It can take some time to get a response from that query

---
Providing a list of 'species' in this 'city'
```sh
0.0.0.0:8084/v1/cities/<city>/trees/species
```

---
Providing a list of trees for the provided 'species' in this 'city'
```sh
0.0.0.0:8084/v1/cities/<city>/trees/species/<species>
```

---
Providing a Google map locating all of the trees for the provided 'species' in this 'city'
```sh
0.0.0.0:8084/v1/cities/<city>/trees/species/<species>/map
```
