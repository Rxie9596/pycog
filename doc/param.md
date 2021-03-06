### Rearranged trainer.py + defaults.py

Parameters
----------

params : dict
     All parameters have default values, see `pycog.defaults`.

Input
-------

    Nin : int, optional
          Number of input units.
          0
          in rnn.ou_defaults 0
    
    Cin : numpy.ndarray or Connectivity, optional
         Input weight structure.
         None
         
    baseline_in : float, optional
         Baseline input rate.
         0.2
         in rnn.ou_defaults 0
         
    var_in : float or numpy.ndarray, optional
         Variance(s) for inputs.
         0.01**2
         in rnn.ou_defaults 0.01**2
    
    distribution_in : str, optional
         Distribution for the initial input weight matrix.
         None
         in trainer: if None set to 
            if ei is not None, 'uniform'
            if ei is None, 'uniform'
         {'uniform', 'normal', 'lognormal', 'gamma',...}
                           
Recurrent
-------
    
    N : int, optional
         Number of recurrent units.
         100
         in rnn.ou_defaults 100
         
    Crec : numpy.ndarray or Connectivity, optional
         Recurrent weight structure.
         None
         in trainer: if None set to
            if ei is not None, blanced  see trainer line 249
            if ei is None, 1*(N,N) with diag=0

    train_brec : bool, optional
         Whether to train recurrent biases.
         False
         
    brec : float, optional
         Initial value of the recurrent bias.
         0
    
    train_x0 : bool, optional
         Whether to optimize the initial conditions.
         True
         in trainer : if mode = 'continuous' set to False
         
    x0 : float, optional
         Initial value of the initial conditions.
         0.1
         
    tau : float or numpy.ndarray, optional
         Time constant(s) for recurrent units.
         100
         in rnn.ou_defaults 100
    
    
    hidden_activation : str, optional
         Hidden activation function.
         'rectify'
         in rnn.ou_defaults
         'linear'
         in theanotools.py
         {'linear', 'rectify', 'rectify_power', 'sigmoid', 'tanh', 'rtanh', 'softplus'}
         in rnn.py 
         {'linear', 'rectify', 'rectify_power', 'sigmoid', 'tanh', 'rtanh', 'softmax'}
         
    var_rec : float or numpy.ndarray, optional
         If `float` or 1D `numpy.ndarray`, then recurrent units receive
         independent noise. If 2D `numpy.ndarray`, then noise is drawn
         from a multivariable normal distribution.
         0.15**2
         in rnn.ou_defaults 0.15**2
         
    rho0 : float, optional
         Spectral radius for the initial recurrent weight matrix.
         1.5
         in trainer : if ei is None, use 1.1 instead
         
    distribution_rec : str, optional
         Distribution for the initial recurrent weight matrix.
         None
         in trainer: if None set to 
            if ei is not None, 'gamma'
            if ei is None, 'normal'
         {'uniform', 'normal', 'lognormal', 'gamma',...}
Output
-------
    Nout : int, optional
         Number of output units.
         1
         in rnn.ou_defaults 0
         
    Cout : numpy.ndarray or Connectivity, optional
         Output weight structure.
         None
        
    train_bout : bool, optional
         Whether to train output biases.
         False
         
    bout : float, optional
         Initial value of the output bias
         0
         
    output_activation: str, optional
         Output activation function.
         'linear'
         in rnn.ou_defaults
         'linear'
         in theanotools.py
         {'linear', 'rectify', 'rectify_power', 'sigmoid', 'softmax'}
         in rnn.py
         {'linear', 'rectify', 'rectify_power', 'sigmoid', 'tanh', 'rtanh', 'softmax'}
    
    distribution_out : str, optional
         Distribution for the initial output weight matrix.
         None
         in trainer: if None set to 
            if ei is not None, 'uniform'
            if ei is None, 'uniform'
         {'uniform', 'normal', 'lognormal', 'gamma',...}
