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




Trial 23 Complete [00h 00m 17s]
val_modulo_distance_accuracy: 0.5643255710601807

Best val_modulo_distance_accuracy So Far: 0.5663708448410034
Total elapsed time: 00h 52m 40s
Best Hyper Values: {'Processing_Units': 32, 'Basic_Layer_Before': 'hard_sigmoid', 'Fancy_Topology': 'RNN', 'Basic_Layer_After': 'hard_silu', 'Sigmoid': 0, 'Output_Limiter': 1, 'Optimizer': 'adamax', 'tuner/epochs': 2, 'tuner/initial_epoch': 0, 'tuner/bracket': 2, 'tuner/round': 0}
68/68 - 4s - 56ms/step - loss: 2.1680 - modulo_distance_accuracy: 0.5664 - modulo_rounded_accuracy: 0.0949
Best Model Loss: 2.167954444885254, Accuracy: [0.5663708448410034, 0.09488694369792938]



Reloading Tuner from tuner_projects/KT/tuner0.json
Best Hyper Values: {'Processing_Units': 32, 'Basic_Layer_Before': 'hard_sigmoid', 'Fancy_Topology': 'RNN', 'Basic_Layer_After': 'hard_silu', 'Sigmoid': 0, 'Output_Limiter': 1, 'Optimizer': 'adamax', 'tuner/epochs': 2, 'tuner/initial_epoch': 0, 'tuner/bracket': 2, 'tuner/round': 0}
/home/roy/anaconda3/envs/dev_1102/lib/python3.12/site-packages/keras/src/saving/saving_lib.py:576: UserWarning: Skipping variable loading for optimizer 'adamax', because it has 2 variables whereas the saved optimizer has 22 variables. 
  saveable.load_own_variables(weights_store.get(inner_path))
68/68 - 4s - 65ms/step - loss: 2.1680 - modulo_distance_accuracy: 0.5664 - modulo_rounded_accuracy: 0.0949
Best Model Loss: 2.167954444885254, Accuracy: [0.5663708448410034, 0.09488694369792938]




Original, way overly complicated, tuning code:

GO_FAST = False

MAX_EPOCHS_PER_MODEL = 30 # Meant to get a decent idea of parameter, not create a final model. Behaves oddly below 3.
HYPERBAND_ITERATIONS = 2  # "Number of times to iterate over the full Hyperband algorithm"
EXECUTIONS_PER_TRIAL = 2  # Training from scratch
SEARCH_FIT_EPOCHS = 30    # Epochs for each attempt to do a fit, I think. Not sure how this relates to MAX_EPOCHS_PER_MODEL.
OVERWRITE = False          # I'm hoping to be able to interrupt a run and resume it later

