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
* A "modeler" notebook, meant to be used interactively, to create Tensorflow neural network models
* An "analysis" notebook reporting and demonstrating interesting findings from the project
* A "..." script, meant to be used from the command line, to interactively test some basic operations

# Repo Contents
Functional Files:
* ...

Informative Files:
* ...

# Instructions

To get started...
* Clone the repo and install necessary packages. A standard dev environment from class, including Tensorflow, is sufficient.
* Create a SQL database (I have been using PostgreSQL) with the schema from ./sql/schema.sql
* Create a file ./credentials.py describing how to connect to your database. See credentials_example.py for an example.
* Optionally, add some more Project Gutenberg text files to ./data/intake/local if you want them encrypted without going into source control
* From the top directory, run ./librarian.py to populate the database and create encrypted files
* Launch Jupyter Notebook and open modeler.ipynb to create whatever models you need. There are notes at the top of the file to help.
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
* Something to track what models to use, even just some constants, maybe help for names
* Add interactive script to let you try stuff out
* Create analysis notebook

### TODO LATER
* Training loop, saving best version, reloading if it gets worse, try to train some more...

### Random Stuff. Do not read.

Caesar, Keys
Best Hyper Values: {'Processing_Units': 64, 'Fancy_Topology': 'LSTM', 'Output_Limiter': 0, 'Optimizer': 'RMSProp', 'Chunk_Size': 256, 'Batch_Size': 512, 'tuner/epochs': 7, 'tuner/initial_epoch': 3, 'tuner/bracket': 2, 'tuner/round': 1, 'tuner/trial_id': '0006'}
262/262 - 3s - 10ms/step - loss: 1.0169 - modulo_distance_accuracy: 0.9672 - modulo_rounded_accuracy: 0.4596
Best Model Loss: 1.0168663263320923, Accuracy: [0.9671978950500488, 0.45957377552986145]