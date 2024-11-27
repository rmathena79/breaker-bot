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

Transcribers' notes would also be good to remove but I'm not sure they are standardized well.

To be fully normalized -- I should probably have tables for titles and urls too
    
Tests?

Should I store the character set in the DB too?

Tools need options for
samples vs full dataset
db credentials for each

Turned on WSL mirrored network mode...

Be careful about when you're using ASCII values vs. offsets within the character set.
I probably want to mostly use offsets, so it would be very helpful to save coded files as binary.

My GPU isn't getting used much, espescially when I have lots of chunks. Into into data pipeline optimization.

Embed -> LSTM(128) -> Limiter(1): 
Loss: 10.517082214355469, Accuracy: [0.6557093262672424, 0.28057751059532166]
Loss: 13.5811, Accuracy (Distance): 0.553594, Accuracy (Rounded): 0.110939

Embed -> RNN(128) -> Limiter(1): 
Loss: 13.5811, Accuracy (Distance): 0.529031, Accuracy (Rounded): 0.0115869

Embed -> GRU(128) -> Limiter(1): 
Loss: 13.5811, Accuracy (Distance): 0.566594, Accuracy (Rounded): 0.158879

Embed -> LSTM(128) -> Linear(1): 
Loss: 13.5811, Accuracy (Distance): 0.565071, Accuracy (Rounded): 0.0760692

Embed -> LSTM(128) -> Sigmoid(1)
Loss: 13.5811, Accuracy (Distance): 0.532304, Accuracy (Rounded): 0.0

Embed -> LSTM(128) -> Sigmoid(128) -> Scaler(128) -> Limiter(1): 
Loss: 1.1285839080810547, Accuracy: [0.5765235424041748, 0.17478026449680328]
Loss: 13.5811, Accuracy (Distance): 0.560611, Accuracy (Rounded): 0.0789181

Embed -> LSTM(128) -> Sigmoid(1) -> Scaler(1) -> Limiter(1): 
Loss: 3.157512903213501, Accuracy: [0.5821149349212646, 0.21897727251052856]
Loss: 13.5811, Accuracy (Distance): 0.5572, Accuracy (Rounded): 0.113442

Embed -> LSTM(128) -> Sigmoid(1) -> Scaler(1)
Loss: 1.5583804845809937, Accuracy: [0.5726279616355896, 0.1371275782585144]
Loss: 13.5811, Accuracy (Distance): 0.5619, Accuracy (Rounded): 0.129071