# coding: utf-8
from sqlalchemy import BigInteger, Column, Date, DateTime, Enum, Index, Integer, Numeric, String, Text, text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class SchemaVersionHistory(Base):
    __tablename__ = 'schema_version_history'

    database_name = Column(String(64), primary_key=True, nullable=False)
    schema_version = Column(String(64), primary_key=True, nullable=False)
    action_datetime = Column(DateTime, primary_key=True, nullable=False)
    action_type = Column(Enum(u'created', u'upgraded'), nullable=False)
    script_name = Column(String(255), nullable=False)


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
    source_format = Column(Enum(u'pbs', u'sge', u'slurm', u'lsf'), nullable=False)
    date_key = Column(Date, nullable=False)
    job_id = Column(Integer, nullable=False)
    job_array_index = Column(Integer)
    job_id_raw = Column(Integer)
    job_name = Column(String(255))
    resource_name = Column(String(255), nullable=False, index=True)
    queue_name = Column(String(255), nullable=False)
    user_name = Column(String(255), nullable=False)
    uid_number = Column(Integer)
    group_name = Column(String(255), nullable=False, server_default=text("'Unknown'"))
    gid_number = Column(Integer)
    account_name = Column(String(255), nullable=False, server_default=text("'Unknown'"))
    project_name = Column(String(255), nullable=False, server_default=text("'Unknown'"))
    pi_name = Column(String(255), nullable=False, server_default=text("'Unknown'"))
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


class ShreddedJobLsf(Base):
    __tablename__ = 'shredded_job_lsf'
    __table_args__ = (
        Index('job', 'resource_name', 'job_id', 'idx', 'submit_time', 'event_time', unique=True),
    )

    shredded_job_lsf_id = Column(BigInteger, primary_key=True)
    job_id = Column(Integer, nullable=False)
    idx = Column(Integer, nullable=False)
    job_name = Column(String(255), nullable=False, server_default=text("''"))
    resource_name = Column(String(255), nullable=False)
    queue = Column(String(255), nullable=False)
    user_name = Column(String(255), nullable=False)
    project_name = Column(String(255), nullable=False, server_default=text("''"))
    submit_time = Column(Integer, nullable=False)
    start_time = Column(Integer, nullable=False)
    event_time = Column(Integer, nullable=False)
    num_processors = Column(Integer, nullable=False)
    num_ex_hosts = Column(Integer, nullable=False)


class ShreddedJobPb(Base):
    __tablename__ = 'shredded_job_pbs'
    __table_args__ = (
        Index('job', 'host', 'job_id', 'job_array_index', 'ctime', 'end', unique=True),
    )

    shredded_job_pbs_id = Column(BigInteger, primary_key=True)
    job_id = Column(Integer, nullable=False)
    job_array_index = Column(Integer, nullable=False, server_default=text("'-1'"))
    host = Column(String(255), nullable=False)
    queue = Column(String(255), nullable=False)
    user = Column(String(255), nullable=False)
    groupname = Column(String(255), nullable=False)
    ctime = Column(Integer, nullable=False)
    qtime = Column(Integer, nullable=False)
    start = Column(Integer, nullable=False)
    end = Column(Integer, nullable=False)
    etime = Column(Integer, nullable=False)
    exit_status = Column(Integer)
    session = Column(Integer)
    requestor = Column(String(255))
    jobname = Column(String(255))
    owner = Column(String(255))
    account = Column(String(255))
    session_id = Column(Integer)
    error_path = Column(String(255))
    output_path = Column(String(255))
    exec_host = Column(Text)
    resources_used_vmem = Column(BigInteger)
    resources_used_mem = Column(BigInteger)
    resources_used_walltime = Column(BigInteger)
    resources_used_nodes = Column(Integer)
    resources_used_cpus = Column(Integer)
    resources_used_cput = Column(BigInteger)
    resource_list_nodes = Column(Text)
    resource_list_procs = Column(Text)
    resource_list_neednodes = Column(Text)
    resource_list_pcput = Column(BigInteger)
    resource_list_cput = Column(BigInteger)
    resource_list_walltime = Column(BigInteger)
    resource_list_ncpus = Column(Integer)
    resource_list_nodect = Column(Integer)
    resource_list_mem = Column(BigInteger)
    resource_list_pmem = Column(BigInteger)
    node_list = Column(Text, nullable=False)


