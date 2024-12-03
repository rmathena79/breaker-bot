# breaker-bot
Data Analytics Boot Camp Final Project -- Code Breaker

## Summary
Open the analysis notebook...

## Detailed Overview

This project explores the use of neural networks to break simple, classic ciphers such as the Caesar and Substition ciphers. The approach taken is meant to scale to more sophisticated ciphers such as Enigma, but not sophisticated modern systems.

There are several moving parts:
* A collection of text files, all public domain texts from Project Gutenberg
* A SQL database to track sources (original texts), encrypted files, and keys
* A "librarian" script which cleans, simplifies, and encrypts those texts then populates the database
* A "report" notebook reporting and demonstrating interesting findings from the project
* A "modeler" notebook, meant to be used interactively, to create Tensorflow neural network models
* A "playground" notebook for trying out the most basic functionality, even without a database of files.

# Repo Contents

## Directories:
This includes directories which are not included in source control, but may be created by scripts or manually.
* **./data:** Where all the training data (text files from Project Gutenberg) lives
* **./data/intake/*:** Starting point for raw text files, direct from the Internet. These files will be processed by the librarian.
* **./data/intake/local/*:** You can add more text files to this directory to get them processed by the librarian, without adding them to source control.
* **./data/raw/*:** The librarian copies text files here, unchanged, after taking them in
* **./data/simplified/*:** The librarian puts "simplified" versions of text files here, meaning the character set has been reduced and Project Gutenberg boilerplate has been removed.
* **./data/encoded/*:** The librarian puts encrypted versions of text files here
* **./models/*:** Pre-trained models and scaler values. See ./models.py for descriptions.
* **./temp_models/*:** During model creation, models and scaler values get saved here. Not in source control.
* **./tuner_projects/*:** During Keras Tuner runs, project files get saved here. Not in source control.

## Notebooks:
* **./modeler.ipynb:** Notebook for creating models. Meant to be used interactively, adjusting configuration values and code to get a good model.
* **./report.ipynb:** 
* **./playground.ipynb:** 
* **./statcheck.ipynb:** Simple notebook used to get a sense of character distribution among sets of text files. No specific use currently, but might be interesting.

## Python Code
* **./librarian.py:** Code responsible for taking in new text files, getting them simplified and encrypted, and populating the database with information about them. This script is meant to be run from the command line, from the top directory.
* **./constants.py:** Simple file collecting several values needed throughout this project
* **./crackers.py:** Class(es) that wrap models to more easily crack encrypted files.
* **./credentials.py:** Database connection information. Not in source control. You must create this file.
* **./credentials_example.py:** Example for credentials.py, showing what information is needed and how it should be structured.
* **./db_connect.py:** Class wrapping up database operations for reuse
* **./encoders.py:** Values and functions related to encoding text, including the cipher systems.
* **./helpers.py:** Several reusable functions, needed throughout the project
* **./model_tuner.py:** Class to build models, using Keras Tuner to choose among parameters. Meant to be used from the modeler notebook.
* **./models.py:** Collection of paths for pre-trained models, and code to load them.
* **./tf_helpers.py:** Reusable functions directly related to Tensorflow.

## Other Files
* **./sql/schema.sql**: The schema for the database, which gets populated by the librarian and queried by several components.
* **./README.md:** No idea.

# Instructions

To get started...
* Clone the repo and install necessary packages. A standard dev environment from class, including Tensorflow, is sufficient.
* Create a SQL database (I have been using PostgreSQL) with the schema from ./sql/schema.sql
* Create a file ./credentials.py describing how to connect to your database. See credentials_example.py for an example.
* Optionally, add some more Project Gutenberg text files to ./data/intake/local if you want them encrypted without going into source control
* From the top directory, run ./librarian.py to populate the database and create encrypted files
* Optionally, launch Jupyter Notebook and open modeler.ipynb to create whatever models you need. There are notes at the top of the file to help.
* Launch Jupyter Notebook and open report.ipynb. Run all the cells to populate the data and graphs.
* ...

# Citations
The input data consists of public domain texts from Project Gutenberg: https://www.gutenberg.org/

To link to the source for any file get the ID number from the filename or contents: https://www.gutenberg.org/ebooks/{ID Number}

# Grading Criteria

### Data Model Implementation (25 points)
* A Python script initializes, trains, and evaluates a model (10 points)
* The data is cleaned, normalized, and standardized prior to modeling (5 points)
* The model utilizes data retrieved from SQL or Spark (5 points)
* The model demonstrates meaningful predictive power at least 75% classification accuracy or 0.80 R-squared. (5 points)

### Data Model Optimization (25 points)
* The model optimization and evaluation process showing iterative changes made to the model and the resulting changes in model performance is documented in either a CSV/Excel table or in the Python script itself (15 points)
* Overall model performance is printed or displayed at the end of the script (10 points)

### GitHub Documentation (25 points)
* GitHub repository is free of unnecessary files and folders and has an appropriate .gitignore in use (10 points)
* The README is customized as a polished presentation of the content of the project (15 points)

### Group Presentation (25 points)
* All group members speak during the presentation. (5 points)
* Content, transitions, and conclusions flow smoothly within any time restrictions. (5 points)
* The content is relevant to the project. (10 points)
* The presentation maintains audience interest. (5 points)


# Development Notes

### SIGNIFICANT PROBLEMS
* Keys aren't getting saved in the database right for substitution cipher, so I can't even begin to train them
* Accuracy metrics seem to be returning overly optimistic values for inferred texts. Or I don't know how to understand the output.

### LESSER PROBLEMS
* My GPU isn't getting used much, especially when I have lots of chunks. Look into data pipeline optimization.
* It's a hassle to tweak settings to avoid running out of memory. Another reason to look into data pipelines.

### BIG IDEAS
* Add full support for substitution cipher and Enigma

### TODO BEFORE SUBMISSION
* Add interactive script to let you try stuff out
* Create analysis notebook

### TODO LATER
* Data pipeline!

### Random Stuff. Do not read.

...