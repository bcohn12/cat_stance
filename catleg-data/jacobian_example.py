# ;; fn      :endpoint
# ;; inputs  :q angles between joints, where q1 is the furthest point from the endpoint
# ;; outputs : matrix
def endpoint(q, L):
	import sympy
	import numpy
	L1, L2, L3, q1, q2, q3 = sympy.symbols('L1 L2 L3 q1 q2 q3')
	def jacobian(xs, symbols):
	    return sympy.Matrix([[sympy.diff(x, s) for s in symbols] for x in xs] )
	    
	G_x = L1 * sympy.cos(q1) + L2*sympy.cos(q1 + q2) + L3 * sympy.cos(q1+q2+q3)
	G_y = L1 * sympy.sin(q1) + L2*sympy.sin(q1 + q2) + L3 * sympy.sin(q1+q2+q3)
	G_alpha = q1 + q2 + q3
	x = [G_x, G_y, G_alpha]
	q = [q1, q2, q3]
	symbolic_J = jacobian(x, q)


	J_evalf = symbolic_J.evalf(subs={q1:q[1], q2:q[2], q3:q[3], L1:L[1],L2:L[2], L3:L[3]})
	# now get the jacobian inverse

	J_inv_evalf = J_evalf.inv()
	J_inv_numpy = numpy.matrix(J_inv_evalf).astype(numpy.double)
	J_inv_numpy # this is a numpy matrix now

	J_inv_numpy = numpy.linalg.inv(J_evalf_numpy)
	return J_inv_numpy.transpose()

endpoint(q=[20, 30, 40], L=[25, 15, 10])