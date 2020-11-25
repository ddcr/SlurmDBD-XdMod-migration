from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Index, Column, Integer, BigInteger,
                        String, Text, Enum, Date, text)
# from sqlalchemy.dialects.mysql import BIGINT, INT, VARCHAR, TEX

Base = declarative_base()


# No need for specific dialect (mysql) types, unless one is creating
# a table (i guess?)
class ShreddedJobSlurm(Base):
    __tablename__ = 'shredded_job_slurm'
    __table_args__ = (
        Index('job', 'cluster_name', 'job_id', 'job_array_index',
              'submit_time', 'end_time', unique=True),
    )

    shredded_job_slurm_id = Column(BigInteger, primary_key=True)
    job_id = Column(Integer, nullable=False)
    job_array_index = Column(Integer, nullable=False,
                             server_default=text("'-1'"))
    job_id_raw = Column(Integer)
    job_name = Column(String, nullable=False)
    cluster_name = Column(String, nullable=False)
    partition_name = Column(String, nullable=False)
    user_name = Column(String, nullable=False)
    uid_number = Column(Integer)
    group_name = Column(String, nullable=False)
    gid_number = Column(Integer)
    account_name = Column(String, nullable=False)
    submit_time = Column(Integer, nullable=False)
    eligible_time = Column(Integer, nullable=False)
    start_time = Column(Integer, nullable=False)
    end_time = Column(Integer, nullable=False)
    elapsed = Column(Integer, nullable=False)
    exit_code = Column(String(32), nullable=False)
    state = Column(String(32))
    nnodes = Column(Integer, nullable=False)
    ncpus = Column(Integer, nullable=False)
    req_cpus = Column(Integer)
    req_mem = Column(String(32))
    timelimit = Column(Integer)
    node_list = Column(Text, nullable=False)

    def __repr__(self):
        line = "<ShreddedJobSlurm("
        line += ', '.join(['{0} = {1}'.format(c.key, getattr(self, c.key)) for
                           c in self.__mapper__.columns])
        line += ")>"
        return(line)


class ShreddedJob(Base):
    __tablename__ = 'shredded_job'
    __table_args__ = (
        Index('end_time', 'end_time', 'resource_name'),
        Index('date_key', 'date_key', 'resource_name'),
        Index('source', 'source_format', 'resource_name'),
        Index('pi_name', 'pi_name', 'resource_name'),
        Index('user_name', 'user_name', 'resource_name', 'pi_name')
    )

    shredded_job_id = Column(BigInteger, primary_key=True)
    source_format = Column(Enum(u'pbs', u'sge', u'slurm', u'lsf'),
                           nullable=False)
    date_key = Column(Date, nullable=False)
    job_id = Column(Integer, nullable=False)
    job_array_index = Column(Integer)
    job_id_raw = Column(Integer)
    job_name = Column(String(255))
    resource_name = Column(String(255), nullable=False, index=True)
    queue_name = Column(String(255), nullable=False)
    user_name = Column(String(255), nullable=False)
    uid_number = Column(Integer)
    group_name = Column(String(255), nullable=False,
                        server_default=text("'Unknown'"))
    gid_number = Column(Integer)
    account_name = Column(String(255), nullable=False,
                          server_default=text("'Unknown'"))
    project_name = Column(String(255), nullable=False,
                          server_default=text("'Unknown'"))
    pi_name = Column(String(255), nullable=False,
                     server_default=text("'Unknown'"))
    start_time = Column(Integer, nullable=False)
    end_time = Column(Integer, nullable=False)
    submission_time = Column(Integer, nullable=False)
    eligible_time = Column(Integer)
    wall_time = Column(BigInteger, nullable=False)
    wait_time = Column(BigInteger, nullable=False)
    exit_code = Column(String(32))
    exit_state = Column(String(32))
    node_count = Column(Integer, nullable=False)
    cpu_count = Column(Integer, nullable=False)
    cpu_req = Column(Integer)
    mem_req = Column(String(32))
    timelimit = Column(Integer)
    node_list = Column(Text)

    def __repr__(self):
        line = "<ShreddedJob("
        line += ', '.join(['{0} = {1}'.format(c.key, getattr(self, c.key)) for
                           c in self.__mapper__.columns])
        line += ")>"
        return(line)
