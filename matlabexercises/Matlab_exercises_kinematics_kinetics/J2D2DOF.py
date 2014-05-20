#######################################
######### NEUROMECHANICS  #############
# (c) Francisco Valero-Cuevas
# September 2013, version 1.0
# Filename: J2D2DOF.py
# Jacobian of 2D, 2DOF linkage system

def symbolic_jacobian(functions, variables):
    """
    Compute the symbolic jacobian of the symbolic expression vector 
    ``functions`` with respect to the symbolic variables in the ``variables`` 
    vector
    """
    return sympy.Matrix([[sympy.diff(f, x) for x in variables] for f in functions])


def print_matrix(matrix):
	s = [[str(e) for e in row] for row in matrix]
	lens = [max(map(len, col)) for col in zip(*s)]
	fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
	table = [fmt.format(*row) for row in s]
	print '\n'.join(table)

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
G = [x,y]
# Create Jacobian and its permutations
J = G.jacobian([q1,q2])
# J = symbolic_jacobian(G, [q1, q2])
J_inverted = J.inv()
J_trans = J_inverted.transpose()
J_trans_inv = J_trans.inv()

print "G"
print G
print "J"
print J
print "J_inverted"
print J_inverted
print "J_trans"
print J_trans
print "J_trans_inv"
print J_trans_inv


print "=================="
# Define substitutions for Numerical Example
# subs = {l1:1, #limb lengths
# 		l2:1,
# 		q1:0, #joint angles
# 		q2:numpy.pi/2.0}



# TODO: convert matlab code below to python
# fprintf('Evaluate the functions for these parameter values\n')
# fprintf('G');subs(G)
# fprintf('J');subs(J)
# fprintf('J_trans');subs(J_trans)
# fprintf('J_inv');subs(J_inv)
# fprintf('J_trans_inv');subs(J_trans_inv)
# % Numerical examples
# fprintf('Example of applying a positive angular velocity at q1 to find the resulting instantaneous endpoint velocity')
# q1_dot = 1
# q2_dot = 0
# x_dot = subs(J*[q1_dot q2_dot]')
# fprintf('Example of applying that same endpoint velocity to find the resulting instantaneous angular velocities')
# q_dot = subs(J_inv*x_dot)
# fprintf('Example of finding which torques produce a horizontal endpoint force vector in equilibrium')
# tau = subs(J_trans*[1 0]')
# fprintf('Example of applying those joint torques to find the resulting endpoint force vector in equilibrium')
# f = subs(J_trans_inv*tau)