# Installation

## Virtualenv

Because Scipy does not compile on many systems nowadays, install it
using your systems package manager and create a virtualenv with the
`--system-site-packages` option and activate it:

    sudo pkg install py39-scipy  # FreeBSD
    mkdir venv
    python -m venv --system-site-packages venv/py39-system
    . ./venv/py39-system/bin/activate
