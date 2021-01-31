from vqeCalc import GameOutput,rando_hermitian
from qiskit import *
import numpy as np



'''
vqeCalc 2 runs the vqe algorithm in matrices of the form 
a*II+b*XX+c*YY+d*ZZ

I'm using this one instead of the General one just because I know which 
parameters are good so I can test

'''
def comparison(ansatz,Matriz,coeff,param=0):


    estimate,ground=GameOutput(Matriz,coeff,ansatz)

    error=(np.abs(estimate-ground))/np.abs(ground)
    print(estimate,ground,error)


    if error<0.6:
        print('Good Estimate')
        return True,estimate,ground
    else:
        print('Bad Estimate')
        return False,estimate,ground