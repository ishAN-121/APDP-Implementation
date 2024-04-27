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

database = "test-database"

start = time.time()

with open('sample_policy.json', 'r') as file:
    policy_json = json.load(file)

policy = Policy.from_json(policy_json)

client = MongoClient()
storage = MongoStorage(client)

# storage.add(policy)
# storage.delete("5")
pdp = PDP(storage)

age= [x for x in range(18,38)]
height = [x for x in range(40,60)]
income = [x for x in range(100,120)]
experience = [x for x in range(0,20)]
rank = [x for x in range(1,21)]
evaluation_matrix = np.array([age, height, income, experience, rank])

weights = [1,0.5,2,4,3]
criterias = np.array([[2,2,0,3,1],[25,50],[12,17]],dtype=object)

t = Topsis(evaluation_matrix, weights, criterias)
t.calc()

end = time.time()
print("Precomputations took: ", end - start)
number_of_iterations = [10]
total_time = 0
errors = []
rmse_values = [] 
avg_time = []

for j in number_of_iterations:
    for i in range(j):
        start = time.time()
        with open('sample_request.json', 'r') as file:
            request_json = json.load(file)

        user_attributes = []

        request = AccessRequest.from_json(request_json)
        for k,v in request.subject.items():
            user_attributes.append(v)

        if pdp.is_allowed(request):
            db = client[database]
            test = db.test
            C = t.comp_attr(user_attributes)
            if request.action["method"] == "get":
                document = test.find({"user_id":request.resource["name"]})
                val = [d["value"] for d in document]
            senstivity = 1 #difference between two datasets
            privacy_budget = np.exp(-1*C)
            scale_parameter = senstivity/privacy_budget
            f_of_D_with_noise = add_laplacian_noise_to_function(val[0], scale_parameter)
            #print(f_of_D_with_noise)
            errors.append(f_of_D_with_noise - val[0])
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

    print("Average time taken ", total_time/i)
    print("RMSE: ", rmse(errors))
    rmse_values.append(rmse(errors))
    avg_time.append(total_time)

plt.bar(list(map(str,number_of_iterations)), rmse_values)
plt.xlabel('Number of iterations')
plt.ylabel('RMSE')

plt.show()

# plt.plot(list(map(str,number_of_iterations)), avg_time)
# plt.xlabel('Number of iterations')
# plt.ylabel('Average time taken')
# plt.show()