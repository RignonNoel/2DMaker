# Quickstart

## Clone the project

The project use [Git](https://git-scm.com/) and is accessible on [Github](https://github.com/).

First of all you need to clone the project on your computer.

```
git clone https://github.com/RignonNoel/2DMaker.git
```

## Create a virtual environment

[Virtualenv](https://virtualenv.pypa.io/) provide isolated Python environments, which are more practical than installing packages systemwide. They also allow installing packages without administrator privileges.

1. Create a new virtual environment 
```
virtualenv env
```

2. Active the virtual environment

```
. env/bin/activate
```

You need to ensure the virtual environment is active each time you want to launch the project.

## Install all requirements

All requirements used by this projects are documented inside the `requirements.txt` file at the root of the repository.
You can install all requirements needed by just one commandline.

**WARNING** : Make sure your virtual environment is active or you will install all these packages systemwide. 
```
pip install -r requirements.txt
```
 
## Test the installation

To launch a first test of this POC you just 
need to execute this commandline

```python
python src/main.py
```