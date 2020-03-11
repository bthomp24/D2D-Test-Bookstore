# D2D-Test-Bookstore

This Sprint was designed with the purpose of screen scraping bookstores in mind, and in doing so will be henceforth known as "Checkmate Library".  It will not retain any information.  The intention is for a user to upload a list of data to the API endpoint, this list of data will be known as "Book_Site_Data".  The Checkmate Library will use the contents of the Book_Site_Data that was passed, to search a list of sites for possible matches, and return them, as well as with a calculated rating, with the intention of rating the likeliness of the Book_Site_Data objects matching.

### Installing

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