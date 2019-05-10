from __future__ import division

import numpy as np

from pycog import tasktools

#-----------------------------------------------------------------------------------------
# Network structure
#-----------------------------------------------------------------------------------------

Nin  = 1
N    = 100
Nout = 2

# -----------------------------------------------------------------------------------------
# Task structure
# -----------------------------------------------------------------------------------------

intensity_range  = [1]
nconditions      = 5*len(intensity_range)
pcatch           = 1/(nconditions + 1)

def generate_trial(rng, dt, params):
    # -------------------------------------------------------------------------------------
    # Select task condition
    # -------------------------------------------------------------------------------------

    catch_trial = False
    if params['name'] in ['gradient', 'test']:
        if params.get('catch', rng.rand() < pcatch):
            catch_trial = True
        else:
            intensity = params.get('intensity', rng.choice(intensity_range))
    elif params['name'] == 'validation':
        b = params['minibatch_index'] % (nconditions + 1)
        if b == 0:
            catch_trial = True
        else:
            intensity = intensity_range[0]
    else:
        raise ValueError("Unknown trial type.")

    # -------------------------------------------------------------------------------------
    # Epochs
    # -------------------------------------------------------------------------------------

    t_foward_min = 80
    t_foward_avg = 800
    t_foward_max = 1500

    t_stimulus = 300

    t_reversal_min = 80
    t_reversal_avg = 500
    t_reversal_max = 1500

    if catch_trial:
        epochs = {'T': tasktools.truncated_exponential(rng, dt, t_foward_avg,
                                                       xmin=t_foward_min, xmax=t_foward_max)}
    else:
        if params['name'] == 'test':
            forward = tasktools.truncated_exponential(rng, dt, t_foward_avg,
                                                      xmin=t_foward_min, xmax=t_foward_min)
        else:
            forward = tasktools.truncated_exponential(rng, dt, t_foward_avg,
                                                      xmin=t_foward_min, xmax=t_foward_max)
        stimulus = t_stimulus
        reversal = tasktools.truncated_exponential(rng, dt, t_reversal_avg,
                                                   xmin=t_reversal_min, xmax=t_reversal_max)
        T = forward + stimulus + reversal

        epochs = {'forward': (0, forward),
                  'stimulus': (forward, forward + stimulus),
                  'reversal': (forward + stimulus, T),
                  'T': T}

    # -------------------------------------------------------------------------------------
    # Trial info
    # -------------------------------------------------------------------------------------

    t, e  = tasktools.get_epochs_idx(dt, epochs) # Time, task epochs in discrete time
    trial = {'t': t, 'epochs': epochs}           # Trial

    # Save e info
    trial['e'] = e

    if catch_trial:
        trial['info'] = {}
    else:
        # Trial info
        trial['info'] = {'intensity': intensity}

    #-------------------------------------------------------------------------------------
    # Inputs
    #-------------------------------------------------------------------------------------

    X = np.zeros((len(t), Nin))
    if not catch_trial:
        # Stimulus
        X[e['stimulus']] = intensity

    trial['inputs'] = X

    #-------------------------------------------------------------------------------------
    # Target output
    #-------------------------------------------------------------------------------------

    if params.get('target_output', False):
        Y = np.zeros((len(t), Nout)) # Output matrix
        M = np.zeros_like(Y)         # Mask matrix

        # Hold values
        hi = 1
        lo = 0.2

        if catch_trial:
            Y[:, 0] = hi   # forward module output
            Y[:, 1] = lo   # reversal module output
            M[:] = 1
        else:
            # forward period
            Y[e['forward'], 0] = hi    # forward module output
            Y[e['forward'], 1] = lo    # reversal module output

            # reversal periods
            Y[e['reversal'], 0] = lo     # forward module output
            Y[e['reversal'], 1] = hi     # reversal module output

            # Only care about forward and reversal periods
            M[e['forward']+e['reversal'],:] = 1

        # Outputs and mask
        trial['outputs'] = Y
        trial['mask']    = M

    #-------------------------------------------------------------------------------------

    return trial


# Performance measure
performance = tasktools.perfomance_f2r

# Termination criterion
TARGET_PERFORMANCE = 85
def terminate(performance_history):
    return np.mean(performance_history[-5:]) > TARGET_PERFORMANCE

# Validation dataset
n_validation = 100*(nconditions + 1)