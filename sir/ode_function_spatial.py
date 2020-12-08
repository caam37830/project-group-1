import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import scipy.sparse as sparse
import scipy.linalg as sla

#Calculates Laplacian Matrix
def Laplacian(n):
    '''
    Calculates Laplacian Matrix over our spatial grid
    Inputs: n as size of our nxn = M grid
    Outputs: Laplacian Matrix
    '''
    def forward_diff_matrix(n):
        """
        Function from class
        Defines forward diff matrix (nxn sparse coo result)
        """
        data = []
        i = []
        j = []
        for k in range(n - 1):
            i.append(k)
            j.append(k)
            data.append(-1)
            i.append(k)
            j.append(k + 1)
            data.append(1)
    
        return sparse.coo_matrix((data, (i, j)), shape=(n, n)).tocsr()

    D = forward_diff_matrix(n) #construct n x n forward diff matrix

    D2 = -D.T@D
    D2x = sparse.kron(sparse.eye(n), D2) # Matrical partial^2(x), kronenger product construct n^2 x n^2 in size
    D2y = sparse.kron(D2, sparse.eye(n)) # Matrical partial^2(y), kronenger product construct n^2 x n^2 in size
    lp = D2x + D2y # Laplacian is D2x + D2y
    L = lp.todense() #size n^2 x n^2
    return L


#Define derivative function
def spatial(t, SIR, L, c):
    '''
    This is our ODE.
    Used Inputs: SIR (3*m^2 x 1) np vector where the first m^2 elements are S, the second are I, the last are R, 
                 c (1x3 vector associated with [b, k, p, m]
                 L as Laplacian matrix of size m^2 x m^2
    Outputs: Derivative at each point in time SIR(t).
    '''
    
    b = c[0]
    k = c[1]
    p = c[2]
    m = c[3]
    
    S = SIR[:m**2]
    I = SIR[m**2:2*m**2]
    R = SIR[2*m**2:]
    
    #defining diffusion terms as (3m^2 x 1) vector
    LS = p*L@S #Vectorized L by S
    LI = p*L@I #Vectorized L by I
    LR = p*L@R #Vectorized L by R
    
    Sdot = -1*b*S*I + LS
    Idot = b*S*I - k*I + LI
    Rdot = k*I + LR
    
    dSIRdt = np.append(np.append(Sdot, Idot,0), Rdot,0) #stacks vertically
              
    return dSIRdt


#Color Map Plotting
def heatmap2d(arr: np.ndarray):
    '''
    Simple function to plot a color map
    Inputs: np.ndarray with values captured in a mxm grid format
    '''
    plt.imshow(arr, cmap='jet')
    plt.colorbar()
    plt.show()   