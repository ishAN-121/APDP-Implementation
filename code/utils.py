import numpy as np

def add_laplacian_noise_to_function(f_of_D, scale_parameter):
    laplace_noise = np.random.laplace(scale=scale_parameter)
    return f_of_D + laplace_noise

def rmse(errors):
    return np.sqrt(np.mean(np.array(errors) ** 2))
