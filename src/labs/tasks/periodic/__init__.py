""" 
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