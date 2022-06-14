# import numpy as np

# close=130
# r2=180
# r1=140
# mean=100
# s1=60
# s2=20
# lst=[r2,r1,mean,s1,s2]

# def find_nearest(array, value):
#     array = np.asarray(array)
#     idx = (np.abs(array - value)).argmin()
#     return array[idx]

# diff=0
# nearest=find_nearest(lst,close)
# if nearest>close:
#     diff=nearest-close
#     print(f'Nearest value: {nearest}, Difference with resistence: {diff}, Market is uptrend')
# else:
#     diff=close-nearest
#     print(f'Nearest value: {nearest}, Difference with support: {diff}, Market is downtrend')


x = [1, 3, 5, 7, 9] 
y = [] 
for i in range (len(x), 0, -1): 
    y.append (x[i-1]) 
    print(y) 