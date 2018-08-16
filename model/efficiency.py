import numba
import numpy as np
from typing import NamedTuple

class ValueSet(NamedTuple):
    """
    Class to represent a results tuple. Adding and printing supported,
    along with a few convenience properties.
    """
    S : int
    Sp : int
    MT : int
    FP : int
        
    @property
    def real_pvs(self):
        return self.S + self.MT

    @property
    def eff_rate(self):
        return self.S / self.real_pvs

    @property
    def fp_rate(self):
        return self.FP / self.real_pvs
    
    def __str__(self):
        message = f"Total: {self.real_pvs}, Successes: {self.S}, MT: {self.MT}, FP: {self.FP}"
        if self.S != self.Sp:
            message += f" (Sp: {self.Sp})"
        return message
    
    def __add__(self, other):
        return self.__class__(self[0]+other[0], self[1]+other[1], self[2]+other[2], self[3]+other[3])
    
    def pretty(self):
        return f"""\
Real PVs in validation set: {self.real_pvs:,}
Successes: Either {self.S:,} or {self.Sp:,}, depending on how you count.
Missed True PVs: {self.MT:,}
False Positives: {self.FP:,}
Efficency of detecting real PVs: {self.eff_rate:.2%}
False positive rate: {self.fp_rate:.2%}"""

@numba.jit(numba.float32[:](numba.float32[:], numba.float32), nopython=True)
def pv_locations(targets, threshold):
    state = False
    start = 0
    
    # Make an empty array and manually track the size (faster than python array)
    items = np.empty(150, np.float32)
    nitems = 0
    
    for i in range(len(targets)):
        if targets[i] >= threshold and not state:
            state = True
            start = i
        elif targets[i] < threshold and state:
            state = False
            items[nitems] = (i + start) / 2.
            nitems += 1
        # otherwise, keep going
    return items[:nitems]

@numba.jit(numba.types.UniTuple(numba.int32,2)(numba.float32[:],
                                               numba.float32[:],
                                               numba.float32), nopython=True)
def compare(a, b, diff):
    succeed = 0
    fail = 0
    
    # Check for closest value
    for item in a:
        mindiff = np.abs(b-item).min()
        if mindiff > diff:
            fail += 1
        else:
            succeed += 1
    
    return succeed, fail


# This function does the calculation (the function after this is
# just a wrapper to produce pretty output)

@numba.jit(numba.types.UniTuple(numba.int32,4)(numba.float32[:],
                                               numba.float32[:],
                                               numba.float32,
                                               numba.float32), nopython=True)
def numba_efficiency(truth, predict, threshold, difference):
    
    a = pv_locations(truth, threshold)
    b = pv_locations(predict, threshold)

    S, MT = compare(b, a, difference)
    Sp, FP = compare(a, b, difference)
    
    
    return S, Sp, MT, FP

def efficiency(truth, predict, threshold, difference):
    """
    Compute three values: The number of succeses (S), the number of missed true
    values (MT), and the number of missed false values (FP). Note that the number of successes
    is computed twice, and both values are returned.
    
    Accepts:
      * truth: Numpy array of truth values
      * predict: Numpy array of predictions
      * threshold: The threshold for considering an "on" value
      * difference: The maximum difference to count a success, in bin widths (successes
                    and failures are to the nearest half bin, currently)
    
    Returns: ValueSet(S, Sp, MT, FP)
    
    A future advancement of this algorithm would be to compute the weighted mean, and use that.
    Also, this will currently be triggered by small fluctionations in the input array.
    It should have a minium total integrated value required to "turn it on".
    """
    
    return ValueSet(*numba_efficiency(truth, predict, threshold, difference))

    