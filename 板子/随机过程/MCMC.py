import numpy as np
import pymc3 as pm
import theano.tensor as tt
import scipy
from scipy import optimize
import matplotlib.pyplot as plt

time = np.random.rand(20)
sleep_obs = np.random.randint(0,1)

with pm.Model() as sleep_model:# 拟合一个logisit，参数alpha、beta

    # Create the alpha and beta parameters
    # Assume a normal distribution
    alpha=pm.Normal('alpha', mu=0.0, tau=0.05, testval=0.0)
    beta=pm.Normal('beta', mu=0.0, tau=0.05, testval=0.0)

    # The sleep probability is modeled as a logistic function
    p=pm.Deterministic('p', 1. / (1. +tt.exp(beta * time + alpha)))

    # Create the bernoulli parameter which uses observed data to inform the algorithm
    observed=pm.Bernoulli('obs', p, observed=sleep_obs)

    # Using Metropolis Hastings Sampling
    step=pm.Metropolis()

    # Draw the specified number of samples
    sleep_trace=pm.sample(2000, step=step)

pm.traceplot(sleep_trace, ['alpha', 'beta'])
pm.autocorrplot(sleep_trace, ['alpha', 'beta'])