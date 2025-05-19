'''
5/19/25: this runs but does not provide output
'''


from cobaya.run import run

info = {
    "params": {
        "x": {
            "prior": {"min": 0, "max": 10},
            "proposal": 0.5,
            "latex": "x"
        }
    },
    "likelihood": {
        "gaussian": {
            "mu": 5,
            "sigma": 1
        }
    },
    "theory": {},
    "sampler": {
        "mcmc": {
            "max_tries": 100000,
            "burn_in": 1000,
            "Rminus1_stop": 0.01
        }
    },
    "output": "gaussian_example_output"
}

from cobaya.likelihood import Likelihood
from math import log, pi

class gaussian(Likelihood):
    def logp(self, **params):
        x = params["x"]
        mu = self.mu
        sigma = self.sigma
        return -0.5 * ((x - mu) / sigma) ** 2 - 0.5 * log(2 * pi * sigma ** 2)

updated_info, sampler = run(info)
