import sympy as sympy
import numpy as numpy

def symbolic_jacobian(functions, variables):
    """
    Compute the symbolic jacobian of the symbolic expression vector 
    ``functions`` with respect to the symbolic variables in the ``variables`` 
    vector
    """
    return sympy.Matrix([[sympy.diff(f, x) for x in variables] for f in functions])

def planar_three_joint_jacobian(q, L):
    cos = sympy.cos
    sin = sympy.sin
 
    L1, L2, L3, q1, q2, q3 = sympy.symbols('L1 L2 L3 q1 q2 q3')
    G_x = L1 * cos(q1) + L2*cos(q1 + q2) + L3 * cos(q1+q2+q3)
    G_y = L1 * sin(q1) + L2*sin(q1 + q2) + L3 * sin(q1+q2+q3)
    G_alpha = q1 + q2 + q3
    x = [G_x, G_y, G_alpha]
    q_symbolic = [q1, q2, q3]

    J = symbolic_jacobian(x, q_symbolic)

    subs = {q1:q[0], q2:q[1], q3:q[2], 
            L1:L[0], L2:L[1], L3:L[2]}
    J_numpy = numpy.matrix(J.evalf(subs = subs)).astype(float)

    return numpy.linalg.inv(J_numpy).transpose()
    
_J = planar_three_joint_jacobian(q = [20, 30, 40], L = [25, 15, 10])
