# slub-library

Transforms the dataset (with 23551 records) `ldp-boersenblatt` from Sächsische Landesbibliothek - Staats- und Universitätsbibliothek Dresden (slub) to Linked Data with Fox (https://github.com/dice-group/FOX).


# Installation Instructions
```bash
$ mkvirtualenv -p $(which python3) slub
$ cdvirtualenv
$ mkdir src && cd src
$ git clone git@github.com:dice-group/slub.git && cd slub
$ pip install -e .
```
