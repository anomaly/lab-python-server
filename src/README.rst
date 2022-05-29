*****************************************
A theatre inspired layout for Python apps
*****************************************

This document is a contemplation on the structure of Python projects as we move to a containerized architecture. Previously we've grouped files by role e.g ``worker`` or ``api``. Going forward it makes sense to group various things by purpose e.g authentication, user accounts, and then application specific functionality.

Each work of theatre is divided up into *acts* which is further divided up into *scenes*. Further there are *tasks* around the scene or act, e.g rearranging the stage or props. Drawing inspiration from this, the proposed structure of project is as follows:

At the root of the package we have:

- ``__init__.py`` which declare the Python package
- ``db.py``, providing the database connection
- ``config.py``, providing the configuration of the application read from the environment
- ``api.py```, providing the API application run by the containerized service
- ``celery.py`` providing the `Celery` application used both to queue and consume the tasks
- ``models`` is a folder that houses the SQLAlchemy models
- ``schema`` is a folder that houses the `pydantic` models used to consume and produce the API payloads

The containers use `celery:app` or `api:app` to run the queue processor or API endpoints.

Drawing attention to the ``acts`` folder, this is where the functionality of the application lives. Each act is named by what it provides e.g ``auth``, ``message``, ``thread`` or whatever else makes sense for the application.

Each ``act`` has two packages one called ``scenes`` and the other ``tasks``:

- ``scenes`` is where the playable or actions live, e.g API endpoint handlers
- ``tasks``` are where background tasks or things that happen outside of the ``scene`` live, but occur as a result or or to support a ``scene``

``tasks`` are consumed and managed by the ``celery:app``.

How you divide up your ``scenes`` is up to you and depends on the use case of the application, however they must all aggregate to the ``__init__.py`` at the `act` level.