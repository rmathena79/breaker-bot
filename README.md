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



Stat Reports

Directory     : sample_data/intake
Text Files    : 19
Subdirectories: 0
        COUNT   PERCENT
0                      
    1685352.0  0.180441
E    866430.0  0.092764
T    656503.0  0.070288
A    560319.0  0.059990
O    530287.0  0.056775
N    505140.0  0.054082
I    498782.0  0.053402
R    453695.0  0.048574
S    420730.0  0.045045
H    344129.0  0.036844
D    284248.0  0.030433
L    277020.0  0.029659
C    229010.0  0.024519
\n   191084.0  0.020458
U    183504.0  0.019647
M    179047.0  0.019170
F    175412.0  0.018780
P    155740.0  0.016674
G    143026.0  0.015313
W    126675.0  0.013562

Directory     : sample_data/simplified
Text Files    : 19
Subdirectories: 0
        COUNT   PERCENT
0                      
    1344585.0  0.155111
E    830798.0  0.095841
T    627773.0  0.072420
A    540988.0  0.062408
O    504166.0  0.058160
N    485340.0  0.055989
I    477751.0  0.055113
R    430896.0  0.049708
S    406280.0  0.046868
H    333888.0  0.038517
D    274098.0  0.031620
L    267905.0  0.030905
C    217439.0  0.025084
\n   179052.0  0.020655
U    173720.0  0.020040
M    173258.0  0.019987
F    168163.0  0.019399
P    147347.0  0.016998
G    134995.0  0.015573
W    121094.0  0.013969

15-epoch training, before character set reduction:
Loss: 1.396213173866272, Accuracy: [0.5052090287208557, 0.03471368923783302]

15-epoch training, 20-character set
Loss: 0.6949121356010437, Accuracy: [0.5059632062911987, 0.05832824856042862]
But my key are all below 0!