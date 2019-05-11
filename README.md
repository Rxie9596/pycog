# Train excitatory-inhibitory recurrent neural networks for cognitive tasks

## Requirements

This code is written in Python 2.7 and requires

* [Theano 0.7](http://deeplearning.net/software/theano/)

Optional but recommended if you plan to run many trials with the trained networks outside of Theano:

* [Cython](http://cython.org/)

Optional but recommended for analysis and visualization of the networks (including examples from the paper):

* matplotlib

The code uses (but doesn't require) one function from the [NetworkX](https://networkx.github.io/) package to check if the recurrent weight matrix is connected (every unit is reachable by every other unit), which is useful if you plan to train very sparse connection matrices.

## Installation

Because you will eventually want to modify the `pycog` source files, we recommend that you "install" by simply adding the `pycog` directory to your `$PYTHONPATH`, and building the Cython extension to (slightly) speed up Euler integration for testing the networks by typing

```
python setup.py build_ext --inplace
```

You can also perform a "standard" installation by going to the `pycog` directory and typing

```
python setup.py install
```

## Examples

Example task specifications, including those used to generate the figures in the paper, can be found in `examples/models`.

Training and testing networks involves some boring logistics, especially regarding file paths. You may find the script `examples/do.py` helpful as you start working with your own networks. For instance, to train a new network we can just type (from the `examples` directory)

```
python do.py models/sinewave train
```

For this particular example we've also directly included code for training and plotting the result, so you can simply type

```
python models/sinewave.py
```

## Notes

* The default recurrent noise level (used for most of the tasks in our paper) is rather high. When training a new task start with a value of `var_rec` that is small, then increase the noise for more robust solutions.

* A list of parameters and their default values can be found in `defaults.py`

* The default time step is also relatively large, so always test with a smaller time step (say 0.05) and re-train with a smaller step size if the results change.

* By default, recurrent and output biases are set to zero. If you encounter difficulties with training, try including the biases by setting `train_brec = True` and/or `train_bout = True`.

* If you still have difficulties with training, try changing the value of `lambda_Omega`, the multiplier for the vanishing-gradient regularizer.

* It's common to see the following warning when running Theano:

  ```
  RuntimeWarning: numpy.ndarray size changed, may indicate binary incompatibility
  rval = __import__(module_name, {}, {}, [module_name])
  ```

  This is almost always innocuous and can be safely ignored.

## Acknowledgments

This code would not be possible without

* On the difficulty of training recurrent neural networks.                                         
  R. Pascanu, T. Mikolov, & Y. Bengio, ICML 2013.                                                  
  https://github.com/pascanur/trainingRNNs

## License

MIT

## Citation

This code is the product of work carried out in the group of [Xiao-Jing Wang at New York University](http://www.cns.nyu.edu/wanglab/). If you find our code helpful to your work, consider giving us a shout-out in your publications:

* Song, H. F.\*, Yang, G. R.\*, & Wang, X.-J. "Training Excitatory-Inhibitory Recurrent Neural Networks for Cognitive Tasks: A Simple and Flexible Framework." *PLoS Comp. Bio.* 12, e1004792 (2016). (\* = equal contribution)

## Added by Yu Xie

Installing environment (on MacOS): do not build the .c file
```
conda create --name RNN python=2.7
source activate RNN

pip install numpy
pip install theano
pip install cython
pip install networkx
pip install matplotlib
```
Additional,
```
conda install mkl-service
```
The following just for reference
```
conda install mkl
pip install mkl
```

Installing environment (currently not working):
```
conda create --name RNN python=2.7
source activate RNN

pip install numpy==1.6.2
pip install scipy==0.16
pip install theano==0.7
pip install cython==0.23.4
pip install networkx==1.10
pip install matplotlib==1.4.3
```

Other useful commands:
```
conda remove --name RNN --all
```
Add the following to `/.bash_profile`(on MacOS) or `/.bash_profile`(on Linux) to add pycog to `$PYTHONPATH`
```
export PYTHONPATH="${PYTHONPATH}:/Users/yuxie/Lab/RNN/pycog"
```
To show `$PYTHONPATH`
```
echo $PYTHONPATH
```

show package
```
conda list
pip freeze
```

### Actions to perform
1. traning network
```
python do.py models/task_name train
```
2. plot cost history
```
python do.py models/task_name costs
```
3. plot network structure
```
python do.py models/task_name structure init            # plot initial structure
python do.py models/task_name structure                 # plot structure after training
python do.py models/task_name structure selectivity     # sort by selectivity or other criteria
```
4. plot network output when there is no input (restingstate)
```
python do.py models/task_name restingstate init    # plot initial restingstate response
python do.py models/task_name restingstate         # plot restingstate response after training
```
5. run analysis
```
python do.py models/task_name run analysis_script actions
```
6. check log file
```
python do.py models/task_name check
```
7. clean up files and documents
```
python do.py models/task_name clean
```
8. submit jobs when using on the cluster
```
python do.py models/task_name submit
```
9. plot performance (if performance is defined)
plot performance without target
```
python do.py models/worm_reversal_con performance
```

plot performance with target
```
python do.py models/worm_reversal_con performance 85
```

## All used commands
```
python all.py -s
=> Perceptual decision-making task
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_varstim clean
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_varstim train -s 1001 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_varstim run /Users/yuxie/Lab/RNN/pycog/examples/analysis/rdm trials 4000 --dt_save 20
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_varstim run /Users/yuxie/Lab/RNN/pycog/examples/analysis/rdm sort_stim_onset
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_varstim run /Users/yuxie/Lab/RNN/pycog/examples/analysis/rdm units_stim_onset
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_rt clean
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_rt train -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_rt run /Users/yuxie/Lab/RNN/pycog/examples/analysis/rdm trials 1500 --dt_save 10
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_rt run /Users/yuxie/Lab/RNN/pycog/examples/analysis/rdm sort_response
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_rt run /Users/yuxie/Lab/RNN/pycog/examples/analysis/rdm units_response
   python /Users/yuxie/Lab/RNN/pycog/paper/fig_rdm.py
=> Perceptual decision-making task (structure)
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_nodale clean
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_nodale train -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_nodale run /Users/yuxie/Lab/RNN/pycog/examples/analysis/rdm trials 2000 --dt_save 100
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_nodale run /Users/yuxie/Lab/RNN/pycog/examples/analysis/rdm selectivity
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_dense clean
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_dense train -s 101 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_dense run /Users/yuxie/Lab/RNN/pycog/examples/analysis/rdm trials 2000 --dt_save 100
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_dense run /Users/yuxie/Lab/RNN/pycog/examples/analysis/rdm selectivity
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_fixed clean
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_fixed train -s 1001 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_fixed run /Users/yuxie/Lab/RNN/pycog/examples/analysis/rdm trials 2000 --dt_save 100
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_fixed run /Users/yuxie/Lab/RNN/pycog/examples/analysis/rdm selectivity
   python /Users/yuxie/Lab/RNN/pycog/paper/fig_structure.py
=> Context-dependent integration task
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante clean
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante train -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante run /Users/yuxie/Lab/RNN/pycog/examples/analysis/mante trials 200 --dt_save 20
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante run /Users/yuxie/Lab/RNN/pycog/examples/analysis/mante sort
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante run /Users/yuxie/Lab/RNN/pycog/examples/analysis/mante regress
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante run /Users/yuxie/Lab/RNN/pycog/examples/analysis/mante units
   python /Users/yuxie/Lab/RNN/pycog/paper/fig_mante.py
=> Context-dependent integration task (areas)
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante_areas clean
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante_areas train -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante_areas run /Users/yuxie/Lab/RNN/pycog/examples/analysis/mante trials 200 --dt_save 20
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante_areas run /Users/yuxie/Lab/RNN/pycog/examples/analysis/mante sort
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante_areas run /Users/yuxie/Lab/RNN/pycog/examples/analysis/mante regress
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante_areas run /Users/yuxie/Lab/RNN/pycog/examples/analysis/mante units
   python /Users/yuxie/Lab/RNN/pycog/paper/fig_mante_areas.py
=> Connectivity for sequence execution task
   python /Users/yuxie/Lab/RNN/pycog/paper/fig_connectivity.py
=> Multisensory integration task
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/multisensory clean
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/multisensory train -s 111 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/multisensory run /Users/yuxie/Lab/RNN/pycog/examples/analysis/multisensory trials 500 --dt_save 20
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/multisensory run /Users/yuxie/Lab/RNN/pycog/examples/analysis/multisensory sort
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/multisensory run /Users/yuxie/Lab/RNN/pycog/examples/analysis/multisensory units
   python /Users/yuxie/Lab/RNN/pycog/paper/fig_multisensory.py
=> Parametric working memory task
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/romo clean
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/romo train -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/romo run /Users/yuxie/Lab/RNN/pycog/examples/analysis/romo trials 100 --dt_save 20
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/romo run /Users/yuxie/Lab/RNN/pycog/examples/analysis/romo sort
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/romo run /Users/yuxie/Lab/RNN/pycog/examples/analysis/romo units
   python /Users/yuxie/Lab/RNN/pycog/paper/fig_romo.py
=> Eye-movement sequence execution task
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/lee clean
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/lee train -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/lee run /Users/yuxie/Lab/RNN/pycog/examples/analysis/lee trials 100 --dt_save 2
   python /Users/yuxie/Lab/RNN/pycog/paper/fig_lee.py
=> Performance
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_varstim clean --seed 1 --suffix _s1
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_varstim train --seed 1 --suffix _s1 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_varstim clean --seed 2 --suffix _s2
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_varstim train --seed 2 --suffix _s2 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_varstim clean --seed 3 --suffix _s3
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_varstim train --seed 3 --suffix _s3 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_varstim clean --seed 4 --suffix _s4
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_varstim train --seed 4 --suffix _s4 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_varstim clean --seed 5 --suffix _s5
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_varstim train --seed 5 --suffix _s5 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_rt clean --seed 1 --suffix _s1
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_rt train --seed 1 --suffix _s1 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_rt clean --seed 2 --suffix _s2
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_rt train --seed 2 --suffix _s2 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_rt clean --seed 3 --suffix _s3
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_rt train --seed 3 --suffix _s3 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_rt clean --seed 4 --suffix _s4
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_rt train --seed 4 --suffix _s4 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_rt clean --seed 5 --suffix _s5
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_rt train --seed 5 --suffix _s5 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_nodale clean --seed 1 --suffix _s1
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_nodale train --seed 1 --suffix _s1 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_nodale clean --seed 2 --suffix _s2
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_nodale train --seed 2 --suffix _s2 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_nodale clean --seed 3 --suffix _s3
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_nodale train --seed 3 --suffix _s3 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_nodale clean --seed 4 --suffix _s4
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_nodale train --seed 4 --suffix _s4 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_nodale clean --seed 5 --suffix _s5
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_nodale train --seed 5 --suffix _s5 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_dense clean --seed 1 --suffix _s1
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_dense train --seed 1 --suffix _s1 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_dense clean --seed 2 --suffix _s2
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_dense train --seed 2 --suffix _s2 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_dense clean --seed 3 --suffix _s3
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_dense train --seed 3 --suffix _s3 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_dense clean --seed 4 --suffix _s4
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_dense train --seed 4 --suffix _s4 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_dense clean --seed 5 --suffix _s5
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_dense train --seed 5 --suffix _s5 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_fixed clean --seed 1 --suffix _s1
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_fixed train --seed 1 --suffix _s1 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_fixed clean --seed 2 --suffix _s2
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_fixed train --seed 2 --suffix _s2 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_fixed clean --seed 3 --suffix _s3
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_fixed train --seed 3 --suffix _s3 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_fixed clean --seed 4 --suffix _s4
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_fixed train --seed 4 --suffix _s4 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_fixed clean --seed 5 --suffix _s5
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/rdm_fixed train --seed 5 --suffix _s5 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante clean --seed 1 --suffix _s1
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante train --seed 1 --suffix _s1 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante clean --seed 2 --suffix _s2
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante train --seed 2 --suffix _s2 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante clean --seed 3 --suffix _s3
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante train --seed 3 --suffix _s3 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante clean --seed 4 --suffix _s4
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante train --seed 4 --suffix _s4 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante clean --seed 5 --suffix _s5
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante train --seed 5 --suffix _s5 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante_areas clean --seed 1 --suffix _s1
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante_areas train --seed 1 --suffix _s1 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante_areas clean --seed 2 --suffix _s2
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante_areas train --seed 2 --suffix _s2 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante_areas clean --seed 3 --suffix _s3
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante_areas train --seed 3 --suffix _s3 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante_areas clean --seed 4 --suffix _s4
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante_areas train --seed 4 --suffix _s4 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante_areas clean --seed 5 --suffix _s5
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/mante_areas train --seed 5 --suffix _s5 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/multisensory clean --seed 1 --suffix _s1
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/multisensory train --seed 1 --suffix _s1 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/multisensory clean --seed 2 --suffix _s2
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/multisensory train --seed 2 --suffix _s2 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/multisensory clean --seed 3 --suffix _s3
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/multisensory train --seed 3 --suffix _s3 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/multisensory clean --seed 4 --suffix _s4
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/multisensory train --seed 4 --suffix _s4 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/multisensory clean --seed 5 --suffix _s5
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/multisensory train --seed 5 --suffix _s5 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/romo clean --seed 1 --suffix _s1
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/romo train --seed 1 --suffix _s1 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/romo clean --seed 2 --suffix _s2
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/romo train --seed 2 --suffix _s2 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/romo clean --seed 3 --suffix _s3
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/romo train --seed 3 --suffix _s3 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/romo clean --seed 4 --suffix _s4
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/romo train --seed 4 --suffix _s4 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/romo clean --seed 5 --suffix _s5
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/romo train --seed 5 --suffix _s5 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/lee clean --seed 1 --suffix _s1
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/lee train --seed 1 --suffix _s1 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/lee clean --seed 2 --suffix _s2
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/lee train --seed 2 --suffix _s2 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/lee clean --seed 3 --suffix _s3
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/lee train --seed 3 --suffix _s3 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/lee clean --seed 4 --suffix _s4
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/lee train --seed 4 --suffix _s4 -g0
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/lee clean --seed 5 --suffix _s5
   python /Users/yuxie/Lab/RNN/pycog/examples/do.py /Users/yuxie/Lab/RNN/pycog/examples/models/lee train --seed 5 --suffix _s5 -g0
   python /Users/yuxie/Lab/RNN/pycog/paper/fig_performance.py

```


