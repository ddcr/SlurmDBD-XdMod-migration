# coding: utf-8
from sqlalchemy import BigInteger, Column, Float, Index, Integer, LargeBinary, SmallInteger, String, Table, Text, text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class AcctCoordTable(Base):
    __tablename__ = 'acct_coord_table'

    creation_time = Column(Integer, nullable=False)
    mod_time = Column(Integer, nullable=False, server_default=text("'0'"))
    deleted = Column(Integer, server_default=text("'0'"))
    acct = Column(String, primary_key=True, nullable=False)
    user = Column(String, primary_key=True, nullable=False)


class AcctTable(Base):
    __tablename__ = 'acct_table'

    creation_time = Column(Integer, nullable=False)
    mod_time = Column(Integer, nullable=False, server_default=text("'0'"))
    deleted = Column(Integer, server_default=text("'0'"))
    name = Column(String, primary_key=True)
    description = Column(Text, nullable=False)
    organization = Column(Text, nullable=False)


class AssocDayUsageTable(Base):
    __tablename__ = 'assoc_day_usage_table'

    creation_time = Column(Integer, nullable=False)
    mod_time = Column(Integer, nullable=False, server_default=text("'0'"))
    deleted = Column(Integer, server_default=text("'0'"))
    id = Column(Integer, primary_key=True, nullable=False)
    period_start = Column(Integer, primary_key=True, nullable=False)
    alloc_cpu_secs = Column(BigInteger, server_default=text("'0'"))


class AssocHourUsageTable(Base):
    __tablename__ = 'assoc_hour_usage_table'

    creation_time = Column(Integer, nullable=False)
    mod_time = Column(Integer, nullable=False, server_default=text("'0'"))
    deleted = Column(Integer, server_default=text("'0'"))
    id = Column(Integer, primary_key=True, nullable=False)
    period_start = Column(Integer, primary_key=True, nullable=False)
    alloc_cpu_secs = Column(BigInteger, server_default=text("'0'"))


class AssocMonthUsageTable(Base):
    __tablename__ = 'assoc_month_usage_table'

    creation_time = Column(Integer, nullable=False)
    mod_time = Column(Integer, nullable=False, server_default=text("'0'"))
    deleted = Column(Integer, server_default=text("'0'"))
    id = Column(Integer, primary_key=True, nullable=False)
    period_start = Column(Integer, primary_key=True, nullable=False)
    alloc_cpu_secs = Column(BigInteger, server_default=text("'0'"))


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


class ClusterDayUsageTable(Base):
    __tablename__ = 'cluster_day_usage_table'

    creation_time = Column(Integer, nullable=False)
    mod_time = Column(Integer, nullable=False, server_default=text("'0'"))
    deleted = Column(Integer, server_default=text("'0'"))
    cluster = Column(String, primary_key=True, nullable=False)
    period_start = Column(Integer, primary_key=True, nullable=False)
    cpu_count = Column(Integer, server_default=text("'0'"))
    alloc_cpu_secs = Column(BigInteger, server_default=text("'0'"))
    down_cpu_secs = Column(BigInteger, server_default=text("'0'"))
    pdown_cpu_secs = Column(BigInteger, server_default=text("'0'"))
    idle_cpu_secs = Column(BigInteger, server_default=text("'0'"))
    resv_cpu_secs = Column(BigInteger, server_default=text("'0'"))
    over_cpu_secs = Column(BigInteger, server_default=text("'0'"))


class ClusterEventTable(Base):
    __tablename__ = 'cluster_event_table'

    node_name = Column(String, primary_key=True, nullable=False)
    cluster = Column(String, primary_key=True, nullable=False)
    cpu_count = Column(Integer, nullable=False)
    state = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    period_start = Column(Integer, primary_key=True, nullable=False)
    period_end = Column(Integer, nullable=False, server_default=text("'0'"))
    reason = Column(String, nullable=False)
    cluster_nodes = Column(Text, nullable=False)


class ClusterHourUsageTable(Base):
    __tablename__ = 'cluster_hour_usage_table'

    creation_time = Column(Integer, nullable=False)
    mod_time = Column(Integer, nullable=False, server_default=text("'0'"))
    deleted = Column(Integer, server_default=text("'0'"))
    cluster = Column(String, primary_key=True, nullable=False)
    period_start = Column(Integer, primary_key=True, nullable=False)
    cpu_count = Column(Integer, server_default=text("'0'"))
    alloc_cpu_secs = Column(BigInteger, server_default=text("'0'"))
    down_cpu_secs = Column(BigInteger, server_default=text("'0'"))
    pdown_cpu_secs = Column(BigInteger, server_default=text("'0'"))
    idle_cpu_secs = Column(BigInteger, server_default=text("'0'"))
    resv_cpu_secs = Column(BigInteger, server_default=text("'0'"))
    over_cpu_secs = Column(BigInteger, server_default=text("'0'"))


