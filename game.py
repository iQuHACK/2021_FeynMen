from comparison import *

from vqeCalc import GameOutput


# The list is just the ansatz given by the user for example H0 means hadamard on qubit 0
# C01 means CX(0,1)
#R0 means RX on the qubit 0

isGood=comparison(['H0','C01','R0'])


circuit=QuantumCircuit(2,2)
print(ansatz(circuit,float(3.1415),['H0','C01','R0']).draw())