Others
-------

    mode : str, optional
         `continuous` or `batch` training/running mode.
         'batch'
         in rnn.ou_defaults 'batch'
         
    n_gradient : int, optional
          Minibatch size for gradient dataset.
          20
    
    n_validation : int, optional
          Minibatch size for validation dataset.
          1000
    
    gradient_batch_size : int, optional
          Number of trials to precompute
          and store in each dataset. Make
          sure the batch sizes are larger
          than the minibatch sizes.
          None
    
    validation_batch_size : int, optional
          Number of trials to precompute
          and store in each dataset. Make
          sure the batch sizes are larger
          than the minibatch sizes.
          None
                                          
         
    ei : numpy.ndarray, optional
         E/I signature.
         None
         
    ei_positive_func : str, optional
         Function to use to keep weights positive.
         'rectify'
         {'abs', 'rectify'}
    
    max_gradient_norm : float, optional
         Clip gradient if its norm is greater than.
         1                 
    
    lambda_Omega : float, optinonal
         Multiplier for the vanishing gradient regularizer.
         2

    lambda1_in, lambda1_rec, lambda1_out : float, optional
         Multipliers for L1 weight regularization.
         0
    
    lambda2_in, lambda2_rec, lambda2_out : float, optional
         Multipliers for L2 weight regularization.
         0
                 
    lambda2_r : float, optional
         Multiplier for L2 firing rate regularization.
         0
                 
    callback : function, optional
         Evaluate validation dataset.
         None
         
    performance : function, optional
         Performance measure.
         None
            
    
    terminate : function, optional
         Custom termination criterion.
         (lambda performance_history: False)

    min_error : float, optional
         Target error. Terminate if error is less than or equal.
         0
          
    learning_rate : float, optional
         Learning rate for gradient descent.
         1e-2
         
    bound : float, optional
         Lower bound for denominator in vanishing gradient regularizer.
         1e-20
         
    seed, gradient_seed, validation_seed : int, optional
         Seeds for the random number generators.
         1234, 11, 22
         
    structure : dict, optional
         Convey structure information, such as what each input represents.
         {}
         
    max_iter : int, optional
         Maximum number of iterations for gradient descent.
         int(1e7)

    dt : float, optional
         Integration time step.
         None
         in trainer: if None set to min(tau)/5 (tau defaults to 100)
         in rnn.ou_defaults 0.5
         in do.py defaults to 0.5
    
    gamma_k : float, optional
         k in Gamma(k, theta). Note mean = k*theta, var = k*theta^2.
         2
    
    checkfreq : int, optional
         Frequency with which to evaluate validation error.
         None
         in sgd.py if None, set to int(1e4)//gradient_data.minibatch_size
         
    patience : int, optional
         Terminate training if the objective function doesn't change
         for longer than `patience`.
         None
         in sgd.py if None, set to 100*checkfreq
    


Unknown 
-------
parameters that are in the default list while not in trainer.py;
there is not parameter in trainer list that are not present in the default list

    rectify_inputs :
         True
         Used in dataset.py line 206
         in rnn.ou_defaults False
                    
    extra_info : 
         {}
    
    tau_in : 
         100 
         
    momentum : 
         False, # Not used currently
    
    method :
         'sgd'  # Not used currently
         
         
### rnn.py specify only when using rnn.py

    'threshold': 1e-4,
        clip_weights threshold
    
    'sigma0':    0
        noise to initial recurrent units values
            


