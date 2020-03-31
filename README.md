# Coffee Shop Full Stack

"Coffee Shop Full Stack" offers a cafe digial managing service. This application have some functionalities like below.
- Display graphics representing the ratios of ingredients in each drink.
- Allow public users to view drink names and graphics.
- Allow the shop baristas to see the recipe information.
- Allow the shop managers to create new drinks and edit existing drinks.


## Getting Started

### Prerequisites

- Python 3.6 or higher, and pip3
- Node, NPM, Git, Ionic Cli and Postgresql
- Using python virtual environment is highly recommended.

### Frontend Installation

#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing Ionic Cli

The Ionic Command Line Interface is required to serve and build the frontend. Instructions for installing the CLI  is in the [Ionic Framework Docs](https://ionicframework.com/docs/installation/cli).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```
npm install
```

#### Configure Enviornment Variables

Ionic uses a configuration file to manage environment variables. These variables ship with the transpiled software and should not include secrets.

- Open `./src/environments/environments.ts` and ensure each variable reflects the system you stood up for the backend.

#### Running Your Frontend in Dev Mode

Ionic ships with a useful development server which detects changes and transpiles as you work. The application is then accessible through the browser on a localhost port. To run the development server, cd into the `frontend` directory and run:

```
ionic serve
```

### Backend Installation

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

#### Running the backends server

From the `./src` directory, run:

```bash
FLASK_APP=api.py FLASK_ENV=development flask run
```


## API Reference.

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application requires autho0 authentication. The application get JWT Token with proper permission from `masonkim32.eu.auth0.com`.

### Endpoints

#### GET /drinks

- General: Retrieve a list of drinks from database.
- Action: GET
- URL: `http://127.0.0.1:5000/drinks`

```
{
  "drinks": [
    {
      "id": 1, 
      "recipe": [
        {
          "color": "wheat", 
          "parts": 1
        }, 
        {
          "color": "green", 
          "parts": 3
        }
      ], 
      "title": "matcha shake"
    }, 
    {
      "id": 2, 
      "recipe": [
        {
          "color": "wheat", 
          "parts": 3
        }, 
        {
          "color": "brown", 
          "parts": 1
        }
      ], 
      "title": "flatwhite"
    }, 
    {
      "id": 3, 
      "recipe": [
        {
          "color": "beige", 
          "parts": 1
        }, 
        {
          "color": "wheat", 
          "parts": 2
        }, 
        {
          "color": "brown", 
          "parts": 1
        }
      ], 
      "title": "cap"
    }, 
    {
      "id": 4, 
      "recipe": [
        {
          "color": "brown", 
          "parts": 1
        }, 
        {
          "color": "wheat", 
          "parts": 3
        }
      ], 
      "title": "chocolate milk"
    }
  ], 
  "success": true
}
```

#### GET /drinks-detail

- General: Retrieve the drink.long() data representation when the requesting
    user is valid.
- Action: GET
- URL: `http://127.0.0.1:5000/drinks-detail`

```
{
  "drinks": [
    {
      "id": 1, 
      "recipe": [
        {
          "color": "wheat", 
          "name": "milk", 
          "parts": 1
        }, 
        {
          "color": "green", 
          "name": "matcha", 
          "parts": 3
        }
      ], 
      "title": "matcha shake"
    }, 
    {
      "id": 2, 
      "recipe": [
        {
          "color": "wheat", 
          "name": "milk", 
          "parts": 3
        }, 
        {
          "color": "brown", 
          "name": "coffee", 
          "parts": 1
        }
      ], 
      "title": "flatwhite"
    }, 
    {
      "id": 3, 
      "recipe": [
        {
          "color": "beige", 
          "name": "foam", 
          "parts": 1
        }, 
        {
          "color": "wheat", 
          "name": "milk", 
          "parts": 2
        }, 
        {
          "color": "brown", 
          "name": "coffee", 
          "parts": 1
        }
      ], 
      "title": "cap"
    }, 
    {
      "id": 4, 
      "recipe": [
        {
          "color": "brown", 
          "name": "chocolate", 
          "parts": 1
        }, 
        {
          "color": "wheat", 
          "name": "milk", 
          "parts": 3
        }
      ], 
      "title": "chocolate milk"
    }
  ], 
  "success": true
}

```

#### POST /drinks

- General: Add a new drink in the drinks table when the requesting user have
    a proper permission.
- Action: POST
- URL: `http://127.0.0.1:5000/drinks`
- Header: Content-Type: application/json
- Data(JSON): {"title": "cafe latte", "recipe": "[{'name': 'foam', 'color': 'beige', 'parts': 2}, {'name': 'milk', 'color': 'wheat', 'parts': 1}, {'name': 'coffee', 'color': 'brown', 'parts': 1}]"}

```
{
  "drinks": [
    {
      "id": 5, 
      "recipe": "[{'name': 'foam', 'color': 'beige', 'parts': 2}, {'name': 'milk', 'color': 'wheat', 'parts': 1}, {'name': 'coffee', 'color': 'brown', 'parts': 1}]", 
      "title": "cafe latte"
    }
  ], 
  "success": true
}
```

#### PATCH /drinks/{int:drink_id}

- General: Update the name or recipe of the designated drinks with drink_id. Only users with proper
    permission can update drinks.
- Action: POST
- URL: `http://127.0.0.1:5000/drinks/2`
- Header: Content-Type: application/json
- Data(JSON): {"title": "flat white", "recipe": "[{'color': 'wheat', 'name': 'milk', 'parts': 2}, {'color': 'brown', 'name': 'coffee', 'parts': 2}]"}

```
{
  "drinks": [
    {
      "id": 2, 
      "recipe": "[{'color': 'wheat', 'name': 'milk', 'parts': 2}, {'color': 'brown', 'name': 'coffee', 'parts': 2}]", 
      "title": "flat white"
    }
  ], 
  "success": true
}
```

#### DELETE /drinks/{int:drink_id}

- General: Delete the corresponding row for drink_id. Only users with proper
    permission can delete drinks.
- Action: DELETE
- URL: `http://127.0.0.1:5000/drinks`

```
{
  "delete": 3,
  "success": true
}
```

### Error Handling

- Errors are returned as JSON objects

```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

- 400: Bad request
- 401: Not authorized
- 404: Resource is not found
- 405: Method not allowed
- 422: Unprocessable

## Authors

- Mason Myoungsung Kim
- Start Code provided by Udacity Team
