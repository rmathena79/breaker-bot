# This file contains functions specifically made to interact with TensorFlow

import tensorflow as tf
import numpy as np

import constants

# Custom output activation, forcing output to be within range -- but not rounding it off
# Possibly not needed, sigmoid + rescaler might work just as well
@tf.keras.utils.register_keras_serializable(package="RPM_breakerbot", name="modulo_output")
def modulo_output(x):
    return tf.math.mod(x, constants.OUTPUT_MAX)

# Custom loss function, adapted from code generated by Copilot
@tf.keras.utils.register_keras_serializable(package="RPM_breakerbot", name="modulo_distance_loss")
def modulo_distance_loss(y_true, y_pred):
    """ Custom loss function to compute the modulo distance. 
    Args: 
        y_true: True values (ground truth). 
        y_pred: Predicted values. 
        modulo: The modulo value to apply -- hard coded.
    Returns: 
        The computed loss. 
    """ 
    # Compute the raw difference
    diff = tf.abs(y_true - y_pred)
    # Apply modulo operation to handle wrap-around cases
    mod_diff = tf.math.mod(diff, constants.CUSTOM_LOSS_MODULO)
    # Ensure the distance is within the range [0, CUSTOM_LOSS_MODULO/2]
    loss = tf.minimum(mod_diff, constants.CUSTOM_LOSS_MODULO - mod_diff) 
    return tf.reduce_mean(loss)

# Custom accuracy function, counterpart to the loss function above.
# Returns accuracy as 1 - (average percent distance from correct value)
@tf.keras.utils.register_keras_serializable(package="RPM_breakerbot", name="modulo_distance_accuracy")
def modulo_distance_accuracy(y_true, y_pred):
    diff = tf.abs(y_true - y_pred)
    mod_diff = tf.math.mod(diff, constants.CUSTOM_LOSS_MODULO)
    loss = tf.minimum(mod_diff, constants.CUSTOM_LOSS_MODULO - mod_diff)

    good_part = tf.math.subtract(constants.CUSTOM_LOSS_MODULO / 2, loss)
    accuracy = tf.math.divide(good_part, constants.CUSTOM_LOSS_MODULO / 2)

    return tf.reduce_mean(accuracy)

# Custom accuracy, percent of correct values after rounding and doing modulo division
@tf.keras.utils.register_keras_serializable(package="RPM_breakerbot", name="modulo_rounded_accuracy")
def modulo_rounded_accuracy(y_true, y_pred):
    # y_true SHOULD all be round, in-bounds numbers but just in case...
    true_rounded = tf.math.round(y_true)
    true_mod = tf.math.mod(true_rounded, constants.CUSTOM_LOSS_MODULO)

    # y_pred came straight from the model, so it needs to be rounded and mod'ed
    pred_rounded = tf.math.round(y_pred)
    pred_mod = tf.math.mod(pred_rounded, constants.CUSTOM_LOSS_MODULO)

    # Count matches, as a percentage by averaging all the 0's and 1's
    matches_bool = tf.math.equal(true_mod, pred_mod)
    matches_float = tf.cast(matches_bool, tf.float64)
    return tf.reduce_mean(matches_float)


# Initialize the callback to save the best model.
# Re-initializing resets the score history.
def initialize_save_best(best_path):
    # Decide what metrics to use
    if constants.USE_CUSTOM_METRICS:
        save_best_monitor = "modulo_distance_accuracy"
        save_best_mode = "max"
    else:
        save_best_monitor = "loss"
        save_best_mode = "min"
    
    # Training checkpoint to save after each epoch, if it is a new best model:    
    model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=best_path,
        monitor=save_best_monitor,
        mode=save_best_mode,
        save_best_only=True,
        save_weights_only=False,
        verbose=2)
    return model_checkpoint_callback





def self_test():
    # Testing my loss and accuracy functions
    t_true = [[1.0, 2.0, 3.0, constants.CUSTOM_LOSS_MODULO*5]]*2
    t_pred = [[0.4, 1.5, 3.5, constants.CUSTOM_LOSS_MODULO + 0.4]]*2
    
    t_true_ts = tf.constant(np.array(t_true).astype(float))
    t_pred_ts = tf.constant(np.array(t_pred).astype(float))
    loss = modulo_distance_loss(t_true_ts, t_pred_ts)
    accD = modulo_distance_accuracy(t_true_ts, t_pred_ts)
    accR = modulo_rounded_accuracy(t_true_ts, t_pred_ts)
    print("true:", t_true_ts)
    print("pred:", t_pred_ts)
    print("rond:", tf.math.round(t_pred_ts))
    print("diff", abs(t_true_ts - t_pred_ts))
    print("loss:", loss)
    print("accD:", accD)
    print("accR:", accR)

if __name__ == '__main__':
    self_test()    