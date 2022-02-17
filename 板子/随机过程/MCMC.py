import numpy as np
import pymc3 as pm
import theano.tensor as tt
import scipy
from scipy import optimize
import matplotlib.pyplot as plt

time = np.random.rand(20)
sleep_obs = np.random.rand(20)
N_SAMPLES = 5000

with pm.Model() as sleep_model:
    # Create the alpha and beta parameters
    alpha = pm.Normal('alpha', mu=0.0, tau=0.01, testval=0.0)
    beta = pm.Normal('beta', mu=0.0, tau=0.01, testval=0.0)
    
    # Create the probability from the logistic function
    p = pm.Deterministic('p', 1. / (1. + tt.exp(beta * time + alpha)))
    
    # Create the bernoulli parameter which uses the observed dat
    observed = pm.Bernoulli('obs', p, observed=sleep_obs)
    
    # Starting values are found through Maximum A Posterior estimation
    # start = pm.find_MAP()
    
    # Using Metropolis Hastings Sampling
    step = pm.Metropolis()
    
    # Sample from the posterior using the sampling method
    sleep_trace = pm.sample(N_SAMPLES, step=step, njobs=2)

    pm.traceplot(sleep_trace, ['alpha', 'beta'])
    pm.autocorrplot(sleep_trace, ['alpha', 'beta']);

plt.show()