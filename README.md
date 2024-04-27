# Introduction

This is an implementation of [Attribute-Based Personalized Differential Privacy Data Publishing Scheme for Social Networks](https://www.researchgate.net/publication/365753132_APDP_Attribute-Based_Personalized_Differential_Privacy_Data_Publishing_Scheme_for_Social_Networks) paper in Python. 

This paper presents a
fine-grained personalized differential privacy data publishing
scheme (APDP) for social networks.Specifically, it designs a new
mechanism that defines the privacy protection levels of different
users based on their attribute values. In particular, it exploits the
TOPSIS method to map the attribute values to the amount of
noise required to add. Furthermore, to prevent illegal download
of data, the access control is integrated with differential privacy.

# Usage

```
git clone git@github.com:ishAN-121/APDP-Implementation.git
 ```
     
    cd APDP-Implementation/code
```
pip install -r requirements.txt
```

In order to run the code you need to install MongoDb database.Also specify the name of the database in the code.By default it is test-database.  **Also you need to add the data of the user in the database that we are trying to retreive.**

Structure of the database is as follows:
```
{
  "user_id" : "123",
  "value" : 0
}
```

Now you need to specify the attributes and their values in the code. You can do this by changing the values of the attributes in ABAC.py file. By default age, height, income, experience and income are used as attributes. Assign weights to these attributes in the same file.


Attribute types defined in the code are:
```
MAX Type = 0
MIN Type = 1
INTERMEDIATE Type = 2
INTERVAL Type = 3
```

In criterias you specify the type of attribute in the correct order. For intermediate type fill the intermeiate values in the the second array of criterias and for interval type fill the interval values in the third array of criterias.

``` 
criterias = np.array([attribute type array,intermediate values, interval values],dtype=object)
```

Number of iterations is used to simulate multiple users. The number of users is equal to the number of iterations. 

## Policy 

The sample_policy.json is an example policy. Resource in the policy defines the resources that are accessible to the user sending the request. Action defines the action that the user can perform on the resource like create,delete or get. The policy is in the form of a json file. Context in the sample policy is for localhost only. Change the value for '*' to allow for all ip addresses.
To change the conditions according to your need lookup the documentation of pyabac.

## Request

Sample request contains the values of user attributes , the type of action and the resource that the user is trying to access. The request is in the form of a json file. Context is your ip address. Change the value of attributes as you wish.

---

Finally after doing all the above steps run the code using the following command:

```
python ABAC.py
```

This will print the value that will be returned after adding the noise.

---

