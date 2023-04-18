""" Example of periodic task using Celery

    This is a simple example of a periodic task using Celery.
    for further documentation please refer to:
    https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html

"""


def setup_periodic_tasks(sender, **kwargs):
    """ Wireup the tasks that have to be run on a schedule
    """
    sender.add_periodic_task(1.0,
        check_every_so_often.s('a periodic task running'),
        name='add every minute')

async def check_every_so_often(arg):
    import logging
    logging.error(arg)