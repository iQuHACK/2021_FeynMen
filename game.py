
from vqeCalc import GameOutput,rando_hermitian
from vqeCalc2 import paulidecompos
import sympy as sp
import numpy as np
ansatz=['H0','C01','X0']


#matriz,coeff=rando_hermitian()


Matriz=sp.Matrix([[1,0,0,0],[0,0,-1,0],[0,-1,0,0],[0,0,0,1]])
coeff=paulidecompos(Matriz)
Matriz=np.array(Matriz).astype(np.float64)

print(GameOutput(Matriz,coeff,ansatz))