class ShreddedJobSge(Base):
    __tablename__ = 'shredded_job_sge'
    __table_args__ = (
        Index('job', 'hostname', 'job_number', 'task_number', 'failed', unique=True),
    )

    shredded_job_sge_id = Column(BigInteger, primary_key=True)
    clustername = Column(String(255))
    qname = Column(String(255))
    hostname = Column(String(255), nullable=False)
    groupname = Column(String(255))
    owner = Column(String(255))
    job_name = Column(String(255))
    job_number = Column(Integer, nullable=False)
    account = Column(String(255))
    priority = Column(Integer)
    submission_time = Column(Integer)
    start_time = Column(Integer)
    end_time = Column(Integer)
    failed = Column(Integer)
    exit_status = Column(Integer)
    ru_wallclock = Column(Integer)
    ru_utime = Column(Numeric(32, 6))
    ru_stime = Column(Numeric(32, 6))
    ru_maxrss = Column(Integer)
    ru_ixrss = Column(Integer)
    ru_ismrss = Column(Integer)
    ru_idrss = Column(Integer)
    ru_isrss = Column(Integer)
    ru_minflt = Column(Integer)
    ru_majflt = Column(Integer)
    ru_nswap = Column(Integer)
    ru_inblock = Column(Integer)
    ru_oublock = Column(Integer)
    ru_msgsnd = Column(Integer)
    ru_msgrcv = Column(Integer)
    ru_nsignals = Column(Integer)
    ru_nvcsw = Column(Integer)
    ru_nivcsw = Column(Integer)
    project = Column(String(255))
    department = Column(String(255))
    granted_pe = Column(String(255))
    slots = Column(Integer)
    task_number = Column(Integer)
    cpu = Column(Numeric(32, 6))
    mem = Column(Numeric(32, 6))
    io = Column(Numeric(32, 6))
    category = Column(Text)
    iow = Column(Numeric(32, 6))
    pe_taskid = Column(Integer)
    maxvmem = Column(BigInteger)
    arid = Column(Integer)
    ar_submission_time = Column(Integer)
    resource_list_arch = Column(String(255))
    resource_list_qname = Column(String(255))
    resource_list_hostname = Column(String(255))
    resource_list_notify = Column(Integer)
    resource_list_calendar = Column(String(255))
    resource_list_min_cpu_interval = Column(Integer)
    resource_list_tmpdir = Column(String(255))
    resource_list_seq_no = Column(Integer)
    resource_list_s_rt = Column(BigInteger)
    resource_list_h_rt = Column(BigInteger)
    resource_list_s_cpu = Column(BigInteger)
    resource_list_h_cpu = Column(BigInteger)
    resource_list_s_data = Column(BigInteger)
    resource_list_h_data = Column(BigInteger)
    resource_list_s_stack = Column(BigInteger)
    resource_list_h_stack = Column(BigInteger)
    resource_list_s_core = Column(BigInteger)
    resource_list_h_core = Column(BigInteger)
    resource_list_s_rss = Column(BigInteger)
    resource_list_h_rss = Column(BigInteger)
    resource_list_slots = Column(String(255))
    resource_list_s_vmem = Column(BigInteger)
    resource_list_h_vmem = Column(BigInteger)
    resource_list_s_fsize = Column(BigInteger)
    resource_list_h_fsize = Column(BigInteger)
    resource_list_num_proc = Column(Integer)
    resource_list_mem_free = Column(BigInteger)


class ShreddedJobSlurm(Base):
    __tablename__ = 'shredded_job_slurm'
    __table_args__ = (
        Index('job', 'cluster_name', 'job_id', 'job_array_index', 'submit_time', 'end_time', unique=True),
    )

    shredded_job_slurm_id = Column(BigInteger, primary_key=True)
    job_id = Column(Integer, nullable=False)
    job_array_index = Column(Integer, nullable=False, server_default=text("'-1'"))
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


class StagingJob(Base):
    __tablename__ = 'staging_job'

    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, nullable=False)
    job_array_index = Column(Integer)
    job_id_raw = Column(Integer)
    job_name = Column(String(255))
    resource_name = Column(String(255), nullable=False)
    queue_name = Column(String(255), nullable=False)
    user_name = Column(String(255), nullable=False)
    uid_number = Column(Integer)
    group_name = Column(String(255), nullable=False)
    gid_number = Column(Integer)
    account_name = Column(String(255))
    project_name = Column(String(255))
    pi_name = Column(String(255), nullable=False)
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


class StagingPi(Base):
    __tablename__ = 'staging_pi'

    pi_id = Column(Integer, primary_key=True)
    pi_name = Column(String(255), nullable=False, unique=True)


class StagingPiResource(Base):
    __tablename__ = 'staging_pi_resource'
    __table_args__ = (
        Index('pi_resource_name', 'pi_name', 'resource_name', unique=True),
    )

    pi_resource_id = Column(Integer, primary_key=True)
    pi_name = Column(String(255), nullable=False, index=True)
    resource_name = Column(String(255), nullable=False, index=True)


class StagingResource(Base):
    __tablename__ = 'staging_resource'

    resource_id = Column(Integer, primary_key=True)
    resource_name = Column(String(255), nullable=False, unique=True)


class StagingUnionUserPi(Base):
    __tablename__ = 'staging_union_user_pi'

    union_user_pi_id = Column(Integer, primary_key=True)
    union_user_pi_name = Column(String(255), nullable=False, unique=True)


class StagingUnionUserPiResource(Base):
    __tablename__ = 'staging_union_user_pi_resource'
    __table_args__ = (
        Index('union_user_pi_resource_name', 'union_user_pi_name', 'resource_name', unique=True),
    )

    union_user_pi_resource_id = Column(Integer, primary_key=True)
    union_user_pi_name = Column(String(255), nullable=False, index=True)
    resource_name = Column(String(255), nullable=False, index=True)


class StagingUserPiResource(Base):
    __tablename__ = 'staging_user_pi_resource'
    __table_args__ = (
        Index('user_pi_resource', 'user_name', 'pi_name', 'resource_name', unique=True),
    )

    user_pi_resource_id = Column(Integer, primary_key=True)
    user_name = Column(String(255), nullable=False, index=True)
    pi_name = Column(String(255), nullable=False, index=True)
    resource_name = Column(String(255), nullable=False, index=True)
