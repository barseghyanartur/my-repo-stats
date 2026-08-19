=============
My Repo Stats
=============

A small static dashboard for your Python projects showing:

- Daily **PyPI downloads** 
- Total number of **GitHub stars**

Data is fetched automatically via GitHub Pages every day.

What it does
============

* Shows a table of your packages and their daily download counts
* Shows a table of your GitHub repos and their star counts
* Updates daily via GitHub Actions (no manual work needed)
* Stores full history — you can see trends over time
* Runs locally with one command for development

Quick start
===========

1. Clone the repo::

    git clone https://github.com/barseghyanartur/my-repo-stats.git
    cd my-repo-stats

2. Set up credentials::

    make init        # creates .env — fill in your API keys

3. Install and fetch data::

    make install
    make update

4. Preview locally::

    make serve       # open http://localhost:8000

Configuration
=============

Edit ``pypi_packages.json`` to track PyPI packages:

.. code-block:: json

   ["pytest", "requests", "flask"]

Edit ``github_repos.json`` to track GitHub repos (stars):

.. code-block:: json

   ["faker-file", "transliterate", "ska"]

Run ``make update`` after any change.

Environment variables
=====================

Set these in ``.env`` (for local use) or in GitHub Actions secrets (for CI):

* ``PEPY_API_KEY`` — get it from https://pepy.tech (Account → API, Pro plan required)
* ``GITHUB_TOKEN`` — get it from https://github.com/settings/tokens (``repo`` scope; optional, only needed for star tracking)
* ``GITHUB_USERNAME`` — your GitHub username (required for star tracking)

Deploying to GitHub Pages
=========================

1. Go to **Settings → Pages → Source** and select **GitHub Actions**
2. Add the secrets listed above in **Settings → Secrets and variables → Actions**
3. Push to ``main`` or wait for the daily run (18:00 UTC)

Your dashboard will be at ``https://<username>.github.io/<repo-name>``

Available commands
==================

.. code-block:: bash

   make help          # Show all targets
   make init          # Create .env from .env.example
   make install       # Install Python dependencies
   make update        # Fetch data from APIs
   make serve         # Run local dev server
   make test          # Run tests
   make clean         # Remove generated data files

License
=======

MIT
