from vqeCalc2 import *



'''
vqeCalc 2 runs the vqe algorithm in matrices of the form 
a*II+b*XX+c*YY+d*ZZ

I'm using this one instead of the General one just because I know which 
parameters are good so I can test

'''
def comparison(ansatz,param=0):
    print('param')
    param=float(param)
    estimate=vqe_ground(param,ansatz)
    ground=np.amin(Eigenvals())

    print(estimate,ground)
    error=(np.abs(estimate-ground))/np.abs(ground)
    print(error)


    if error<0.5:
        print('Good Estimate')
        return True
    else:
        print('Bad Estimate')
        return False

