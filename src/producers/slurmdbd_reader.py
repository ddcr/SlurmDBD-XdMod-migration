# -*- coding: utf-8 -*-
# @Author: ddcr
# @Date:   2016-08-30 20:06:12
# @Last Modified by:   ddcr
# @Last Modified time: 2016-09-09 22:54:05
import logging
import sqlalchemy as sa
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker, synonym, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Index, Column, Integer, SmallInteger,
                        BigInteger, LargeBinary, String, Text, text)
from sqlalchemy.ext.hybrid import hybrid_property
import settings
import time
import datetime

__all__ = ["JobTable", "AssocTable", "UserTable",
           "AcctTable", "ReadSlurmDBD"]

logger = logging.getLogger('read_slurm_acct_db')

Base = declarative_base()
metadata = Base.metadata

try:
    # configure Session class with desired options
    Session = sessionmaker()
    # later, we create the engine
    engine = sa.create_engine(URL(**settings.SLURMDBD), echo=False)
    # associate it with our custom Session class
    Session.configure(bind=engine, autocommit=False, autoflush=False)
    metadata.create_all(engine)
    # work with the session
    SlurmDBSession = Session()
except:
    logging.error("[SQLAlachemy Server] session error")
    raise


class JobTable(Base):
    __tablename__ = 'job_table'
    __table_args__ = (
        Index('jobid', 'jobid', 'associd', 'submit', unique=True),
    )

    id = Column(Integer, primary_key=True)
    deleted = Column(Integer, server_default=text("'0'"))
    jobid = Column(Integer, nullable=False)
    jobidraw = synonym("jobid")
    associd = Column(Integer, nullable=False)
    wckey = Column(String, nullable=False)
    wckeyid = Column(Integer, nullable=False)
    uid = Column(SmallInteger, nullable=False)
    gid = Column(SmallInteger, nullable=False)
    cluster = Column(String, nullable=False)
    partition = Column(String, nullable=False)
    blockid = Column(String)
    account = Column(String)
    eligible = Column(Integer, nullable=False, server_default=text("'0'"))
    submit = Column(Integer, nullable=False, server_default=text("'0'"))
    start = Column(Integer, nullable=False, server_default=text("'0'"))
    end = Column(end, Integer, nullable=False, server_default=text("'0'"))
    suspended = Column(Integer, nullable=False, server_default=text("'0'"))
    timelimit = Column(Integer, nullable=False, server_default=text("'0'"))
    name = Column(String, nullable=False)
    track_steps = Column(Integer, nullable=False)
    state = Column(SmallInteger, nullable=False)
    comp_code = Column(Integer, nullable=False, server_default=text("'0'"))
    priority = Column(Integer, nullable=False)
    req_cpus = Column(Integer, nullable=False)
    alloc_cpus = Column(Integer, nullable=False)
    alloc_nodes = Column(Integer, nullable=False)
    nodelist = Column(Text)
    node_inx = Column(Text)
    kill_requid = Column(SmallInteger, nullable=False,
                         server_default=text("'-1'"))
    # requested job memory is not accounted in slurm v2.0.5
    # mem_req = column_property()
    qos = Column(SmallInteger, server_default=text("'0'"))
    resvid = Column(Integer, nullable=False)

    @hybrid_property
    def eligible_datetime(self):
        return datetime.datetime.fromtimestamp(float(self.eligible))

    @eligible_datetime.setter
    def eligible_datetime(self, value):
        self.eligible = int(time.mktime(value.timetuple()))

    @hybrid_property
    def submit_datetime(self):
        return datetime.datetime.fromtimestamp(float(self.submit))

    @submit_datetime.setter
    def submit_datetime(self, value):
        self.submit_time = int(time.mktime(value.timetuple()))

    @hybrid_property
    def start_datetime(self):
        return datetime.datetime.fromtimestamp(float(self.start))

    @start_datetime.setter
    def start_datetime(self, value):
        self.start = int(time.mktime(value.timetuple()))

    @hybrid_property
    def end_datetime(self):
        return datetime.datetime.fromtimestamp(float(self.end))

    @end_datetime.setter
    def end_datetime(self, value):
        self.end = int(time.mktime(value.timetuple()))

    def __repr__(self):
        line = "<JobTable("
        line += ', '.join(['{0} = {1}'.format(c.key, getattr(self, c.key)) for
                           c in self.__mapper__.columns])
        line += ")>"
        return(line)


