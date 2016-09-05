import logging
import os

import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, sessionmaker

# from veredas_settings import *
from src.consumers.models import Base, ChatMessage

logger = logging.getLogger('filling_xdmod_database')

SETTINGS_XDMOD_DB_FILE = os.path.expanduser("~/.slurm/xdmod_db_settings.py")
if os.path.exists(SETTINGS_XDMOD_DB_FILE):
    with open(SETTINGS_XDMOD_DB_FILE) as f:
        exec(f.read())
else:
    raise Exception('{} not found. Please create it'
                    ' and put your DATABASE settings'
                    ' in it (database, password, '
                    'host, etc).'.format(SETTINGS_XDMOD_DB_FILE))


def create_mysql_pool():
    mysql_host = MYSQL_HOST
    mysql_port = MYSQL_PORT
    mysql_db = MYSQL_DB
    mysql_user = MYSQL_USER
    mysql_socket = MYSQL_SOCKET
    mysql_passwd = MYSQL_PASSWD

    # max_connections default for mysql = 100
    # set mysql connections to 90 and 5 for sqlalchemy buffer
    if mysql_socket:
        mysql_url = 'mysql://{user}:{passwd}@{host}?unix_socket={sock}'\
                    .format(user=mysql_user,
                            passwd=mysql_passwd,
                            host=mysql_host,
                            sock=mysql_socket)
    else:
        mysql_url = 'mysql://{user}:{passwd}@{host}'.format(
            user=mysql_user,
            passwd=mysql_passwd,
            host=mysql_host)

    mysql_pool = sa.create_engine(mysql_url,
                                  pool_size=10,
                                  max_overflow=5,
                                  pool_recycle=3600)
    try:
        mysql_pool.execute("USE {db}".format(
            db=mysql_db)
        )
    except sa.exc.OperationalError:
        logger.info('DATABASE {db} DOES NOT EXIST. CREATING...'.format(
            db=mysql_db)
        )
        mysql_pool.execute("CREATE DATABASE {db}".format(db=mysql_db))
        mysql_pool.execute("USE {db}".format(db=mysql_db))

    mysql_pool = sa.create_engine(
        'mysql://{user}:{passwd}@{host}/{db}'.format(
            user=mysql_user,
            passwd=mysql_passwd,
            host=mysql_host,
            db=mysql_db
        ),
        pool_size=10,
        pool_recycle=3600,
    )
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
            #logger.info('duplicate entry in db {0}'.format(batch_object.id))
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