class ClusterMonthUsageTable(Base):
    __tablename__ = 'cluster_month_usage_table'

    creation_time = Column(Integer, nullable=False)
    mod_time = Column(Integer, nullable=False, server_default=text("'0'"))
    deleted = Column(Integer, server_default=text("'0'"))
    cluster = Column(String, primary_key=True, nullable=False)
    period_start = Column(Integer, primary_key=True, nullable=False)
    cpu_count = Column(Integer, server_default=text("'0'"))
    alloc_cpu_secs = Column(BigInteger, server_default=text("'0'"))
    down_cpu_secs = Column(BigInteger, server_default=text("'0'"))
    pdown_cpu_secs = Column(BigInteger, server_default=text("'0'"))
    idle_cpu_secs = Column(BigInteger, server_default=text("'0'"))
    resv_cpu_secs = Column(BigInteger, server_default=text("'0'"))
    over_cpu_secs = Column(BigInteger, server_default=text("'0'"))


class ClusterTable(Base):
    __tablename__ = 'cluster_table'

    creation_time = Column(Integer, nullable=False)
    mod_time = Column(Integer, nullable=False, server_default=text("'0'"))
    deleted = Column(Integer, server_default=text("'0'"))
    name = Column(String, primary_key=True)
    control_host = Column(String, nullable=False)
    control_port = Column(Integer, nullable=False, server_default=text("'0'"))
    rpc_version = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    classification = Column(SmallInteger, server_default=text("'0'"))


class JobTable(Base):
    __tablename__ = 'job_table'
    __table_args__ = (
        Index('jobid', 'jobid', 'associd', 'submit', unique=True),
    )

    id = Column(Integer, primary_key=True)
    deleted = Column(Integer, server_default=text("'0'"))
    jobid = Column(Integer, nullable=False)
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
    end = Column(Integer, nullable=False, server_default=text("'0'"))
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
    kill_requid = Column(SmallInteger, nullable=False, server_default=text("'-1'"))
    qos = Column(SmallInteger, server_default=text("'0'"))
    resvid = Column(Integer, nullable=False)


t_last_ran_table = Table(
    'last_ran_table', metadata,
    Column('hourly_rollup', Integer, nullable=False, server_default=text("'0'")),
    Column('daily_rollup', Integer, nullable=False, server_default=text("'0'")),
    Column('monthly_rollup', Integer, nullable=False, server_default=text("'0'"))
)


class QosTable(Base):
    __tablename__ = 'qos_table'

    creation_time = Column(Integer, nullable=False)
    mod_time = Column(Integer, nullable=False, server_default=text("'0'"))
    deleted = Column(Integer, server_default=text("'0'"))
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text)
    max_jobs_per_user = Column(Integer)
    max_submit_jobs_per_user = Column(Integer)
    max_cpus_per_user = Column(Integer)
    max_nodes_per_user = Column(Integer)
    max_wall_duration_per_user = Column(Integer)
    max_cpu_mins_per_user = Column(BigInteger)
    grp_jobs = Column(Integer)
    grp_submit_jobs = Column(Integer)
    grp_cpus = Column(Integer)
    grp_nodes = Column(Integer)
    grp_wall = Column(Integer)
    grp_cpu_mins = Column(BigInteger)
    job_flags = Column(Text)
    preemptees = Column(Text, nullable=False)
    preemptors = Column(Text, nullable=False)
    priority = Column(Integer, server_default=text("'0'"))
    usage_factor = Column(Float(asdecimal=True), nullable=False, server_default=text("'1'"))


class ResvTable(Base):
    __tablename__ = 'resv_table'

    id = Column(Integer, primary_key=True, nullable=False, server_default=text("'0'"))
    name = Column(Text, nullable=False)
    cluster = Column(Text, primary_key=True, nullable=False)
    deleted = Column(Integer, server_default=text("'0'"))
    cpus = Column(Integer, nullable=False)
    assoclist = Column(Text, nullable=False)
    nodelist = Column(Text, nullable=False)
    node_inx = Column(Text, nullable=False)
    start = Column(Integer, primary_key=True, nullable=False, server_default=text("'0'"))
    end = Column(Integer, nullable=False, server_default=text("'0'"))
    flags = Column(SmallInteger, nullable=False, server_default=text("'0'"))


