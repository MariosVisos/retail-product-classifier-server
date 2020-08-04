# retail-product-classifier-server

Flask web application

## Description

Backend server to be used with the [retail-product-classifier](https://github.com/MariosVisos/retail-product-classifier "retail-product-classifier client repository") client.

## Getting Started

### Dependencies

The python version used is 3.8.2. See either requirements.txt or PIPFILE in order to view dependencies and their corresponding versions.

### Installing

Create a .env file same as the .env.example file and set your values.
e.g.
`JWT_SECRET_KEY=random-jwt-key`
`APP_SECRET_KEY=random-app-key`
`APPLICATION_SETTINGS=default_config.py`
`EMAIL_USER=random@gmail.com`
`EMAIL_PASSWORD=random-password`

There are two ways to install the app, either with Docker or without.

Installing without Docker:

Run `python3 -m venv env.` to create a virtual environment.
Activate your venv by typing `env\Scripts\activate` if you're on Windows or 
`source tutorial-env/bin/activate` if you're on either Unix or MacOS.
Run `pip install -r requirements.txt` in order to install all the dependencies in your virtual environment.

### Running the server

Inside the virtual environment run `python src/app.py`.
The app is running at `http://YOUR_WLAN_IPV4_IP_ADDRESS:5000`


## Acknowledgments

* https://github.com/4viM/PIPELINE
* https://github.com/eg4000/SKU110K_CVPR19
