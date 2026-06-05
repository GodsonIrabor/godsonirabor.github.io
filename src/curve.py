import numpy as np

class TreasuryCurve:
    def __init__(self, data_points):
        #data points will be a dictionary mapping tenors (yields) to yield (float)
    # This will show us what year the bond is and its corresponding yield,
    # example {8: 0.038, 12: 0.044} these would be the pairing

    # We use the dictionary keys (year and tenor) and sort them numerically
        sorted_tenors = sorted(data_points.keys())
        #then we create an array of the tenors in order (4,8,10)
        self.tenors = np.array(sorted_tenors)
        #using list comprehension and setting self yields to match/corresspend to the tenors variable we created
        # Specifically this will make it certain that self.yield[0] will link to self.tenors[0]
        self.yields = np.array([data_points[t] for t in sorted_tenors])
   
    

    def get_yield(self, target_maturity):
        return np.interp(target_maturity, self.tenors, self.tenors)
        # this functions calculates the yield for any maturity on the curve, and with yield price can be calculated















import numpy as np

class TreasuryCurve:
    def __init__(self, data_points):
        """
        data_points: A dictionary mapping tenor (int/float) to yield (float)
        Example: {2: 0.045, 10: 0.042, 30: 0.043}
        """
        # Sort by tenor to ensure interpolation works correctly
        sorted_tenors = sorted(data_points.keys())
        self.tenors = np.array(sorted_tenors)
        self.yields = np.array([data_points[t] for t in sorted_tenors])

    def get_yield(self, target_maturity):
        """
        Calculates the yield for any point on the curve.
        """
        # Linear interpolation between the closest known tenors
        return np.interp(target_maturity, self.tenors, self.yields)