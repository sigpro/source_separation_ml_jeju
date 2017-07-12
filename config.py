class Config:
    """Holds model hyperparams and data information.

    The config class is used to store various hyperparameters and dataset
    information parameters. Model objects are passed a Config() object at
    instantiation.
    """
    num_freq_bins = 257
    num_time_frames = 5169

    batch_size = 4
    output_size = num_freq_bins * 2
    num_hidden = 1024

    num_layers = 3

    num_epochs = 5000
    l2_lambda = 0
    lr = 0.0001
    beta1 = 0.9
    beta2 = 0.999