### Original parameters list in trainer.py
```
    Parameters
    ----------

    params : dict
             All parameters have default values, see `pycog.defaults`.

      Entries
      -------

      Nin : int, optional
            Number of input units.
            0
            
      N : int, optional
          Number of recurrent units.
          100

      Nout : int, optional
             Number of output units.
             1

      train_brec : bool, optional
                   Whether to train recurrent biases.

      brec : float, optional
             Initial value of the recurrent bias.

      train_bout : bool, optional
                   Whether to train output biases.

      bout : float, optional
             Initial value of the output bias

      train_x0 : bool, optional
                 Whether to optimize the initial conditions.

      x0 : float, optional
           Initial value of the initial conditions.

      mode : str, optional
             `continuous` or `batch` training/running mode.

      tau : float or numpy.ndarray, optional
            Time constant(s) for recurrent units.

      Cin : numpy.ndarray or Connectivity, optional
            Input weight structure.

      Crec : numpy.ndarray or Connectivity, optional
             Recurrent weight structure.

      Cout : numpy.ndarray or Connectivity, optional
             Output weight structure.

      ei : numpy.ndarray, optional
           E/I signature.

      ei_positive_func : str, optional
                         Function to use to keep weights positive.

      hidden_activation : str, optional
                          Hidden activation function.

      output_activation: str, optional
                         Output activation function.

      n_gradient : int, optional
                   Minibatch size for gradient dataset.

      n_validation : int, optional
                     Minibatch size for validation dataset.

      gradient_batch_size, validation_batch_size : int, optional
                                                   Number of trials to precompute
                                                   and store in each dataset. Make
                                                   sure the batch sizes are larger
                                                   than the minibatch sizes.

      lambda_Omega : float, optinonal
                     Multiplier for the vanishing gradient regularizer.

      lambda1_in, lambda1_rec, lambda1_out : float, optional
                                             Multipliers for L1 weight regularization.

      lambda2_in, lambda2_rec, lambda2_out : float, optional
                                             Multipliers for L2 weight regularization.

      lambda2_r : float, optional
                  Multiplier for L2 firing rate regularization.

      callback : function, optional
                 Evaluate validation dataset.

      performance : function, optional
                    Performance measure.

      terminate : function, optional
                  Custom termination criterion.

      min_error : float, optional
                  Target error. Terminate if error is less than or equal.

      learning_rate : float, optional
                      Learning rate for gradient descent.

      max_gradient_norm : float, optional
                          Clip gradient if its norm is greater than.

      bound : float, optional
              Lower bound for denominator in vanishing gradient regularizer.

      baseline_in : float, optional
                    Baseline input rate.

      var_in : float or numpy.ndarray, optional
               Variance(s) for inputs.

      var_rec : float or numpy.ndarray, optional
                If `float` or 1D `numpy.ndarray`, then recurrent units receive
                independent noise. If 2D `numpy.ndarray`, then noise is drawn
                from a multivariable normal distribution.

      seed, gradient_seed, validation_seed : int, optional
                                             Seeds for the random number generators.

      structure : dict, optional
                  Convey structure information, such as what each input represents.

      rho0 : float, optional
             Spectral radius for the initial recurrent weight matrix.

      max_iter : int, optional
                 Maximum number of iterations for gradient descent.

      dt : float, optional
           Integration time step.

      distribution_in : str, optional
                        Distribution for the initial input weight matrix.

      distribution_rec : str, optional
                         Distribution for the initial recurrent weight matrix.

      distribution_out : str, optional
                         Distribution for the initial output weight matrix.

      gamma_k : float, optional
                k in Gamma(k, theta). Note mean = k*theta, var = k*theta^2.

      checkfreq : int, optional
                  Frequency with which to evaluate validation error.

      patience : int, optional
                 Terminate training if the objective function doesn't change
                 for longer than `patience`.
```

### Original parameters default value in defaults.py
```
    'extra_info':            {},
    'Nin':                   0,
    'N':                     100,
    'Nout':                  1,
    'rectify_inputs':        True,
    'train_brec':            False,
    'brec':                  0,
    'train_bout':            False,
    'bout':                  0,
    'train_x0':              True,
    'x0':                    0.1,
    'mode':                  'batch',
    'tau':                   100,
    'tau_in':                100,
    'Cin':                   None,
    'Crec':                  None,
    'Cout':                  None,
    'ei':                    None,
    'ei_positive_func':      'rectify',
    'hidden_activation':     'rectify',
    'output_activation':     'linear',
    'n_gradient':            20,
    'n_validation':          1000,
    'gradient_batch_size':   None,
    'validation_batch_size': None,
    'lambda_Omega':          2,
    'lambda1_in':            0,
    'lambda1_rec':           0,
    'lambda1_out':           0,
    'lambda2_in':            0,
    'lambda2_rec':           0,
    'lambda2_out':           0,
    'lambda2_r':             0,
    'callback':              None,
    'performance':           None,
    'terminate':             (lambda performance_history: False),
    'min_error':             0,
    'learning_rate':         1e-2,
    'max_gradient_norm':     1,
    'bound':                 1e-20,
    'baseline_in':           0.2,
    'var_in':                0.01**2,
    'var_rec':               0.15**2,
    'seed':                  1234,
    'gradient_seed':         11,
    'validation_seed':       22,
    'structure':             {},
    'rho0':                  1.5,
    'max_iter':              int(1e7),
    'dt':                    None,
    'distribution_in':       None,
    'distribution_rec':      None,
    'distribution_out':      None,
    'gamma_k':               2,
    'checkfreq':             None,
    'patience':              None,
    'momentum':              False, # Not used currently
    'method':                'sgd'  # Not used currently
```

### Original parameters default value in RNN.py
```

    defaults = {
        'threshold': 1e-4,
        'sigma0':    0
        }
    
    ou_defaults = {
        'N':                 100,
        'Nin':               0,
        'Nout':              0,
        'hidden_activation': 'linear',
        'output_activation': 'linear',
        'baseline_in':       0,
        'rectify_inputs':    False,
        'var_in':            0.01**2,
        'var_rec':           0.15**2,
        'dt':                0.5,
        'tau':               100,
        'mode':              'batch'
        }
```