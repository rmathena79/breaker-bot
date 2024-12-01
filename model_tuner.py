# This file contains a class to encapsulate creation of models during tuning

import tensorflow as tf

import constants
import tf_helpers

class ModelTuner(object):
    # Initialize choice lists as empty. These should be populated by the top-level code.
    def __init__(self, input_shape, output_size, chunk_size, batch_size):
        self.INPUT_SHAPE = input_shape
        self.OUTPUT_SIZE = output_size
        self.CHUNK_SIZE = chunk_size
        self.BATCH_SIZE = batch_size
        self.CHOICES_PROCESSING_UNITS = []
        self.CHOICES_ACTIVATIONS = []
        self.CHOICES_FANCY_TOPO = []
        self.CHOICES_USE_OUTPUT_LIMITER = []
        self.CHOICES_OPTIMIZER = []

    def CreateModel(self, hp) -> tf.keras.Model:
        model = tf.keras.models.Sequential()
        
        processing_units = hp.Choice("Processing_Units", self.CHOICES_PROCESSING_UNITS)
        fancy_topo = hp.Choice("Fancy_Topology", self.CHOICES_FANCY_TOPO)
        use_output_limiter = hp.Choice("Output_Limiter", self.CHOICES_USE_OUTPUT_LIMITER)
        optimizer = hp.Choice("Optimizer", self.CHOICES_OPTIMIZER)

        # These aren't really choices, they just make the output more informative
        _ = hp.Choice("Chunk_Size", [self.CHUNK_SIZE])
        _ = hp.Choice("Batch_Size", [self.BATCH_SIZE])

        model.add(tf.keras.Input(shape=self.INPUT_SHAPE[1:], name="Input_Layer"))

        if fancy_topo == "NONE":
            # I'm not sure this works anymore
            activation_A = hp.Choice("Activation_A", self.CHOICES_ACTIVATIONS)
            activation_B = hp.Choice("Activation_B", self.CHOICES_ACTIVATIONS)
            model.add(tf.keras.layers.Dense(processing_units, activation=activation_A))
            model.add(tf.keras.layers.Dense(processing_units, activation=activation_B))
        elif fancy_topo == "GRU":
            activation_A = hp.Choice("Activation_A", self.CHOICES_ACTIVATIONS)
            recurrent_activation_A = hp.Choice("Recurrent_Activation_A", self.CHOICES_ACTIVATIONS)
            
            model.add(tf.keras.layers.GRU(processing_units, return_sequences=True, activation=activation_A, recurrent_activation=recurrent_activation_A))
        elif fancy_topo == "RNN":
            model.add(tf.keras.layers.SimpleRNN(processing_units, return_sequences=True))
        elif fancy_topo == "LSTM":
            activation_A = hp.Choice("Activation_A", self.CHOICES_ACTIVATIONS)
            recurrent_activation_A = hp.Choice("Recurrent_Activation_A", self.CHOICES_ACTIVATIONS)

            model.add(tf.keras.layers.LSTM(processing_units, return_sequences=True, activation=activation_A, recurrent_activation=recurrent_activation_A))
        elif fancy_topo == "GRU-RNN":
            activation_A = hp.Choice("Activation_A", self.CHOICES_ACTIVATIONS)
            recurrent_activation_A = hp.Choice("Recurrent_Activation_A", self.CHOICES_ACTIVATIONS)

            model.add(tf.keras.layers.GRU(processing_units, return_sequences=True, activation=activation_A, recurrent_activation=recurrent_activation_A))
            model.add(tf.keras.layers.SimpleRNN(processing_units, return_sequences=True ))
        elif fancy_topo == "GRU-LSTM":
            activation_A = hp.Choice("Activation_A", self.CHOICES_ACTIVATIONS)
            recurrent_activation_A = hp.Choice("Recurrent_Activation_A", self.CHOICES_ACTIVATIONS)
            activation_B = hp.Choice("Activation_B", self.CHOICES_ACTIVATIONS)
            recurrent_activation_B = hp.Choice("Recurrent_Activation_B", self.CHOICES_ACTIVATIONS)
            
            model.add(tf.keras.layers.GRU(processing_units, return_sequences=True, activation=activation_A, recurrent_activation=recurrent_activation_A))
            model.add(tf.keras.layers.LSTM(processing_units, return_sequences=True, activation=activation_B, recurrent_activation=recurrent_activation_B))
        elif fancy_topo == "GRU-RNN-LSTM":
            activation_A = hp.Choice("Activation_A", self.CHOICES_ACTIVATIONS)
            recurrent_activation_A = hp.Choice("Recurrent_Activation_A", self.CHOICES_ACTIVATIONS)
            activation_B = hp.Choice("Activation_B", self.CHOICES_ACTIVATIONS)
            recurrent_activation_B = hp.Choice("Recurrent_Activation_B", self.CHOICES_ACTIVATIONS)

            model.add(tf.keras.layers.GRU(processing_units, return_sequences=True, activation=activation_A, recurrent_activation=recurrent_activation_A))
            model.add(tf.keras.layers.SimpleRNN(processing_units, return_sequences=True))
            model.add(tf.keras.layers.LSTM(processing_units, return_sequences=True, activation=activation_B, recurrent_activation=recurrent_activation_B))
        else:
            raise Exception(f"Bad choice {fancy_topo}")
        
        if use_output_limiter:
            model.add(tf.keras.layers.Dense(self.OUTPUT_SIZE, activation=tf_helpers.modulo_output, name="Output_Limiter"))
        else:
            model.add(tf.keras.layers.Dense(self.OUTPUT_SIZE, name="Linear_Output"))

        # Compile the model
        if constants.USE_CUSTOM_METRICS:
            loss = tf_helpers.modulo_distance_loss
            metrics = [tf_helpers.modulo_distance_accuracy, tf_helpers.modulo_rounded_accuracy]
        else:
            loss = "mae"
            metrics = "mae"
        model.compile(loss=loss, optimizer=optimizer, metrics=metrics)
        
        return model        