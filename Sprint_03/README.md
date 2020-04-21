# D2D-B2B Site

This Sprint was designed with the purpose of providing a site-front that allows the customer to interact with the checkmate library in an intuitive manner.  This sprint will also have a limited tracking on the users requests, so that companies can be charged for the amount of queries that they use.
### Installing

This sprint is designed to have the Sprint 2 folder in the same directory as the Sprint 3, as is shown on Github, that way we could import files from the checkmate.  If the checkmate library is improperly placed, then Sprint 03 will not work correctly.

When creating your virtual environment, the .gitignore file has been customized to ignore a virtual environment with the name of 'venv'.  This is the recommendation for the name of your virtual environment.  Below is how to set that up.

``` 
py -m venv venv

(CHANGE YOUR INTERPRETER TO THE VIRTUAL ENVIRONMENT)

pip install -r pip_requirements.txt 
```

## Updating Pip Requirements

```
pip freeze > pip_requirements.txt
```

## Acknowledgements

* Brendan Van Tuyle
* Brandon Thompson
* Daniel Guill
* Jamed Hannah
* Sanjay Ranjit