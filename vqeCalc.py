import matplotlib.pyplot as plt
import sympy as sp
import numpy as np
from qiskit import *
from random import randint



def rando_hermitian():
    sigmax=np.array([[0,1],[1,0]])
    sigmay=np.array([[0,-1j],[1j,0]])
    sigmaz=np.array([[1,0],[0,-1]])
    Identity=np.array([[1,0],[0,1]])
    II=np.kron(Identity,Identity)
    IZ=np.kron(Identity,sigmaz)
    IX=np.kron(Identity,sigmax)
    IY=np.kron(Identity,sigmay)
    ZI=np.kron(sigmaz,Identity)
    ZZ=np.kron(sigmaz,sigmaz)
    ZX=np.kron(sigmaz,sigmax)
    ZY=np.kron(sigmaz,sigmay)
    XI=np.kron(sigmax,Identity)
    XZ=np.kron(sigmax,sigmaz)
    XX=np.kron(sigmax,sigmax)
    XY=np.kron(sigmax,sigmay)
    YI=np.kron(sigmay,Identity)
    YZ=np.kron(sigmay,sigmaz)
    YX=np.kron(sigmay,sigmax)
    YY=np.kron(sigmay,sigmay)
    pauli=[II,IZ,IX,IY,ZI,ZZ,ZX,ZY,XI,XZ,XX,XY,YI,YZ,YX,YY]
    tags=['II','IZ','IX','IY','ZI','ZZ','ZX','ZY','XI','XZ','XX','XY','YI','YZ','YX','YY']
    elements=np.random.rand(16,1)
    general_m=np.zeros((4,4),dtype='complex128')

    for i in range(0,len(tags)):
        general_m+=pauli[i]*elements[i]
    coeff={}
    for i in range(len(tags)):
        coeff[tags[i]]=elements[i][0]
    return general_m,coeff


def ansatz(circuit, theta):
    q = circuit.qregs[0]
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
    if basis == 'ZZ':
        circuit.measure(q, c)
    elif basis == 'XX':
        circuit.u2(0, np.pi, q[0])
        circuit.u2(0, np.pi, q[1])
        circuit.measure(q[0], c[0])
        circuit.measure(q[1], c[1])
    elif basis == 'YY':
        circuit.u2(0, np.pi/2, q[0])
        circuit.u2(0, np.pi/2, q[1])
        circuit.measure(q[0], c[0])
        circuit.measure(q[1], c[1])
    elif basis == 'IX':
        circuit.u2(0, np.pi, q[1])
        circuit.measure(q[0], c[0])
        circuit.measure(q[1], c[1])
    elif basis == 'IY':
        circuit.u2(0, np.pi/2, q[1])
        circuit.measure(q[0], c[0])
        circuit.measure(q[1], c[1])
    elif basis == 'IZ':
        circuit.measure(q[0], c[0])
        circuit.measure(q[1], c[1])
    elif basis == 'ZI':
        circuit.measure(q[0], c[0])
        circuit.measure(q[1], c[1])
    elif basis == 'ZX':
        circuit.u2(0, np.pi, q[1])
        circuit.measure(q[0], c[0])
        circuit.measure(q[1], c[1])
    elif basis == 'ZY':
        circuit.u2(0, np.pi/2, q[1])
        circuit.measure(q[0], c[0])
        circuit.measure(q[1], c[1])
    elif basis == 'XI':
        circuit.u2(0, np.pi, q[0])
        circuit.measure(q[0], c[0])
        circuit.measure(q[1], c[1])
    elif basis == 'XZ':
        circuit.u2(0, np.pi, q[0])
        circuit.measure(q[0], c[0])
        circuit.measure(q[1], c[1])
    elif basis == 'XX':
        circuit.u2(0, np.pi, q[0])
        circuit.u2(0, np.pi, q[1])
        circuit.measure(q[0], c[0])
        circuit.measure(q[1], c[1])
    elif basis == 'XY':
        circuit.u2(0, np.pi, q[0])
        circuit.u2(0, np.pi/2, q[1])
        circuit.measure(q[0], c[0])
        circuit.measure(q[1], c[1])
    elif basis == 'YZ':
        circuit.u2(0, np.pi/2, q[0])
        circuit.measure(q[0], c[0])
        circuit.measure(q[1], c[1])
    elif basis == 'YI':
        circuit.u2(0, np.pi/2, q[0])
        circuit.measure(q[0], c[0])
        circuit.measure(q[1], c[1])
    elif basis == 'YX':
        circuit.u2(0, np.pi/2, q[0])
        circuit.u2(0, np.pi, q[1])
        circuit.measure(q[0], c[0])
        circuit.measure(q[1], c[1])
    else:
        raise ValueError('Not a valid pauli basis, input should be X,Y or Z, we excluded I because no circuit is needed')

    return circuit


def get_expectation(theta, basis):
    
    if basis == 'II':
        return 1
    else:
        circuit = two_qubit_vqe(theta, basis)
    
    shots = 10000 # Max
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

def vqe_ground(theta,coeff):
    sum_=0
    tags=['II','IZ','IX','IY','ZI','ZZ','ZX','ZY','XI','XZ','XX','XY','YI','YZ','YX','YY']
    for i in tags:
         sum_+=coeff[i]*get_expectation(theta, i)

    
    # summing the measurement results    
    return sum_



def  GameOutput():
    Matriz,coeff=rando_hermitian()
    print('Input your chosen parameter from 0 to 2 pi')
    eigen=np.real(np.linalg.eigvals(Matriz))
    param=input()
    param=float(param)
    estimation=vqe_ground(param,coeff)
    print(estimation,eigen)
    return estimation,eigen