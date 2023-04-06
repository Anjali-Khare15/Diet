#!/usr/bin/env python
# coding: utf-8

# In[81]:


pip install p


# In[82]:


import numpy as np


# In[83]:


import pandas as pd


# In[84]:


data= pd.read_excel('C:/Users/angel/OneDrive/Documents/diet_large2.xlsx', skiprows = 1, header=0)


# In[85]:


dataTable = data[0:7146]


# In[86]:


dataTable=dataTable.values.tolist()


# In[87]:


nutrientNames = list(data.columns.values)


# In[88]:


numNutrients=len(nutrientNames)-1


# In[89]:


for i in range(0,7146):
    for j in range(1,numNutrients):
        if np.isnan(dataTable[i][j]):
            dataTable[i][j]=0


# In[90]:


minVal=data[7147:7148].values.tolist()


# In[91]:


maxVal= data[7149:7151].values.tolist()


# In[92]:


foods=[j[0] for j in dataTable]


# In[93]:


cost=dict([(j[0],float(j[nutrientNames.index('Cholesterol')])) for j in dataTable])


# In[94]:


nutrients=[]
for i in range (0,numNutrients):
    nutrients.append(dict([(j[0],float(j[i+1])) for j in dataTable]))


# In[95]:


from pulp import *


# In[96]:


prob = LpProblem('Food optimization', LpMinimize)


# In[97]:


foodVars=LpVariable.dicts("Foods",foods,0)


# In[98]:


prob +=lpSum([cost[f] * foodVars[f] for f in foods]), 'Total Cost'


# In[99]:


for i in range(0,numNutrients): 
    if (not np.isnan(minVal[0][i+1])) and (not np.isnan(maxVal[0][i+1])): 
        prob += lpSum([nutrients[i][j] * foodVars[j] for j in foods]) >= minVal[0][i+1],'min nutrient' + nutrientNames[i+1]
        prob += lpSum([nutrients[i][j] * foodVars[j] for j in foods]) <= maxVal[0][i+1],'max nutrient ' + nutrientNames[i+1]


# In[100]:


prob.solve()


# In[101]:


print("---------The solution to the diet problem is----------")
for var in prob.variables():
    if var.varValue > 0:
        print(str(var.varValue)+" units of "+str(var).replace('Foods_','') )
print("Total cholesterol = %f" % value(prob.objective))


# In[ ]:





# In[ ]:




