#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install pulp


# In[187]:


get_ipython().system('pip install pulp')


# In[188]:


import pandas as pd


# In[189]:


import numpy as np


# In[190]:


df=pd.read_excel(open('C:/Users/angel/OneDrive/Documents/diet.xlsx','rb'),sheet_name='Sheet1')


# In[191]:


df


# In[192]:


df.head


# In[193]:


data=df[0:64]


# In[194]:


data=data.values.tolist()


# In[195]:


foods = [x[0] for x in data]
calories = dict([(x[0], float(x[3])) for x in data])
cholesterol = dict([(x[0], float(x[4])) for x in data])
totalFat = dict([(x[0], float(x[5])) for x in data])
sodium = dict([(x[0], float(x[6])) for x in data])
carbs = dict([(x[0], float(x[7])) for x in data])
fiber = dict([(x[0], float(x[8])) for x in data])
protien = dict([(x[0], float(x[9])) for x in data])
vitaminA = dict([(x[0], float(x[10])) for x in data])
vitaminC = dict([(x[0], float(x[11])) for x in data])
calcium = dict([(x[0], float(x[12])) for x in data])
iron = dict([(x[0], float(x[13])) for x in data])


# In[196]:


amin = [1500, 30, 20, 800, 130, 125, 60, 1000, 400, 700, 10]
amax = [2500, 240, 70, 2000, 450, 250, 100, 10000, 5000, 1500, 40]


# In[197]:


B = []
for j in range(0,11):
    B.append(dict([(x[0], float(x[j+3])) for x in data]))


# In[200]:


cost = dict([(x[0], float(x[1])) for x in data])


# In[201]:


from pulp import *


# In[202]:


problem2= LpProblem("PuLPTutorial", LpMinimize)


# In[203]:


foodVars = LpVariable.dicts("foods", foods,0)


# In[204]:


chosenVars = LpVariable.dicts("Chosen",foods,0,1,"Binary")


# In[205]:


x = LpVariable.dicts("x", foods, 0)


# In[206]:


problem2 += lpSum([cost[f] * foodVars[f] for f in foods])


# In[207]:


problem2


# In[209]:


for f in foods:
    problem2 += foodVars[f] <= 10000 * chosenVars[f]
    problem2 += foodVars[f] >= .1 * chosenVars[f]


# In[210]:


for i in range(0,11):
    dot_B_x = pulp.lpSum([B[i][j] * foodVars[j] for j in foods])
    condition1 = amin[i] <= + dot_B_x
    problem2 += condition1


# In[211]:


problem2 += chosenVars['Frozen Broccoli'] + chosenVars['Celery, Raw'] <= 1, 'At most one Broccoli / Celery'


# In[212]:


problem2 += chosenVars['Roasted Chicken'] + chosenVars['Poached Eggs'] +   chosenVars['Scrambled Eggs'] + chosenVars['Frankfurter, Beef'] +   chosenVars['Kielbasa,Prk'] + chosenVars['Hamburger W/Toppings'] +   chosenVars['Hotdog, Plain'] + chosenVars['Pork'] +   chosenVars['Bologna,Turkey'] + chosenVars['Ham,Sliced,Extralean'] +   chosenVars['White Tuna in Water']   >= 3, 'At least three proteins'


# In[213]:


problem2.solve()


# In[214]:


print('Optimization Solution:')
for var in problem2.variables():
    if var.varValue > 0:
        if str(var).find('Chosen'):
            print(str(var.varValue) + " units of " + str(var))


# In[215]:


print("Total cost of food = $%.2f" % value(problem2.objective))

