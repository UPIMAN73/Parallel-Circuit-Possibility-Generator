from random import randint
from math import factorial

# Resistor Parallel Circuit Generator
class RPCG:
    def __init__(self, resistor_array, total_resistors, target_current, target_resistance, input_current, input_voltage):
        self.RA = resistor_array
        self.TR = target_resistance
        self.TotalR = total_resistors
        self.TI = target_current
        self.IC = input_current
        self.IV = input_voltage
        self.resistor_array = []
        self.top_array = []
    
    def generate(self):
        perm = self.permutation()
        resistance_array = []
        RA = []
        i = 0
        # generating resistance array for manipulation
        for i in range(0, self.TotalR):
            RA.append(0)
        
        while (i != perm):
            # Generate resistance values
            for R in range(0,4):
                # index generation
                RA[R] = self.RA[randint(0, len(self.RA)-1)]
            if (RA in resistance_array):
                continue
            else:
                resistance_array.append(RA)
                i += 1
            
            if (i == perm):
                break
            
        # End of While
        return resistance_array

    # Run this After Generate
    def weight(self, resistance_array, threshold):
        # automatically filters the array based on a scoring system & a threshold
        result = []
        RA = []
        for i in range(0, len(resistance_array)):
            RA = [resistance_array[i]]
            if (abs(parallel_resistance_total(RA) - self.target_resistance) <= threshold):
                result.append(RA)
            else:
                continue
        RA = None
        return result

    
    # Run this after Weight function!!!
    def Itable(self, RArray):
        # calculates the current of the resistor array based on current division formula
        result = []
        Rtotal = parallel_resistance_total(RA)
        for i in range(0,len(RArray)):
            result.append(current_n(self.input_current, Rtotal, RA[i]))
        return result
    
    # Run this function after Weight function!!!
    def overallWeight(self, resistor_array, Ithreshold):
        # calculates the weight and finds a new weight based on number of resistors and current division
        result = []
        keep = False
        for RA in resistor_array:
            I = Itable(RA)
            # go through the current table and see if it is within threashold
            for i in I:
                # only do the threshold calculation if the specific current value is greater than target value
                if ((i > self.TI)):
                    if (abs(i - self.TI) <= Ithreshold):
                        keep = True
                    else:
                        keep = False
                        break
                else:
                    keep = True
            if keep:
                result.append(RA)
        
        return result

    # just for overall generation and other stuff (calculation time, etc.)
    def permutation(self):
        return (factorial(len(self.RA)) / factorial(len(self.RA) - self.TotalR))

    # Current based on N value
    def current_n(self, I_s, R_total, R_n):
        return I_s * (R_total / R_n)
    
    # parallel resistance calculation
    def parallel_resistance_total(self, RArray):
        Req = 0.0
        for i in range(0,len(RArray)):
            Req += 1.0 / RArray[i]
        return (1.0 / Req)
    



# Example
# List of possible resistor values that you want to use
R_A = [0.1, 0.22, 1, 2, 2.2, 4.7, 10, 22, 47, 100, 150, 220, 330, 360, 390, 470, 560, 680, 1000, 2000, 2200, 4700, 6800, 10000]

# Total number of resistors you want in your circuit
T_Res = 4

# Target Current Value for current management
T_I = 0.5 # Amps

# Target Resistance Value for the overall parallel circuit
T_R = 4.0 # ohms

# Input Current Value
I_C = 1.25 # Amps

# Input Voltage Value (Only used for power table calculation)
I_V = 4.1 # Volts 

# Resistance Weight Threashold
R_T = 0.4

# Current Weight Threashold
I_T = 0.1

# Create RPCG Class
layer_1 = RPCG(R_A, T_Res, T_I, T_R, I_C, I_V)

# Generate a list of possible resistor configurations given the resistance array and permutations
layer_1.resistor_array = layer_1.generate()

# Select an ammount of configurations that are within design constraints (Resistance)
layer_1.top_array = layer_1.weight(layer_1.resistor_array, R_T)

# Select the best possible configurations that are within design constraints (Current + Resistance)
top_possible_layer_1 = layer_1.overallWeight(layer_1.top_array, I_T)

print(top_possible_layer_1)