# All-encompassing optimization parameter choices. Do not try to use all of them at once...
CHOICES_PROCESSING_UNITS = [1, CHUNK_SIZE // 16, CHUNK_SIZE // 4, CHUNK_SIZE, CHUNK_SIZE * 2] # Prefers 128 (CHUNK_SIZE // 4)
CHOICES_BASIC_LAYERS = ["NONE", "elu", "gelu", "hard_sigmoid", "hard_silu", "hard_swish", "leaky_relu", "linear", "log_softmax", "mish",
        "relu", "relu6", "selu", "sigmoid", "silu", "softmax", "softplus", "softsign", "swish", "tanh"]
CHOICES_FANCY_TOPO = ["NONE", "GRU", "RNN", "LSTM", "GRU-RNN", "GRU-LSTM", "GRU-RNN-LSTM"]     # LSTM seems to win
CHOICES_USE_SIGMOID = [True, False] # Prefers True
CHOICES_SIGMOID_SIZE_TO_OUTPUT = [True, False] # Prefers False
CHOICES_USE_SCALER = [True, False] # Only relevant when using Sigmoid -- prefers True
CHOICES_USE_OUTPUT_LIMITER = [True, False] # Prefers True
CHOICES_OPTIMIZER = ["adamax", "sgd", "RMSProp"] # Prefers adamax

# Narrow down the choices as needed.
# CHOICES_PROCESSING_UNITS unchanged
# CHOICES_BASIC_LAYERS unchanged
# CHOICES_FANCY_TOPO = unchanged
CHOICES_USE_SIGMOID = [False]
CHOICES_SIGMOID_SIZE_TO_OUTPUT = [False]
CHOICES_USE_SCALER = [True]
CHOICES_USE_OUTPUT_LIMITER = [True]
CHOICES_OPTIMIZER = ["adamax"]

if GO_FAST:
    MAX_EPOCHS_PER_MODEL = 3
    SEARCH_FIT_EPOCHS = 4

# Create a method that creates a new Sequential model with hyperparameter options
def create_model(hp):
    processing_units = hp.Choice("Processing_Units", CHOICES_PROCESSING_UNITS)
    basic_layer_before = hp.Choice("Basic_Layer_Before", CHOICES_BASIC_LAYERS)
    fancy_topo = hp.Choice("Fancy_Topology", CHOICES_FANCY_TOPO)
    basic_layer_after = hp.Choice("Basic_Layer_After", CHOICES_BASIC_LAYERS)
    use_sigmoid = hp.Choice("Sigmoid", CHOICES_USE_SIGMOID)    
    use_output_limiter = hp.Choice("Output_Limiter", CHOICES_USE_OUTPUT_LIMITER)
    optimizer = hp.Choice("Optimizer", CHOICES_OPTIMIZER)

    # These aren't really choices, they just make the output more informative
    _ = hp.Choice("Chunk_Size", [CHUNK_SIZE])
    _ = hp.Choice("Batch_Size", [BATCH_SIZE])

    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Embedding(input_dim=CHUNK_SIZE, output_dim=processing_units, name="Embedding_Input"))

    if basic_layer_before != "NONE":
        model.add(tf.keras.layers.Dense(units=processing_units, activation=basic_layer_before, name="Basic_Layer_Before"))

    if fancy_topo == "NONE":
        pass
    elif fancy_topo == "GRU":
        model.add(tf.keras.layers.GRU(processing_units))
    elif fancy_topo == "RNN":
        model.add(tf.keras.layers.SimpleRNN(processing_units))
    elif fancy_topo == "LSTM":
        model.add(tf.keras.layers.LSTM(processing_units))
    elif fancy_topo == "GRU-RNN":
        model.add(tf.keras.layers.GRU(processing_units, return_sequences=True))
        model.add(tf.keras.layers.SimpleRNN(processing_units))
    elif fancy_topo == "GRU-LSTM":
        model.add(tf.keras.layers.GRU(processing_units, return_sequences=True))
        model.add(tf.keras.layers.LSTM(processing_units))
    elif fancy_topo == "GRU-RNN-LSTM":
        model.add(tf.keras.layers.GRU(processing_units, return_sequences=True))
        model.add(tf.keras.layers.SimpleRNN(processing_units, return_sequences=True))
        model.add(tf.keras.layers.LSTM(processing_units))
    else:
        raise Exception(f"Bad choice {fancy_topo}")

    if basic_layer_after != "NONE":
        model.add(tf.keras.layers.Dense(units=processing_units, activation=basic_layer_after, name="Basic_Layer_After"))

    if use_sigmoid:
        # The sigmoid layer can be sized like a processing unit or for output,
        # but that only matters if those values are different
        if OUTPUT_SIZE != processing_units:
            # There are two possibilities, so allow checking both
            sigmoid_size_to_output = hp.Choice("Sigmoid_Size_To_Output", CHOICES_SIGMOID_SIZE_TO_OUTPUT)
            sigmoid_units = OUTPUT_SIZE if sigmoid_size_to_output else processing_units
        else:
            # The two values are the same, so just use that value
            sigmoid_units = OUTPUT_SIZE
    
        model.add(tf.keras.layers.Dense(units=processing_units, activation="sigmoid", name="Sigmoid"))
        use_scaler = hp.Choice("Scaler", CHOICES_USE_SCALER)
        if use_scaler:
            model.add(tf.keras.layers.Rescaling(scale=OUTPUT_MAX, offset=0, name="Rescaler")) # Input is 0-1
    
    if use_output_limiter:
        model.add(tf.keras.layers.Dense(OUTPUT_SIZE, activation=modulo_output, name="Output_Limiter"))
    else:
        model.add(tf.keras.layers.Dense(OUTPUT_SIZE, name="Linear_Output"))

    # Compile the model
    if USE_CUSTOM_METRICS:
        loss = modulo_distance_loss
        metrics = [modulo_distance_accuracy, modulo_rounded_accuracy]
    else:
        loss = LOSS_METRIC
        metrics = [MAIN_ACCURACY_METRIC]
    model.compile(loss=loss, optimizer=optimizer, metrics=metrics)
    
    return model


# Run the kerastuner search for best hyperparameters
if TUNE_NETWORK:
    if USE_CUSTOM_METRICS:
        objective = kt.Objective("val_modulo_distance_accuracy", direction="max")
    else:
        objective = kt.Objective(f"val_{MAIN_ACCURACY_METRIC}", direction="max")

    tuner = kt.Hyperband(
        create_model,
        objective=objective,
        max_epochs=MAX_EPOCHS_PER_MODEL,
        hyperband_iterations=HYPERBAND_ITERATIONS,
        executions_per_trial=EXECUTIONS_PER_TRIAL,
        overwrite=OVERWRITE,
        directory=TUNER_DIRECTORY,
        project_name=TUNER_PROJECT_NAME)
    tuner.search(X_train_scaled, y_train, epochs=SEARCH_FIT_EPOCHS, batch_size=BATCH_SIZE, validation_data=(X_test_scaled,y_test))
    
    best_hyper = tuner.get_best_hyperparameters(1)[0]
    print(f"Best Hyper Values: {best_hyper.values}")
    
    nn = tuner.get_best_models(1)[0]
    eval_results = nn.evaluate(X_test_scaled, y_test, verbose=2, batch_size=BATCH_SIZE )
    print(f"Best Model Loss: {eval_results[0]}, Accuracy: {eval_results[1:]}")

    nn.save("./saved_models/tuned.keras")



Keys aren't getting saved in the database right