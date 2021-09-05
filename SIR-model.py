import numpy as np
import scipy.integrate
import matplotlib.pyplot as pyplot
import random


#The number of days in the model (Assuming that t0 equals zero)
PERIOD = 20

#Array (S, I, R) of the results
SIR_out = []

#Arrays of S, I, R, respectively 
S = []
I = []
R = []

#Initial values
S0 = 1000.0
I0 = 7.0
R0 = 0.0
beta = 0.0020
gamma = 0.50

#The number of people in the model
N = S0 + I0 + R0


#Return the slopes of the variables at the of the day
#Using formulas from SIR model to calculate the scope
#y: The values of S, I, R of the day before
def SIR_atom(y, beta, gamma):
    S_, I_, R_ = y

    
    dS_dt = -(beta)*I_*S_
    dR_dt = gamma*I_

    #Limits the number of S and R people so that 0<S, I, R<N at all times
    if(y[0] + dS_dt <0):
        dS_dt = -y[0]
    if(y[2] + dR_dt >N):
        dR_dt = N-y[2]
        
    dI_dt = - (dS_dt + dR_dt)
    

    return ([dS_dt, dI_dt, dR_dt])


#Get results and store them in SIR_out
# y is the array of S, I, R
def SIR_model(y, beta, gamma):

    #Instanciate values
    S.append(y[0])
    I.append(y[1])
    R.append(y[2])

    #Run over a period of (PERIOD) days
    for i in range(PERIOD):
        dS_dt, dI_dt, dR_dt = SIR_atom(y, beta, gamma)
        y[0] += dS_dt
        y[1] += dI_dt
        y[2] += dR_dt

        # Store values
        S.append(y[0])
        I.append(y[1])
        R.append(y[2])
        
    # Store values
    SIR_out.append(S)
    SIR_out.append(I)
    SIR_out.append(R)



if __name__ == "__main__":

    SIR_model([S0, I0, R0], beta, gamma)

    #Prints out all the results in (S I R) form
    for col in range(PERIOD):
        print(SIR_out[0][col], SIR_out[1][col], SIR_out[2][col], sep = " ")

    t = range(PERIOD + 1)

    #Arrays to store values to draw plot
    S_t = []
    I_t = []
    R_t = []

    #Store calues to draw plot
    for e in SIR_out[0]:
        S_t.append(e)

    for e in SIR_out[1]:
        I_t.append(e)
    
    for e in SIR_out[2]:
        R_t.append(e)


    #Draw the plot that shows the result 
    pyplot.plot(t, S_t, label = "S(t)", marker = '^')
    pyplot.plot(t, I_t, label = "I(t)", marker = 'o')
    pyplot.plot(t, R_t, label = "R(t)", marker = 'v')
    pyplot.xlabel("time")
    pyplot.ylabel("number of cases")
    pyplot.legend()
    pyplot.show()
