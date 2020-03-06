import numpy as np
import scipy.sparse as sps
from scipy.sparse.linalg.dsolve import linsolve
from scipy.sparse import spdiags, csr_matrix

def solve_serial_direct(grid, ivar, rvar, verbose, *args):

    """Solve the Poisson system using a direct solver from the scipy library.

    Arguments
    ---------
    grid : Grid object
        Grid containing data.
    ivar : string
        Name of the grid variable of the numerical solution.
    rvar : string
        Name of the grid variable of the right-hand side.

    Returns
    -------
    verbose : bool, optional
        Set True to display residual information;
        default: False.

    """

    phi = grid.get_values(ivar)
    b = grid.get_values(rvar)
    dx, dy = grid.dx, grid.dy
    nx, ny = grid.nx, grid.ny

    matrix_length = nx*ny

    mtx = sps.lil_matrix((matrix_length, matrix_length), dtype=np.float64)

    counter = 0

    for i in range(1,nx+1):
        for j in range(1,ny+1):

            coeff = 0.0
    
            if(j > 1):
                mtx[counter,counter-1] = 1.0/(dx**2)
                coeff = coeff - 1.0/(dx**2)

            if(j < ny):
                mtx[counter,counter+1] = 1.0/(dx**2)
                coeff = coeff - 1.0/(dx**2)

            if(i > 1):
                mtx[counter,counter-ny] = 1.0/(dx**2)
                coeff = coeff - 1.0/(dx**2)

            if(i < nx):
                mtx[counter,counter+ny] = 1.0/(dx**2)
                coeff = coeff - 1.0/(dx**2)

            mtx[counter,counter] = coeff

            counter = counter + 1
        
    mtx = mtx.tocsr()

    sol = linsolve.spsolve(mtx, b[1:-1, 1:-1].flatten())

    residual = np.linalg.norm(mtx * sol - b[1:-1, 1:-1].flatten())

    phi[1:-1,1:-1] = np.reshape(sol,(nx,ny))
    grid.fill_guard_cells(ivar)

    if verbose:
        print('Direct Solver:')
        print('- Final residual: {}'.format(residual))

    return None, residual
