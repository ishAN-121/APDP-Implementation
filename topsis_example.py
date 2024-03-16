from topsis import Topsis
import numpy as np
import time

#define attribute types
# MAX = 0
# MIN = 1
# INTERMEDIATE = 2
# INTERVAL = 3

def add_laplacian_noise_to_function(f_of_D, scale_parameter):
    laplace_noise = np.random.laplace(scale=scale_parameter)
    return f_of_D + laplace_noise

def my_function(D):
    return np.sum(D)

start = time.time()

D = [1, 2, 3, 4, 5]
f_of_D = my_function(D)


age= [x for x in range(18,38)]
height = [x for x in range(40,60)]
income = [x for x in range(100,120)]
experience = [x for x in range(0,20)]
evaluation_matrix = np.array([age, height, income, experience])

weights = [1,0.5,2,4]
criterias = np.array([[2,2,0,3],[25,50],[12,17]],dtype=object)

t = Topsis(evaluation_matrix, weights, criterias)
t.calc()

user_attributes = [2,1,3]
C = t.comp_attr(user_attributes)
print(C)

senstivity = 1 #difference between two datasets
privacy_budget = np.exp(-1*C)
scale_parameter = senstivity/privacy_budget
f_of_D_with_noise = add_laplacian_noise_to_function(f_of_D, scale_parameter)
print(f_of_D_with_noise)
end = time.time()
print(end - start)


