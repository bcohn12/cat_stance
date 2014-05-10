#
# model specific constants
#

# limb topology
_link_lengths = (0.8, 0.5)
_joint_angles_reference = vector(RDF, [45*pi/180, pi/2])
_joint_angle_pairs = matrix(RDF, [[1.190800, 1.83641],
                                  [1.062100, 1.87549],
                                  [0.813389, 1.87549],
                                  [0.700844, 1.83641],
                                  [0.601398, 1.77215],
                                  [0.518223, 1.68353],
                                  [0.453598, 1.57080],
                                  [0.409172, 1.43286],
                                  [0.386661, 1.26610],
                                  [0.389248, 1.06157]])
# moment arms and tendon routings
_r_0 = -10/100
_r_1 = 7/100
_r_2 = -8/100
_r_3 = 12/100
_moment_arm_matrix =  matrix(RDF, [[_r_0, _r_0, _r_1, _r_1],
                                   [_r_2, _r_3, _r_2, _r_3]])

# muscle structure
_sigma_max = 3.5e5
_pcsa = vector(RDF, [1e-3, 2e-3, 1.5e-3, 2.5e-3])
_muscle_lengths = vector(RDF, [20/100, 10/100, 20/100, 15/100])


#
# symbolic computations for the endpoint functions
#
_L = var('L_0 L_1') # symbolic link lengths
_q = var('q_0 q_1') # symbolic joint angles

_symbolic_endpoint_position = matrix([[L_0 * cos(q_0) + L_1 * cos(q_0 + q_1)],
                                      [L_0 * sin(q_0) + L_1 * sin(q_0 + q_1)]])

_symbolic_endpoint_jacobian = jacobian(_symbolic_endpoint_position, (q_0, q_1))

def _numeric(expr, q, L = _link_lengths):
    return expr.subs(L_0 = L[0], L_1 = L[1],
                     q_0 = q[0], q_1 = q[1]).N()

def endpoint_position(joint_angles, link_lengths):
    return _numeric(_symbolic_endpoint_position, joint_angles, link_lengths)

def endpoint_jacobian(joint_angles, link_lengths):
    return _numeric(_symbolic_endpoint_jacobian, joint_angles, link_lengths)

def muscle_strain(joint_angles_difference, muscle_lengths = _muscle_lengths, moment_arm_matrix = _moment_arm_matrix):
    result = moment_arm_matrix.T * joint_angles_difference
    for i in range(len(result)):
        result[i] /= muscle_lengths[i]
    return result

def force_length_curve(muscle_strain, shape_factor=0.5):
    return muscle_strain.apply_map(lambda s: 0 if s >= shape_factor else (1 - (s/shape_factor)**2))

def maximal_muscle_forces(muscle_strain, sigma_max = _sigma_max, pcsa = _pcsa):
    return diagonal_matrix(sigma_max * (force_length_curve(muscle_strain).pairwise_product(pcsa)))

def endpoint_force_matrix(joint_angles,
                          joint_angles_reference = _joint_angles_reference,
                          link_lengths = _link_lengths,
                          muscle_lengths = _muscle_lengths,
                          moment_arm_matrix = _moment_arm_matrix,
                          sigma_max = _sigma_max,
                          pcsa = _pcsa):
    joint_angles_difference = joint_angles_reference - joint_angles
    _muscle_strain = muscle_strain(joint_angles_difference, muscle_lengths, moment_arm_matrix)
    F_0 = maximal_muscle_forces(_muscle_strain, sigma_max, pcsa)
    _endpoint_jacobian = endpoint_jacobian(joint_angles, link_lengths)
    return _endpoint_jacobian.T.inverse() * moment_arm_matrix * F_0

def n_cube_alt_ieqs(n):
    """
    Construct the inequalities for the n-cube [0,1]^n in a format that
    the Polyhedron constructor accepts
    """
    e = identity_matrix(n)
    lt_one  = [[1] + (-e[i]).list() for i in xrange(n)]
    gt_zero = [[0] + (e[i]).list() for i in xrange(n)]
    return lt_one + gt_zero
    
def planar_upwards_force_activation_space(generators):
    """
    Construct the activation space corresponding to the output
    actions codirectional to the y-axis (second coordinate).
    
    The generators must be planar (i.e. a 2-by-n matrix).
    """
    d, n = generators.dimensions()
    
    if d != 2:
        raise ValueError('The generators must be two dimensional')

    ieqs_n_cube = n_cube_alt_ieqs(n)                    # activations in [0,1]^n
    ieqs_nonnegative_y = [[0] + generators[1,:].list()] # output y >= 0
    ieqs = ieqs_n_cube + ieqs_nonnegative_y
    eqns = [[0] + generators[0,:].list()]               # output x == 0
    return Polyhedron(ieqs=ieqs, eqns=eqns)

def projection_into_own_dimension(p):
    """
    Project a polytope containing the origin into a vector space of
    its own dimension. The result is a polyhedron isomorphic to the
    original.
    """
    
    dim = p.dim()
    ambient_face = p.faces(dim)[0]
    
    if zero_vector(p.base_ring(), p.ambient_dim()) not in p:
        raise ValueError("The input polytope not contain the origin ")
    
    ambient_basis = span((v.vector() for v in ambient_face.vertex_generator())).basis_matrix()
    ambient_orthogonal_basis = ambient_basis.gram_schmidt(orthonormal=False)[0] # orthonormality does not work over QQ
    return linear_transformation(ambient_orthogonal_basis.T)

def feasible_output_force_set(joint_angles):
    from zonotope import zonotope_from_vectors
    generators = endpoint_force_matrix(joint_angles)
    return zonotope_from_vectors(matrix(QQ,generators.T))

_all_generators = [endpoint_force_matrix(joint_angles) for joint_angles in _joint_angle_pairs]
_feasible_output_force_sets = [feasible_output_force_set(joint_angles) for joint_angles in _joint_angle_pairs]
_activation_spaces = [planar_upwards_force_activation_space(matrix(QQ,generators)) for generators in _all_generators]
_activation_spaces_projections = [p.projection()(projection_into_own_dimension(p)) for p in _activation_spaces]


