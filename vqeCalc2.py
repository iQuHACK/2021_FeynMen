import matplotlib.pyplot as plt
import sympy as sp
import numpy as np
from qiskit import *
from random import randint


def paulidecompos(Matriz):
    x,y=Matriz.shape
    sigmax=sp.Matrix([[0,1],[1,0]])
    sigmay=sp.Matrix([[0,-sp.I],[sp.I,0]])
    sigmaz=sp.Matrix([[1,0],[0,-1]])
    Identity=sp.Matrix([[1,0],[0,1]])
    if x==y:
        II=sp.kronecker_product(Identity,Identity)
        ZZ=sp.kronecker_product(sigmaz,sigmaz)
        XX=sp.kronecker_product(sigmax,sigmax)
        YY=sp.kronecker_product(sigmay,sigmay)
        pauli=[II,ZZ,XX,YY]
        tags=['II','ZZ','XX','YY']
        elements=sp.symbols('a0:4')
        general_m=sp.zeros(x)
    else:
        print('The input is not a square matrix')
    for i in range(0,len(tags)):
        general_m+=pauli[i]*elements[i]
    decomposition=sp.solve(general_m-Matriz)
    coeff={}
    for i in range(len(tags)):
        coeff[tags[i]]=decomposition[elements[i]]
    return coeff


Matriz=sp.Matrix([[1,0,0,0],[0,0,-1,0],[0,-1,0,0],[0,0,0,1]])
coeff=paulidecompos(Matriz)

def Eigenvals():
    return np.linalg.eigvals(np.array(Matriz).astype(np.float64))

def ansatz(circuit, theta):
    q = circuit.qregs[0]
    print('Select your first gate')
    gate=input()
    if gate=='H':
        circuit.h(q[0])
    circuit.h(q[0])
    circuit.cx(q[0], q[1])
    circuit.rx(theta, q[0])
    return circuit

def two_qubit_vqe(theta, basis):
    q = QuantumRegister(2)
    c = ClassicalRegister(2)
    circuit = QuantumCircuit(q, c)

    # implement the ansate in the circuit
    circuit = ansatz(circuit, theta)
    # measurement
    if basis == 'Z':
        circuit.measure(q, c)
    elif basis == 'X':
        circuit.u2(0, np.pi, q[0])
        circuit.u2(0, np.pi, q[1])
        circuit.measure(q[0], c[0])
        circuit.measure(q[1], c[1])
    elif basis == 'Y':
        circuit.u2(0, np.pi/2, q[0])
        circuit.u2(0, np.pi/2, q[1])
        circuit.measure(q[0], c[0])
        circuit.measure(q[1], c[1])
    else:
        raise ValueError('Not a valid pauli basis, input should be X,Y or Z, we excluded I because no circuit is needed')

    return circuit

def get_expectation(theta, basis):
    
    if basis == 'I':
        return 1
    elif basis == 'Z':
        circuit = two_qubit_vqe(theta, 'Z')
    elif basis == 'X':
        circuit = two_qubit_vqe(theta, 'X')
    elif basis == 'Y':
        circuit = two_qubit_vqe(theta, 'Y')
    else:
        raise ValueError('Not a valid pauli basis, input should be I,X,Y or Z')
    
    shots = 1996 # My birthyear c:
    backend = BasicAer.get_backend('qasm_simulator')
    job = execute(circuit, backend, shots=shots)
    result = job.result()
    counts = result.get_counts()
    
    expected_value = 0
    for event in counts:
        pm = 1
        if event == '01':
            pm = -1
        if event == '10':
            pm = -1
        expected_value += pm * counts[event] / shots
        
    return expected_value


def vqe_ground(theta):
        
    ground_I = coeff['II']*get_expectation(theta, 'I')
    ground_Z = coeff['ZZ']*get_expectation(theta, 'Z')
    ground_X = coeff['XX']*get_expectation(theta, 'X')
    ground_Y = coeff['YY']*get_expectation(theta, 'Y')
    
    # summing the measurement results
    sum_ = ground_I+ground_Z+ground_X+ground_Y
    
    return sum_


