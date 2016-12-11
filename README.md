# TimeFlies

## Installation

In order to install from source code one should run

```bash
    git clone git@github.com:maremun/TimeFlies.git
    pip install -r TimeFlies/requirements.txt
    pip install -i TimeFlies
```

Web service that uses wtb hook to handle updates could be run with

```bash
    ./run.py
```

from root directory of repository. In order to fetch update in long polling manner start

```bash
    timeflies loop
```

## Settings

There are several the most important parameters to define that are listed bellow.

1. `DEBUG`. Default value is `True`.
2. `API_TOKEN`. Default value is `None`. One should set this value up.
3. `DB_URI`. Default value is `sqlite:///var/timeflies.db` from the root of repository.

All these settings could be overrided in module `timeflies_settings` in working directory.

One can check is token valid or not or just get account info if one run the following

```bash
    timeflies me
```
