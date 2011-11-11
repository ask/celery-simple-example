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
