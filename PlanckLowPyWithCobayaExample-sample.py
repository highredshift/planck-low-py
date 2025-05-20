#!/usr/bin/env python
# coding: utf-8

# ### May 18, 2025
# 
# This notebook is from Prince+Dunkly 2022, https://journals.aps.org/prd/abstract/10.1103/PhysRevD.105.023518. The arXiv version is not up-to-date.
# 
# I can run the notebook in full. To do that, I created a kernel "Cobaya", using a conda environment. The conda environment has to be created in $PSCRATCH (gpt says my home directory would work too), but not in the project directory: /global/cfs/projectdirs/cosmo/work/users/xhuang/xh-repos
# 
# `conda create -n cobaya-scratch python=3.10`
# 
# I then followed gpt instructions:
# 
# `conda install ipykernel`
#  
# `python -m ipykernel install --user --name cobaya-scratch --display-name "Cobaya"`
# 
# I then installed cobaya (https://cobaya.readthedocs.io/en/latest/installation.html) 
# 
# `python -m pip install cobaya --upgrade`
# 
# and then (https://cobaya.readthedocs.io/en/latest/installation_cosmo.html)
# 
# `cobaya-install cosmo -p /pscratch/sd/x/xshuang/cobaya-cosmo-scratch`
# 
# In installing the Cobaya `cosmo` package, I ran into trouble with Python 3.11. GPT was right: after creating an environment with 3.10 everything worked.
# 
# (Previously I created a conda environment (`cobaya-env`) in order to create a kernel in the project directory above, but that didn't work. That's why I created `cobaya-scratch` in $PSCRATCH. `cobaya-env` was then removed.)
# 
# 
# 

# # cobaya example
# You can run this if you have cobaya installed on your computer (see https://cobaya.readthedocs.io/en/latest/)
# 
# You will need to set the cobaya_modules_path variable below to wherever the cobaya cosmological codes and likelihoods are installed on your computer
# 
# This plots a slice the low-ell EE likelihood for different values of tau, and the low-ell TT likelihood for different values of n_s.
# 
# For more about the model wrapper of cobaya see https://cobaya.readthedocs.io/en/latest/cosmo_model.html

# In[1]:


# cobaya_modules_path='/Users/heatherp/cobaya-cosmo'

cobaya_modules_path='/pscratch/sd/x/xshuang/cobaya-cosmo-scratch'


# In[2]:


import numpy as np
import matplotlib.pyplot as plt

from cobaya.model import get_model
from cobaya.yaml import yaml_load

from cobaya.run import run


# In[3]:


'''
Notes on the ymal file below:

- Cl # probably just the spherical harmonics coefficients

- requires: {'Cl': {'ee': 29}}  # 29 means l < 30, or the low ell's. For Planck, l < 30 and l >= 30 are treated differently; see Prince thesis.

- planck_2018_highl_plik.TTTEEE_lite: null # I don't understand this line.

- I added the lines at the end, in order to sample

sampler:
  mcmc: null

- It appears that to run model = get_model(info) below twice will cause error. So everything needs to be defined in this cell.

VERY IMPORTANT:

You only want to call one of these, not both!
get_model(info): Instantiates the model and loads all likelihoods, but does NOT run sampling.

run(info): Does everything—model construction and sampling (and so will load all likelihoods).


'''


info_txt = r'''
likelihood:
  planck_low_py_EE: 
      external: import_module('planck_low_py').planck_lowE_binned_loglike_cobaya
      requires: {'Cl': {'ee': 29}}
  planck_low_py_TT: 
      external: import_module('planck_low_py').planck_lowT_binned_loglike_cobaya
      requires: {'Cl': {'tt': 29}}
  planck_2018_highl_plik.TTTEEE_lite: null
params:
  # fixed
  H0: 67
  ombh2: 0.022
  omch2: 0.12
  # sampled
  As:
    prior:
      min: 1e-9
      max: 6e-9
  ns:
    prior:
      min: 0.8
      max: 1.2
  tau:
    prior:
      min: 0.005
      max: 0.8
theory:
  camb:

sampler:
  mcmc: null
'''


# In[4]:


info = yaml_load(info_txt)
info['modules'] = cobaya_modules_path

# Set the output path for chains (adjust as needed)
# output_path = "/global/cfs/projectdirs/cosmo/work/users/xhuang/xh-repos/planck-low-py/output"

output_path = "/pscratch/sd/x/xshuang/repos/planck-low-py/output_w0wa_test8"


# Add to your info dict:
info["output"] = output_path

# it appears that to run this a second time will cause error
# model = get_model(info)


# In[5]:


# Run Cobaya
# info["sampler"] = {"mcmc": None}
updated_info, sampler = run(info)

