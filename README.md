# Web-Scarping-on-EPFO
Use Python Selenium to scrape data from the EPFO website
In this project, I have done web scarping on the EPFO website to get the payment details for the Employees. 

I have done this project using two approach because there was cpachta persent in the websitte for automating the captcha I need to do with two different approach :

1. Using python library (pytesseract)
2. Using ML model (microsoft/trocr-large-printed)

#### Purpose behind these approaches:
Python library (PyTesseract) is not able to convert image into text efficiently. Sometimes it gives wrong captcha text, that's why I'm working with the ML model to solve the captcha in an efficient manner for converting image to text.

#### Executable file:

1. Using python library (pytesseract) : run python3 web_library.py

2. Using ML model (microsoft/trocr-large-printed) : run python3 web_model.py


## Project Setup

Ensure that you have [Python3.8](https://www.python.org/downloads/release/python-380/) installed for writing script and also installed [PyTesseract](https://pypi.org/project/pytesseract/) in your Pc for Tesseract executable. 

```
virtualenv -p </path/to/python3.8> .venv
source .venv/bin/activate
pip install -r requirements.dev.txt
```