class StepTable(Base):
    __tablename__ = 'step_table'

    id = Column(Integer, primary_key=True, nullable=False)
    deleted = Column(Integer, server_default=text("'0'"))
    stepid = Column(SmallInteger, primary_key=True, nullable=False)
    start = Column(Integer, nullable=False, server_default=text("'0'"))
    end = Column(Integer, nullable=False, server_default=text("'0'"))
    suspended = Column(Integer, nullable=False, server_default=text("'0'"))
    name = Column(Text, nullable=False)
    nodelist = Column(Text, nullable=False)
    node_inx = Column(Text)
    state = Column(SmallInteger, nullable=False)
    kill_requid = Column(SmallInteger, nullable=False, server_default=text("'-1'"))
    comp_code = Column(Integer, nullable=False, server_default=text("'0'"))
    nodes = Column(Integer, nullable=False)
    cpus = Column(Integer, nullable=False)
    tasks = Column(Integer, nullable=False)
    task_dist = Column(SmallInteger, server_default=text("'0'"))
    user_sec = Column(Integer, nullable=False, server_default=text("'0'"))
    user_usec = Column(Integer, nullable=False, server_default=text("'0'"))
    sys_sec = Column(Integer, nullable=False, server_default=text("'0'"))
    sys_usec = Column(Integer, nullable=False, server_default=text("'0'"))
    max_vsize = Column(BigInteger, nullable=False, server_default=text("'0'"))
    max_vsize_task = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    max_vsize_node = Column(Integer, nullable=False, server_default=text("'0'"))
    ave_vsize = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    max_rss = Column(BigInteger, nullable=False, server_default=text("'0'"))
    max_rss_task = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    max_rss_node = Column(Integer, nullable=False, server_default=text("'0'"))
    ave_rss = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    max_pages = Column(Integer, nullable=False, server_default=text("'0'"))
    max_pages_task = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    max_pages_node = Column(Integer, nullable=False, server_default=text("'0'"))
    ave_pages = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))
    min_cpu = Column(Integer, nullable=False, server_default=text("'0'"))
    min_cpu_task = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    min_cpu_node = Column(Integer, nullable=False, server_default=text("'0'"))
    ave_cpu = Column(Float(asdecimal=True), nullable=False, server_default=text("'0'"))


t_suspend_table = Table(
    'suspend_table', metadata,
    Column('id', Integer, nullable=False),
    Column('associd', Integer, nullable=False),
    Column('start', Integer, nullable=False, server_default=text("'0'")),
    Column('end', Integer, nullable=False, server_default=text("'0'"))
)


class TableDefsTable(Base):
    __tablename__ = 'table_defs_table'

    creation_time = Column(Integer, nullable=False)
    mod_time = Column(Integer, nullable=False, server_default=text("'0'"))
    table_name = Column(Text, primary_key=True)
    definition = Column(Text, nullable=False)


class TxnTable(Base):
    __tablename__ = 'txn_table'

    id = Column(Integer, primary_key=True)
    timestamp = Column(Integer, nullable=False, server_default=text("'0'"))
    action = Column(SmallInteger, nullable=False)
    name = Column(Text, nullable=False)
    actor = Column(String, nullable=False)
    info = Column(LargeBinary)


class UserTable(Base):
    __tablename__ = 'user_table'

    creation_time = Column(Integer, nullable=False)
    mod_time = Column(Integer, nullable=False, server_default=text("'0'"))
    deleted = Column(Integer, server_default=text("'0'"))
    name = Column(String, primary_key=True)
    default_acct = Column(String, nullable=False)
    default_wckey = Column(String, nullable=False)
    admin_level = Column(SmallInteger, nullable=False, server_default=text("'1'"))


class WckeyDayUsageTable(Base):
    __tablename__ = 'wckey_day_usage_table'

    creation_time = Column(Integer, nullable=False)
    mod_time = Column(Integer, nullable=False, server_default=text("'0'"))
    deleted = Column(Integer, server_default=text("'0'"))
    id = Column(Integer, primary_key=True, nullable=False)
    period_start = Column(Integer, primary_key=True, nullable=False)
    alloc_cpu_secs = Column(BigInteger, server_default=text("'0'"))
    resv_cpu_secs = Column(BigInteger, server_default=text("'0'"))
    over_cpu_secs = Column(BigInteger, server_default=text("'0'"))


class WckeyHourUsageTable(Base):
    __tablename__ = 'wckey_hour_usage_table'

    creation_time = Column(Integer, nullable=False)
    mod_time = Column(Integer, nullable=False, server_default=text("'0'"))
    deleted = Column(Integer, server_default=text("'0'"))
    id = Column(Integer, primary_key=True, nullable=False)
    period_start = Column(Integer, primary_key=True, nullable=False)
    alloc_cpu_secs = Column(BigInteger, server_default=text("'0'"))
    resv_cpu_secs = Column(BigInteger, server_default=text("'0'"))
    over_cpu_secs = Column(BigInteger, server_default=text("'0'"))


class WckeyMonthUsageTable(Base):
    __tablename__ = 'wckey_month_usage_table'

    creation_time = Column(Integer, nullable=False)
    mod_time = Column(Integer, nullable=False, server_default=text("'0'"))
    deleted = Column(Integer, server_default=text("'0'"))
    id = Column(Integer, primary_key=True, nullable=False)
    period_start = Column(Integer, primary_key=True, nullable=False)
    alloc_cpu_secs = Column(BigInteger, server_default=text("'0'"))
    resv_cpu_secs = Column(BigInteger, server_default=text("'0'"))
    over_cpu_secs = Column(BigInteger, server_default=text("'0'"))


class WckeyTable(Base):
    __tablename__ = 'wckey_table'
    __table_args__ = (
        Index('name', 'name', 'user', 'cluster', unique=True),
    )

    creation_time = Column(Integer, nullable=False)
    mod_time = Column(Integer, nullable=False, server_default=text("'0'"))
    deleted = Column(Integer, server_default=text("'0'"))
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cluster = Column(String, nullable=False)
    user = Column(String, nullable=False)
