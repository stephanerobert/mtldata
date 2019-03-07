mtldata
========

Extract and make sence of Montreal open data.
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
Providing a list of 'arrondissements' and the 'essences' available in the area.
```sh
0.0.0.0:8084/v1/arbres
```

---
Providing a list of trees (all 'essences' included) in this 'arrondissement'
```sh
0.0.0.0:8084/v1/arbres/<arrondissement>
```
WARNING: It can take some time to get a response from that query

---
Providing a list of trees for the provided 'essence' in this 'arrondissement'
```sh
0.0.0.0:8084/v1/arbres/<arrondissement>/<essence>
```

---
Providing a Google map locating all of the trees for the provided 'essence' in this 'arrondissement'
```sh
0.0.0.0:8084/v1/arbres/<arrondissement>/<essence>/map
```
