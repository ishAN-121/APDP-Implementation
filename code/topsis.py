import numpy as np

class Topsis():
    evaluation_matrix = np.array([])  
    conversion_matrix = np.array([])
    normalized_decision = np.array([]) 
    N = 0 
    M = 0  

    def __init__(self, evaluation_matrix, weight_matrix, criteria):
        self.evaluation_matrix = np.array(evaluation_matrix, dtype="float")
        self.row_size = len(self.evaluation_matrix)
        self.column_size = len(self.evaluation_matrix[0])
        self.weight_matrix = np.array(weight_matrix, dtype="float")
        self.weight_matrix = self.weight_matrix/sum(self.weight_matrix)
        self.criteria = np.array(criteria[0], dtype="float")
        self.intermediate = np.array(criteria[1], dtype="float")
        self.interval = np.array(criteria[2], dtype="float")
        self.normalized_dict = {}
    
    def conversion(self):
        intermediate = 0
        interval = 0
        self.conversion_matrix = np.copy(self.evaluation_matrix)
        for i in range(self.row_size):
            if(self.criteria[i] == 1):
                max_value = max(self.evaluation_matrix[i,:])
                for j in range(self.column_size):
                    self.conversion_matrix[i,j] = max_value - self.evaluation_matrix[i,j]

            if(self.criteria[i] == 2):
                best = self.intermediate[intermediate]
                for j in range(self.column_size):
                    self.conversion_matrix[i,j] = abs(best - self.evaluation_matrix[i,j])
                max_value = max(self.conversion_matrix[i,:])
                for j in range(self.column_size):
                    self.conversion_matrix[i,j] = 1 -  self.conversion_matrix[i,j]/max_value  
                intermediate += 1
            
            if(self.criteria[i] == 3):
                a = self.interval[interval]
                b = self.interval[interval+1]
                M = max(a-min(self.evaluation_matrix[i,:]), max(self.evaluation_matrix[i,:])-b)
                for j in range(self.column_size):
                    if(self.evaluation_matrix[i,j] < a):
                        self.conversion_matrix[i,j] = 1 - (a-self.evaluation_matrix[i,j])/M
                    elif(self.evaluation_matrix[i,j] > b):
                        self.conversion_matrix[i,j] = 1 - (self.evaluation_matrix[i,j]-b)/M
                    else:
                        self.conversion_matrix[i,j] = 1
                interval += 2

    def normalization(self):
        self.normalized_decision = np.copy(self.conversion_matrix)
        sqrd_sum = np.zeros(self.row_size)
        for i in range(self.row_size):
            for j in range(self.column_size):
                sqrd_sum[i] += self.conversion_matrix[i, j]**2
        for i in range(self.row_size):
            for j in range(self.column_size):
                self.normalized_decision[i,j] = self.conversion_matrix[i, j]/(sqrd_sum[i]**0.5)

        for i in range(self.row_size):
            for j in range(self.column_size):
                if i not in self.normalized_dict:
                    self.normalized_dict[i] = {}
                self.normalized_dict[i][self.evaluation_matrix[i, j]] = self.normalized_decision[i, j]

    def alternatives(self):
        self.worst_alternatives = np.zeros(self.row_size)
        self.best_alternatives = np.zeros(self.row_size)
        for i in range(self.row_size):
            self.worst_alternatives[i] = min(
                self.normalized_decision[i,:])
            self.best_alternatives[i] = max(self.normalized_decision[i,:])

    def comp_attr(self, user_attributes):
        user_attributes = np.array(user_attributes, dtype="float")
        dist_best = 0
        dist_worst = 0
        for i in range(self.row_size):
            dist_best += (self.weight_matrix[i] * ((self.best_alternatives[i] - self.normalized_dict[i][user_attributes[i]])**2))
            dist_worst += (self.weight_matrix[i] * ((self.worst_alternatives[i] - self.normalized_dict[i][user_attributes[i]])**2))
        best_distance = dist_best**0.5
        worst_distance = dist_worst**0.5
        C = best_distance/(best_distance + worst_distance)
        return C

    def calc(self):
        self.conversion()
        # print(self.evaluation_matrix, end="\n\n")
        # print(self.conversion_matrix, end="\n\n")
        self.normalization()
        #print(self.normalized_decision, end="\n\n")
        self.alternatives()
        #print(self.worst_alternatives,self.best_alternatives, end="\n\n")