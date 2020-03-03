"""Implementation of the immersed boundary module"""

from flowx.imbound.imbound_interface import imbound_interface

class imbound_main(imbound_interface):

    def __init__(self, imbound_vars=None, **kwargs):

        """
        Constructor for the imbound unit

        Arguments
        ---------

        imbound_vars : list
                List of string for field variables required by ins unit
               
                imbound_vars[0] --> indicator variable for immersed boundary
                imbound_vars[1] --> velocity variable

        **kwargs : Dictionary of keyword arguments

        'with_ib' - keyword to indicate if immersed boundary is present or not
                  - True if present
                  - False if not present

        kwargs['with_ib'] = False --> default
                          = True

        Error generated if kwargs['with_ib'] is True and imbound_vars is None

        """

        from flowx.imbound.solvers.stub_force import stub_force
        from flowx.imbound.solvers.stub_compute import stub_compute
        from flowx.imbound.solvers.force_levelset import force_levelset
        from flowx.imbound.solvers.compute_levelset import compute_levelset

        self._with_ib = False
        self.ibmf = 'stub'
        self.velc = 'stub'

        if 'with_ib' in kwargs: self._with_ib = kwargs['with_ib']

        if imbound_vars is not None:
            self.ibmf = imbound_vars[0]
            self.velc = imbound_vars[1] 

        if self._with_ib:
            self.force = force_levelset
            self.compute = compute_levelset

        else:
            self.force = stub_force
            self.compute = stub_compute
      
        if(self._with_ib and imbound_vars is None): raise ValueError('imbound_vars cannot be None when with_ib is True')

        return
 
    def map_to_grid(self, gridx, gridy, particles):
        """
        Subroutine to map immersed boundary on grid
 
        Arguments
        ---------
        gridx : object
          Grid object for x-face variables

        gridy : object
          Grid object for y-face variables

        particles: object
           Object containing immersed boundary information
        """

        self.compute(gridx, gridy, particles, self.ibmf, self.velc)

        return

    def force_flow(self, gridx, gridy, scalars, particles):

        """
        Subroutine to compute immersed boundary forces
 
        Arguments
        ---------
        gridx : object
          Grid object for x-face variables

        gridy : object
          Grid object for y-face variables

        scalars: object
           Scalars object to access time-step and Reynold number

        particles: object
           Object containing immersed boundary information
        """

        self.force(gridx, gridy, scalars, particles, self.ibmf, self.velc)

        return
