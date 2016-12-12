# TimeFlies

## Installation

To install from source code:

```bash
    git clone git@github.com:maremun/TimeFlies.git
    pip install -r TimeFlies/requirements.txt
    pip install -i TimeFlies
```

Run a web service that uses webhook to handle updates by executing:

```bash
    ./run.py
```

from root directory of repository. 

Getting updates by long polling:

```bash
    timeflies loop
```

## Settings

There are several most important parameters to define that are listed below.

1. `DEBUG`. Default value is `True`.
2. `API_TOKEN`. Default value is `None`. One should set this value (you can get API_TOKEN from Telegram's BotFather).
3. `DB_URI`. Default value is `sqlite:///var/timeflies.db` from the root of the repository.

All the settings could be overridden in module `timeflies_settings` in the working directory.

One can check if token is valid by running the following (it also provides account information)

```bash
    timeflies me
```
