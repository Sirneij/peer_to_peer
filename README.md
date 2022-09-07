A barebone web API service, powered by gunicorn, that uses query paramenters to modify an in-memory data.

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
(virtualenv)$: gunicorn peer_to_peer.server:app --reload
```

You should see something like:

```bash

```
