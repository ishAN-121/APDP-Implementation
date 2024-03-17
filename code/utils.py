import numpy as np

def add_laplacian_noise_to_function(f_of_D, scale_parameter):
    laplace_noise = np.random.laplace(scale=scale_parameter)
    return f_of_D + laplace_noise
    
#example function representing a value that a user may demand
def my_function(D):
    return np.sum(D)

def rmse(errors):
    return np.sqrt(np.mean(np.array(errors) ** 2))
