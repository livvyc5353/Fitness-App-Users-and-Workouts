# it566_project_app_framework
Application framework for semester project.

## Instructions

- Create your project GitHub repository
- Clone your repository to your local machine
- Copy the contents of the app_framework directory to your repository directory
- Begin work on your project

## Create Virtual Environment with PipEnv

- pipenv --python 3.12 
- pipenv install

## Miscellaneous Notes

- **Windows Segmentation Fault when Creating MySQL Pooled Connection**
    - PROBLEM: Windows users might get a Segmentation Fault when attempting to create the MySQLConnection pool in the MySQLPersistenceWrapper class. This does not seem to affect MacOS or Linux users. The problem stems from incompatible C binaries related to the mysql-connector-python package.
    - SOLUTION: I have added a `"use_pure": true` to the configuration file's "database":"pool" section. I have modified the `MySQLPersistenceWrapper._initialize_database_connection_pool()` method to use this setting in the MySQLConnectionPool() constructor.
    - Linux and MacOS users should be able to set `"use_pure": false`.
    - Windows users can try `"use_pure": false` but if you receive the Segmentation Fault error set `"use_pure": true`.
    _ I have tested this on Windows 10 Pro, Linux Debian, and MacOS 26 and 10.15.7 Catalina 



