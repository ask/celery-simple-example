========================================================
 Simple Example of a Distributed Task Queue with Celery
========================================================

Get Started
-----------

Setup a broker as described in the Celery docs.
Create a virtualenv and ``pip install celery``.

Install RabbitMQ (and some utilities)::

    sudo apt-get install rabbitmq-server amqp-tools

By default, RabbitMQ provides a connection at::

    amqp://guest:guest@localhost:5672//

To configure RabbitMQ, see:
http://www.rabbitmq.com/configure.html


Run the Example
---------------

Starting with:
http://docs.celeryq.org/en/latest/getting-started/first-steps-with-celery.html

Make sure RabbitMQ is running, then have several terminal sessions handy.
In one terminal session, run celeryd::

    celeryd -E --loglevel=INFO # -E provides events for monitoring

In another, monitor workers::

    celeryev

In another, running Python::

    >>> from tasks import add
    >>> add.delay(6, 36)
    <AsyncResult: ...>
    >>> result = _
    >>> result.result
    42
    >>>

Look for details from celeryd logging and celeryev.


Custom Routing
--------------

This example takes the Celery quickstart further to demonstrate custom routing.
http://ask.github.com/celery/userguide/routing.html

Scenario: a request/response (e.g. HTTP) server gets a request which triggers a
process requiring a lot of computing or network I/O, and the results of the
worker process need to be stored in a database on a specific host.

Solution: line up many compute celeryd processes on available remote hosts (and
add them as needed) and one or two result celeryd processes on a host with the
target database.  Register remote celeryd processes to compute, and the
database host celeryd processes to store the results.

The ``celeryconfig.py`` configuration file defines specific queues for tasks in
``tasks.py``, where each queue has specifically defined tasks.  To simulate the
results-on-db-host scenario described here: run multiple celeryd processes with
specified queues.  In one terminal session, start a result worker::

    celeryd -E --loglevel=INFO -Q result --hostname=main

In one or more (as many as you like) terminal session, start compute workers::

    celeryd -E --loglevel=INFO -Q compute --hostname=compute1
    celeryd -E --loglevel=INFO -Q compute --hostname=compute2
    celeryd -E --loglevel=INFO -Q compute --hostname=compute3
    ...
    celeryd -E --loglevel=INFO -Q compute --hostname=computeN

In another, monitor workers::

    celeryev

In another, running Python::

    >>> from tasks import compute
    >>> for x in range(1, 51):
    ...     for y in range(1, 51):
    ...         compute.delay(x, y)
    ...
    <AsyncResult: ...> # 50 * 50 = 2500 times.
    >>>

Add compute celeryd processes and take down (Control-C) celeryd processes as
desired.  Watch ``celeryev`` for changes.

The ``compute`` task is calling the ``handle_result`` task asynchronously,
where compute tasks are being farmed out to many celeryd processes, which in
turn push their results back to a single (optionally many, but on the same
host) celeryd which handles the result.
