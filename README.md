# NSGA-II Algorithm

Forked from wreszelewski/nsga2 but mostly rewritten.

### Usage

cwd: Repository base.

Windows:
```shell
set PYTHONPATH=%PYTHONPATH%;%cd% && python examples
```

Unix:
```shell
$ export PYTHONPATH=${PYTHONPATH};$(pwd) && python examples
```


### Changelist

The following changes have been made to the pre-fork repository:

1. Compatible with > 3 objective problems.
    - The original nsga2 repository was only compatible with 2-objective problems.
1. Does not require the user to rescale
    - The original nsga2 implementation relied on the decision vectors to be [0,1] but this implementation can take customized bounds.
    - The previous implementation also required the objective space vectors to be standardized but this implementation abstracts over that.
1. The visualizer can now visualize up to 3 dimensions(3 objectives)
1. Removed the use of callback functions and used generators instead.
1. NSGA2 now inherits from an `ioptimizer` interface which is compatible with `iproblem` interfaces
    - This was in order to test multiple optimizers in a generic fashion.
1. Python3 Compatible
    - Certain uses of `sorted(cmp=)` made the original repository incompatible with python3 but it now runs on python3
    - Also, there is occasional use of type hinting especially around the public API


### To Do

- Write test code, since debugging this was actually quite difficult.
- Remove the use of state and try to make the methods static methods.
- Matplotlib hangs