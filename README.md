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
Installing environment (not on MacOS):
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
conda install mkl
pip install mkl
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
