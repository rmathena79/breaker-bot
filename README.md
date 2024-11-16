# breaker-bot
Data Analytics Boot Camp Final Project -- Code Breaker

# Grading Criteria
Data Model Implementation (25 points)
A Python script initializes, trains, and evaluates a model (10 points)
The data is cleaned, normalized, and standardized prior to modeling (5 points)
The model utilizes data retrieved from SQL or Spark (5 points)
The model demonstrates meaningful predictive power at least 75% classification accuracy or 0.80 R-squared. (5 points)

Data Model Optimization (25 points)
The model optimization and evaluation process showing iterative changes made to the model and the resulting changes in model performance is documented in either a CSV/Excel table or in the Python script itself (15 points)
Overall model performance is printed or displayed at the end of the script (10 points)

GitHub Documentation (25 points)
GitHub repository is free of unnecessary files and folders and has an appropriate .gitignore in use (10 points)
The README is customized as a polished presentation of the content of the project (15 points)

Group Presentation (25 points)
All group members speak during the presentation. (5 points)
Content, transitions, and conclusions flow smoothly within any time restrictions. (5 points)
The content is relevant to the project. (10 points)
The presentation maintains audience interest. (5 points)


# Notes

DB would be really nice to keep track of keys.

The text files seem to start and end with some boilerplate, marked like this:
    boilerplate
    *** START OF THE PROJECT GUTENBERG EBOOK THE BOY MECHANIC, VOLUME 1: 700 THINGS FOR BOYS TO DO ***
    ...
    *** END OF THE PROJECT GUTENBERG EBOOK THE BOY MECHANIC, VOLUME 1: 700 THINGS FOR BOYS TO DO ***
    boilerplate

Transcribers' notes would also be good to remove but I'm not sure they are standardized well.


Save ORIGINAL
Strip boilerplate, remove all non-desired characters, convert to uppercase.
Save SIMPLIFIED
Encode with various keys
Save ENCODED\CAESAR\pg123123_KEY.txt or similar

Tables
Sources -- where I got stuff from
    ID
    Title
    URL
Encoding Types
    ID
    Encoder Name (None, Caesar, Substitution, Enigma)
Key Types
    ID
    Name (Caesar Offset, Substitution Table, Enigma Dials(?))
Keys
    ID
    Key Type ID
Files
    ID
    Source ID
    Encoder ID
    Key ID (nullable)
    Relative Path
    
This makes sense if I'm going to encode whole files. Which would be nice.
Might want to compress the parent folder.
I need scripts to populate the files (and track them in DB)
    Boilerplate has book ID# which might let me deduce the URL
    https://www.gutenberg.org/ebooks/{ID}
Script for encoding/decoding
Script to generate and test the model
Tests?