class AssocTable(Base):
    __tablename__ = 'assoc_table'
    __table_args__ = (
        Index('user', 'user', 'acct', 'cluster', 'partition', unique=True),
    )

    creation_time = Column(Integer, nullable=False)
    mod_time = Column(Integer, nullable=False, server_default=text("'0'"))
    deleted = Column(Integer, server_default=text("'0'"))
    id = Column(Integer, primary_key=True)
    user = Column(String, nullable=False)
    acct = Column(String, nullable=False)
    cluster = Column(String, nullable=False)
    partition = Column(String, nullable=False)
    parent_acct = Column(String, nullable=False)
    lft = Column(Integer, nullable=False)
    rgt = Column(Integer, nullable=False)
    fairshare = Column(Integer, nullable=False, server_default=text("'1'"))
    max_jobs = Column(Integer)
    max_submit_jobs = Column(Integer)
    max_cpus_per_job = Column(Integer)
    max_nodes_per_job = Column(Integer)
    max_wall_duration_per_job = Column(Integer)
    max_cpu_mins_per_job = Column(BigInteger)
    grp_jobs = Column(Integer)
    grp_submit_jobs = Column(Integer)
    grp_cpus = Column(Integer)
    grp_nodes = Column(Integer)
    grp_wall = Column(Integer)
    grp_cpu_mins = Column(BigInteger)
    qos = Column(LargeBinary, nullable=False)
    delta_qos = Column(LargeBinary, nullable=False)

    @hybrid_property
    def creation_datetime(self):
        return datetime.datetime.fromtimestamp(float(self.creation_time))

    @hybrid_property
    def mod_datetime(self):
        return datetime.datetime.fromtimestamp(float(self.mod_time))


class UserTable(Base):
    __tablename__ = 'user_table'

    creation_time = Column(Integer, nullable=False)
    mod_time = Column(Integer, nullable=False, server_default=text("'0'"))
    deleted = Column(Integer, server_default=text("'0'"))
    name = Column(String, primary_key=True)
    default_acct = Column(String, nullable=False)
    default_wckey = Column(String, nullable=False)
    admin_level = Column(SmallInteger, nullable=False,
                         server_default=text("'1'"))

    @hybrid_property
    def creation_datetime(self):
        return datetime.datetime.fromtimestamp(float(self.creation_time))

    @creation_datetime.setter
    def creation_datetime(self, value):
        self.creation_time = time.mktime(value.timetuple())

    @hybrid_property
    def mod_datetime(self):
        return datetime.datetime.fromtimestamp(float(self.mod_time))


class AcctTable(Base):
    __tablename__ = 'acct_table'

    creation_time = Column(Integer, nullable=False)
    mod_time = Column(Integer, nullable=False, server_default=text("'0'"))
    deleted = Column(Integer, server_default=text("'0'"))
    name = Column(String, primary_key=True)
    description = Column(Text, nullable=False)
    organization = Column(Text, nullable=False)
    users = relationship("UserTable",
                         primaryjoin="AcctTable.name == AssocTable.acct",
                         secondaryjoin="AssocTable.user == UserTable.name",
                         secondary=AssocTable.__table__,
                         backref='all_accts')

    @hybrid_property
    def creation_datetime(self):
        return datetime.datetime.fromtimestamp(float(self.creation_time))

    @creation_datetime.setter
    def creation_datetime(self, value):
        self.creation_time = time.mktime(value.timetuple())

    def __repr__(self):
        line = "<AcctTable("
        line += ', '.join(['{0} = {1}'.format(c.key, getattr(self, c.key)) for
                           c in self.__mapper__.columns])
        line += ")>"
        return(line)


class ReadSlurmDBD(object):
    pass
    # def __init__(self):


if __name__ == '__main__':
    pass
