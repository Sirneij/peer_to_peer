A barebone web API service, powered by gunicorn, that uses query paramenters to modify an in-memory data.

#### CAVEAT: The application may sometimes misbehave. It's barebone, as written.

## Starting locally

### Clone this project and change directory into it:

You first need to have a copy of this project. To do so, open up your terminal (PowerShell in Windows or WSL terminal) and run the following commands:

```bash
$: git clone https://github.com/Sirneij/peer_to_peer.git

$: cd peer_to_peer
```

### Create and activate virtual environment

Create and activate python virtual environment. You are free to use any python package of choice but I opted for `ven`:

```bash
$: python3 -m venv virtualenv

$: source virtualenv/bin/activate.fish
```

I used the `.fish` version of `activate` because my default shell is `fish`.

### Install dpendencies and run the application

This app does not need fancy framework, the only required dependency is `gunicorn` which serves the application. Other dependencies are not required, they only help make the code consistent and beautifull:

```bash
(virtualenv)$: pip install -r requirements.txt
```

Next, launch the application.

```bash
(virtualenv)$: gunicorn peer_to_peer.server:app --reload -w 5
```

You should see something like:

```bash
[2022-09-07 14:46:01 +0100] [10341] [INFO] Starting gunicorn 20.1.0
[2022-09-07 14:46:01 +0100] [10341] [INFO] Listening at: http://127.0.0.1:8000 (10341)
[2022-09-07 14:46:01 +0100] [10341] [INFO] Using worker: sync
[2022-09-07 14:46:01 +0100] [10342] [INFO] Booting worker with pid: 10342
```

## Make requests

There are currently the following `endpoints`, in addition to the domain `http://127.0.0.1:8000`:

- `/`: This returns the list of `users` currently in the app. If no `query` parameter is passed, you will get the following response:
  ```json
  "You cannot just view this page without a `name` query parameter."
  ```
  However, when a query parameter named `name` is passed, it gives different behaiours. If you have a url like `http://127.0.0.1:8000/?name=Admin`, you will recieve the list of all users and their details except `password`:
  ```json
  [
    {
      "id": 1,
      "username": "owolabi"
    }
  ]
  ```
  If, however, you use `?name=Owolabi`, you will get something like:
  ```json
  {
    "id": 1,
    "username": "owolabi",
    "password": "password"
  }
  ```
- `/add-user/`: This endpoint adds user to the in-memory data used by the system. You must provide the user's `name`, and `password` as query parameters, like `http://127.0.0.1:8000/add-user/?name=Owolabi&password=password`. This will return a response such as:
  ```json
  {
    "id": 1,
    "username": "owolabi",
    "password": "password"
  }
  ```
  If you try adding another user with the same username, you will receive the following response:
  ```text
  "A user with username, Owolabi, already exists."
  ```
- `/add-money/`: This endpoint deposits money into user account. It requires that you add three query parameters: `?name=<username>&password=<user_password>&amount=<amount_to_deposit>`. For instance, if `John` and `password` are the username and password of a user, and you want to deposit `$10`, the request will be, `http://127.0.0.1:8000/add-money/?name=John&amount=10&password=password`. You will get this response:
  ```json
  {
    "id": 1,
    "username": "john",
    "password": "password",
    "balance": 10
  }
  ```
  If you miss the password or its incorrect, you will get this response:
  ```json
  "You are not authorized to add money to this user's balance."
  ```
  In the case of incorrect username, you will get:
  ```json
  "A user with that name does not exist."
  ```
- `/check-balance`: As the url implies, it checks user's balance. You need to provide both `name` and `password` query parameters to make it work. If the name provided is not found, you will get:
  ```json
  "A user with that name does not exist."
  ```
  If password was not provided, you will be responded with:
  ```json
  "You must provide the user's password to check balance."
  ```
  If however, you get all the details right, you will get:
  ```json
  {
    "balance": 10
  }
  ```
- `/transfer-money-to-user`: This allows users to transfer money to another user. The query parameters required are `?from_name=<the_user_sending_money>&from_password=<the_password_of_the_user_sending>&amount=<amount_to_be_sent>&to_name=<receiver_name>`. If it goes well, you will have something like:
  ```json
  "A sum of $5 was successfully transferred to john."
  ```
- `/transfer-money-out`: Allows users to transfer money out of the app. The query parameters required are `?name=<username>&password=<user_password>&amount=<amount>&to_bank=<bank_name>`. A correct request such as `http://localhost:8000/transfer-money-out/?name=John&password=password&amount=10&to_bank=GTB` will yield:
  ```json
  "A sum of $10 was successfully transferred to GTB"
  ```
  Approriate errors are raised in case of incorrect parameters or ommission.

## Automatic test

Automatic unittests are currently being written.
