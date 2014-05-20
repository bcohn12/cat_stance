% 2014-05-13: Hongchul Sohn
% Description and notes for variables in the data file 'Sohn2013_hinlimb_models.mat'

% Each data structure in cell Cats ({1} birdy, {2} nikey, {3} russl) contains:
% % name (string): cat's name
% % R (7x31): moment arm matrix
% % J (6x7): geometric Jacobian, mapping endpoing wrench (6x1) and joint torque (7x1)
% % q (7x1): model posture matched to experimental cat configuration at normal preferred stance

% DoFs {1,3}: DoF names
% % HF (hip flexion), HAd (hip adduction), HR (hip rotation), 
% % KE (knee extension), KA (knee adduction), AE (ankle extension), AAd (ankle adduction)

% muscles {1x31}: muscle names (abbreviations in paper)

% fmax (1x31): maximum isometric muscle force, descending from original cat model [Burkholder and Nichols, 2004]

% afl95: scaling factor from active force-length relationship curve, at 95% of optimal fiber length
% cosa95 (1x31): cosine of pennation at given posture
% Note that,
% % Above two variables are computed from specific Hill-type muscle model using Neuromechanic. 
% % Tendon slack lengths, which we regard as free variable, are set so that all muscles are at 95% of its optimum fiber lengths.
% % Because of this, pennation is same across all postures (or cats).


% For model construction, you only need fmax, afl95, cos95 and R for a given cat. 
% Choose birdy (cat = 1), for example:
%   RFm = Cats{1,cat}.R*diag(afl95*(fmax.*cosa95))

% Linear equation for static equilibrium then becomes:
%   RFm*e = (Cats{1,cat}.J)'*Fend
% where e (31x1) is the muscle excitation vector you are solving for and
% Fend (6x1) is an endpoint wrench vector you specify as the task.
