# Manuscript extraction plan

The long derivation is the master formalism document. This manuscript project keeps only the equations needed in the main article and moves derivational details to appendices.

## Main text essentials

### Model

Keep:

- physical domains `D_{1->1}` and `D_{1->2}`;
- Hamiltonian decomposition `H = H_t + H_perp + H_on + H_Delta`;
- quasiparticle operator with the factor `s_sigma` in the hole component;
- BdG block `(H_sigma, Delta; Delta^dagger, -H^*_{-sigma}(-K))`;
- statement that a K sector is `(K,sigma) + (-K,-sigma)` in BdG space.

Move to appendix:

- term-by-term Fourier transformation;
- commutator algebra;
- pairing antisymmetry proof.

### Transfer and modes

Keep:

- staggered transfer states;
- central BdG transfer matrix;
- flux metric and pseudo-unitarity;
- stable propagation matrices `P_+` and `P_-`.

Move to appendix:

- explicit inversions;
- determinant identities;
- bilayer secular algebra.

### Conductance

Keep:

- local interface maps;
- round-trip matrix;
- cavity equation;
- `r_he` formula;
- BTK conductance with `chi_in`.

Move to appendix:

- selector matrices;
- 6x6 interface systems;
- Schur-complement reductions.

### Resonances

Keep:

- `s_min(I-M_rt)` diagnostic;
- `r_he = sum_j C_j/(1-mu_j)`;
- bright versus dark poles;
- fixed-K versus integrated ridges;
- K-flatness diagnostic.

## Code outputs needed for the Results section

For each geometry, spin, energy, transverse momentum, and length, output:

- `chi_in`;
- `R_N`, `R_A`, `T_QP`;
- unitarity error `abs(1 - R_N - R_A - T_QP)`;
- fixed-K conductance `g(E,K,sigma,N)`;
- integrated conductance `G(E,N)`;
- `M_rt`;
- `s_min(I_4 - M_rt)`;
- eigenvalues `mu_j = rho_j exp(i Theta_j)`;
- residues `C_j`;
- weights `abs(C_j)^2/abs(1-mu_j)^2`;
- branch curves `E_{ell j}(K,N)`;
- K-flatness `delta E_{ell j}(N)`;
- optional electron/hole content of the round-trip eigenvectors.
