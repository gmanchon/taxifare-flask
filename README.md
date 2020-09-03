
DE day 4 recap

# usage

sit at the root of the project

``` bash
python train.py
```

# taxifare trainer

reuse generic minimistic trainer from scratch with:
- a transfo
- a pipeline
- iterate through the trainer on hyperparams
- upload params and metrics to mlflow
- use mlflow base class

in order to:
- download training data from gcp
- upload trained model to gcp
- iterate on trainings + mlflow
- iterate using a gridsearch + mlflow
- use a bigger machine to demonstrate the ROI of using gcp
