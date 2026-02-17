
# weird OpenMP error:
# export KMP_DUPLICATE_LIB_OK=TRUE

import numpy as np
import pandas as pd

import torch
import torch.nn as nn
import torch.nn.functional as F


import newstatscraping as ss
from scipy import stats

year = 2022
P = ss.grab_fangraphs_pitching_data([year])



tbfnum = (P['TBF'].values)


tbfnum = (P['TBF'].values.astype('float'))
tbflimit=100

tbfnorm = (P['TBF'].values.astype('float'))[tbfnum>tbflimit]
#tbfnorm = 1.0

hrnum = (P['HR'].values.astype('float'))[tbfnum>tbflimit]/tbfnorm
hitnum = (P['H'].values.astype('float'))[tbfnum>tbflimit]/tbfnorm

bbarr = (P['BB'].values.astype('float'))[tbfnum>tbflimit]/tbfnorm
eraarr = (P['ER'].values.astype('float'))[tbfnum>tbflimit]/tbfnorm
karr = (P['SO'].values.astype('float'))[tbfnum>tbflimit]/tbfnorm
warr = (P['W'].values.astype('float'))[tbfnum>tbflimit]#/tbfnorm

def NormVec(arr):
    arr = (arr-np.nanmean(arr))/np.nanstd(arr)
    return arr


hrnum = NormVec(hrnum)
eraarr = NormVec(eraarr)
karr = NormVec(karr)
bbarr = NormVec(bbarr)
#warr = NormVec(warr)

print(np.nanstd(hrnum))

plrs = (P['Name'].values)[tbfnum>tbflimit]


X = np.array([eraarr,karr,bbarr,hrnum]).T
Y = np.array(warr)
print(X.shape,Y.shape)



from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.2,random_state=0)


from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

print(X_train)

X_train = torch.FloatTensor(X_train)
X_test = torch.FloatTensor(X_test)
Y_train = torch.LongTensor(Y_train)
Y_test = torch.LongTensor(Y_test)

print(Y_train,Y_test)

class ANN(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(in_features=4, out_features=64) # 4 is the number of input features
        self.fc2 = nn.Linear(in_features=64, out_features=2)
        self.output = nn.Linear(in_features=2, out_features=23) # 25 here is the number of W we are discretising
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.output(x)
        return x


model = ANN()
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)


#%%time
epochs = 100
loss_arr = []
for i in range(epochs):
   y_hat = model.forward(X_train)
   loss = criterion(y_hat, Y_train)
   loss_arr.append(loss)
   if i % 10 == 0:
       print(f'Epoch: {i} Loss: {loss}')
   optimizer.zero_grad()
   loss.backward()
   optimizer.step()


preds = []
with torch.no_grad():
   for val in X_test:
       y_hat = model.forward(val)
       preds.append(y_hat.argmax().item())


df = pd.DataFrame({'Y': Y_test, 'YHat': preds})
df['Correct'] = [1 if corr == pred else 0 for corr, pred in zip(df['Y'], df['YHat'])]

df['Correct'] = [1 if (corr-pred <= 2) else 0 for corr, pred in zip(df['Y'], df['YHat'])]


print(df['Correct'].sum() / len(df))


