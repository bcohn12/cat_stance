#######################################
######### NEUROMECHANICS  #############
# (c) Francisco Valero-Cuevas
# September 2013, version 1.0
# Filename: J2D2DOF.py
# Jacobian of 2D, 2DOF linkage system

# Import required packages
import sympy
import numpy
# Define variables for symbolic analysis
G, J = sympy.symbols('G J')					# Vector functions
q1, q2, x, y = sympy.symbols('q1 q2 x y')	# Degrees of freedom
l1, l2 = sympy.symbols('l1 l2')				# System parameters

# Define x and y coordinates of the endpoint
x = l1*sympy.cos(q1) + l2*sympy.cos(q1+q2)
y = l1*sympy.sin(q1) + l2*sympy.sin(q1+q2)
# Create Matrix for Geometric Model
# G = [x,y]
G = sympy.Matrix([x,y])
# Create Jacobian and its permutations
J = G.jacobian([q1,q2])
J_inv = J.inv()
J_trans = J_inv.transpose()
J_trans_inv = J_trans.inv()

print("G")
sympy.pprint(G)
print("J")
sympy.pprint(J)
print("J_inv")
sympy.pprint(J_inv)
print("J_trans")
sympy.pprint(J_trans)
print("J_trans_inv")
sympy.pprint(J_trans_inv)
sympy.pprint(J_trans_inv)


print "=================="
# Define substitutions for Numerical Example
subs = {l1:1, #limb lengths
		l2:1,
		q1:0, #joint angles
		q2:numpy.pi/2.0}
print("Evaluate the functions for these parameter values \n")

# % Numerical examples
print('Numerical examples')

print('G \n')
valG = G.evalf(subs=subs)
sympy.pprint(valG)

print('J \n')
numerical_J = J.evalf(subs=subs)
sympy.pprint(numerical_J)

print('J_trans \n')
numerical_J_trans = J_trans.evalf(subs=subs)
sympy.pprint(numerical_J_trans)

print('J_inv \n')
numerical_J_inv = J_inv.evalf(subs=subs)
sympy.pprint(numerical_J_inv)

print('J_trans_inv \n')
numerical_J_trans_inv = J_trans_inv.evalf(subs=subs)
sympy.pprint(numerical_J_trans_inv)

print('Example of applying a positive angular velocity at q1 to find the resulting instantaneous endpoint velocity')
q1_dot = 1
q2_dot = 0
x_dot = numerical_J * sympy.Matrix([q1_dot, q2_dot]).evalf(subs=subs)
x_dot = x_dot.n()
sympy.pprint(x_dot)
print('Example of applying that same endpoint velocity to find the resulting instantaneous angular velocities')
q_dot = numerical_J_inv * x_dot
q_dot = q_dot.evalf(subs=subs).n()
sympy.pprint(q_dot)
print('Example of finding which torques produce a horizontal endpoint force vector in equilibrium')
tau = numerical_J_inv.transpose() * sympy.Matrix([1, 0])
sympy.pprint(tau.n())
print('Example of applying those joint torques to find the resulting endpoint force vector in equilibrium')
# f = subs(J_trans_inv*tau)
f = numerical_J_trans_inv * tau
sympy.pprint(f.evalf())

