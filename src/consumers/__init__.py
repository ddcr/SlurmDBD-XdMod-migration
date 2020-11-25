import logging

import sqlalchemy as sa
from sqlalchemy.engine.url import URL
# from sqlalchemy.orm import scoped_session
import settings
from src.consumers.models import Base, ChatMessage

logger = logging.getLogger('filling_xdmod_database')


def create_mysql_pool():
    # max_connections default for mysql = 100
    # set mysql connections to 90 and 5 for sqlalchemy buffer
    mysql_pool = sa.create_engine(URL(**settings.XDMODDB), pool_size=10,
                                  max_overflow=5, pool_recycle=3600)
    return mysql_pool


init_mysql_pool = create_mysql_pool()
Base.metadata.create_all(init_mysql_pool, checkfirst=True)
init_mysql_pool.dispose()


def batch_insert(session, result):
    """
    Start transactional insert
    """
    # save to sql database
    batch_insert = []
    for batch_object in result:
        record = session.query(ChatMessage).get({batch_object.id})
        if record:
            # logger.info('duplicate entry in db {0}'.format(batch_object.id))
            continue
        batch_insert.append(batch_object)
    if batch_insert:
        try:
            session.add_all(batch_insert)
            session.commit()
        except sa.exc.IntegrityError:
            logger.info('something HORRIBLE has happened')
            session.rollback()
    session.close()
    return True
