from pymongo import MongoClient
from py_abac import PDP, Policy, AccessRequest
from py_abac.storage.mongo import MongoStorage
from topsis import Topsis
from utils import *
import numpy as np
import time
import json
import seaborn as sns
import matplotlib.pyplot as plt

#define attribute types
# MAX = 0
# MIN = 1
# INTERMEDIATE = 2
# INTERVAL = 3

start = time.time()

with open('policy.json', 'r') as file:
    policy_json = json.load(file)

policy = Policy.from_json(policy_json)

client = MongoClient()
storage = MongoStorage(client)

# storage.add(policy)
# storage.delete("6")
pdp = PDP(storage)

age= [x for x in range(18,38)]
height = [x for x in range(40,60)]
income = [x for x in range(100,120)]
experience = [x for x in range(0,20)]
evaluation_matrix = np.array([age, height, income, experience])

weights = [1,0.5,2,4]
criterias = np.array([[2,2,0,3],[25,50],[12,17]],dtype=object)

t = Topsis(evaluation_matrix, weights, criterias)
t.calc()

end = time.time()
print("Precomputations took: ", end - start)
number_of_iterations = 1000
total_time = 0
errors = []

for i in range(number_of_iterations):
    start = time.time()
    with open('request.json', 'r') as file:
        request_json = json.load(file)

    user_attributes = []

    request = AccessRequest.from_json(request_json)
    for k,v in request.subject.items():
        user_attributes.append(v)

    if pdp.is_allowed(request):
        db = client['test-database']
        test = db.test
        C = t.comp_attr(user_attributes)
        D = [1, 2, 3, 4, 5]
        f_of_D = my_function(D)
        senstivity = 1 #difference between two datasets
        privacy_budget = np.exp(-1*C)
        scale_parameter = senstivity/privacy_budget
        f_of_D_with_noise = add_laplacian_noise_to_function(f_of_D, scale_parameter)
        errors.append(f_of_D_with_noise - f_of_D)
        end = time.time()
        total_time += (end - start)
    else:
        print("Access denied")
        exit(1)

sns.kdeplot(errors, fill=True)
plt.xlabel('Values')
plt.ylabel('Density')
plt.title('Kernel Density Estimation Plot')
plt.show()

print("Average time taken for each iteration: ", total_time/number_of_iterations)
print("RMSE: ", rmse(errors))