# -*- coding: utf-8 -*-
# @Author: ddcr
# @Date:   2016-09-03 20:51:58
# @Last Modified by:   ddcr
# @Last Modified time: 2016-09-12 19:33:08
import datetime
import sqlalchemy as sa
from src.producers.slurmdbd_reader import SlurmDBSession
from src.producers.slurmdbd_reader import (UserTable, AcctTable,
                                           JobTable, AssocTable)


def test1():
    """Using a Hybrid
    """
    for obj in SlurmDBSession.query(UserTable):
        print obj.creation_time, obj.creation_datetime
        obj.creation_datetime = datetime.datetime.now()
        print obj.creation_time, obj.creation_datetime,
        int(obj.creation_time)
        print('='*70)


def test2():
    """Runtime information about
    sqlalchemy ORM objects
    """
    from sqlalchemy import inspect

    insp = inspect(AcctTable)
    print list(insp.columns)
    print insp.all_orm_descriptors.keys()
    print [c_attr.key for c_attr in insp.mapper.column_attrs]


def test3():
    """Print mysql expressions
    """
    from sqlalchemy.dialects import mysql

    q = SlurmDBSession.query(AcctTable).order_by(AcctTable.creation_time)
    print str(q.statement.compile(dialect=mysql.dialect()))


def test4():
    """Test relationship in AcctTable. We list all users of given account/group
    """
    for row in SlurmDBSession.query(AcctTable).\
            filter(sa.and_(AcctTable.deleted == 0,
                           AcctTable.organization == 'qui')):
        account_users = row.users
        print row.creation_datetime, row.name,
        [c.name for c in account_users]

    for row in SlurmDBSession.query(UserTable).\
            filter(UserTable.deleted == 0):
            user_accounts = row.all_accts
            print row.name, row.default_acct,
            [c.name for c in user_accounts]


def test5():
    for row in SlurmDBSession.query(AcctTable).\
            filter(sa.and_(AcctTable.deleted == 0,
                           AcctTable.organization == 'qui')):
        print repr(row)


def test6():
    """These query examples are for slurm-2.0.5.
    In version 2.1.16 (the last of the series 2.1.x) one more
    job field in the query was added: t1.timelimit

    select <JOB_FIELDS> from job_table as t1
    left join assoc_table as t2 on t1.associd=t2.id

    (a) WITH usage_start; NO usage_end
    where(t1.end >= USAGE_START || t1.end = 0)

    (b) WITH usage_start; WITH usage_end
    where((t1.eligible < USAGE_END &&
          (t1.end >= USAGE_START || t1.end = 0)))

    (c) NO usage_start; WITH usage_end
    where((t1.eligible < USAGE_END))

    && (t1.state='STATE_1' || t1.state='STATE_2' || ...)
    && ((t1.cluster='veredas' || t2.cluster='veredas'))
    order by order by t1.cluster, jobid, submit desc
    """
    from sqlalchemy.sql import select, text, desc

    job_table = JobTable().__table__
    assoc_table = AssocTable.__table__

    s = select([job_table.alias('t1'), assoc_table.alias('t2')])
    print(s)
    print('-'*80)

    stmt = text(
        "SELECT  t1.id, t1.jobid, t1.associd, t1.wckey, "
        "t1.wckeyid, t1.uid, t1.gid, t1.resvid, "
        "t1.partition, t1.blockid, t1.cluster, "
        "t1.account, t1.eligible, t1.submit, t1.start, "
        "t1.end, t1.suspended, t1.name, t1.track_steps, "
        "t1.state, t1.comp_code, t1.priority, t1.req_cpus, "
        "t1.alloc_cpus, t1.alloc_nodes, t1.nodelist, "
        "t1.node_inx, t1.kill_requid, t1.qos, "
        "t2.user, t2.cluster, t2.acct, t2.lft "
        "FROM job_table AS t1 LEFT JOIN assoc_table AS t2 "
        "ON t1.associd = t2.id "
        "WHERE (t1.state = '3' || t1.state = '4' || "
        "t1.state = '5' || t1.state = '6' || t1.state = '7') && "
        "((t1.cluster = 'veredas' || t2.cluster = 'veredas')) "
        "order by t1.cluster, jobid, submit desc")

    print stmt
    print('-'*80)

    t1 = job_table.alias('t1')
    t2 = assoc_table.alias('t2')
    cols = [t1.c.id, t1.c.jobid, t1.c.associd, t1.c.wckey,
            t1.c.wckeyid, t1.c.uid, t1.c.gid, t1.c.resvid,
            t1.c.partition, t1.c.blockid, t1.c.cluster,
            t1.c.account, t1.c.eligible, t1.c.submit, t1.c.start,
            t1.c.end, t1.c.suspended, t1.c.name, t1.c.track_steps,
            t1.c.state, t1.c.comp_code, t1.c.priority, t1.c.req_cpus,
            t1.c.alloc_cpus, t1.c.alloc_nodes, t1.c.nodelist,
            t1.c.node_inx, t1.c.kill_requid, t1.c.qos,
            t2.c.user, t2.c.cluster, t2.c.acct, t2.c.lft]

    # since I am only concerned with a unique cluster, I do not
    # need to order rows by cluster name
    q = select(cols).\
        select_from(t1.outerjoin(t2, t1.c.associd == t2.c.id)).\
        where(((t1.c.state == '3') | (t1.c.state == '4') |
               (t1.c.state == '5') | (t1.c.state == '6') |
               (t1.c.state == '7')) &
              ((t1.c.cluster == 'veredas') | (t2.c.cluster == 'veredas'))).\
        order_by(desc("t1.jobid, t1.submit")).limit(10)
    print(q)
    print('-'*80)

    # ResultProxy obj.
    # result = conn.execute(s)


def test7():
    from sqlalchemy.sql import select, text, desc
    from sqlalchemy.orm import aliased

    t1 = aliased(JobTable, name='t1')
    t2 = aliased(AssocTable, name='t2')

    t = SlurmDBSession.query(t1.id, t1.jobid, t1.associd, t1.wckey,
                             t1.wckeyid, t1.uid, t1.gid, t1.resvid,
                             t1.partition, t1.blockid, t1.cluster,
                             t1.account, t1.eligible, t1.submit, t1.start,
                             t1.end, t1.suspended, t1.name, t1.track_steps,
                             t1.state, t1.comp_code, t1.priority, t1.req_cpus,
                             t1.alloc_cpus, t1.alloc_nodes, t1.nodelist,
                             t1.node_inx, t1.kill_requid, t1.qos,
                             t2.user, t2.cluster, t2.acct, t2.lft).\
        outerjoin(AssocTable, t1.associd == AssocTable.id)
    print('\n {}'.format(t))


def test8():
    """These query tests refer to changes made in slurm-2.2.0.
    From this version on, we have one job database for each cluster:
    <cluster_name>_<table>, and so each job database is consulted
    separately if a list of clusters is given in sacct.

    The columns of the database have also changed:
    Changed:
    t1.cpus_alloc     <-- t1.alloc_cpus
    t1.cpus_req       <-- t1.req_cpus
    t1.exit_code      <-- t1.comp_code (?)
    t1.id_assoc       <-- t1.associd
    t1.id_block       <-- t1.blockid
    t1.id_group       <-- t1.gid
    t1.id_job         <-- t1.jobid
    t1.id_qos         <-- t1.qos
    t1.id_resv        <-- t1.resvid
    t1.id_user        <-- t1.uid
    t1.id_wckey       <-- t1.wckeyid
    t1.job_db_inx     <-- t1.id
    t1.job_name       <-- t1.name
    t1.nodes_alloc    <-- t1.alloc_nodes
    t1.time_eligible  <-- t1.eligible
    t1.time_end       <-- t1.end
    t1.time_start     <-- t1.start
    t1.time_submit    <-- t1.submit
    t1.time_suspended <-- t1.suspended

    Added:
    t1.derived_ec
    t1.derived_es
    t1.timelimit

    """
    from sqlalchemy.sql import select, desc

    job_table = JobTable().__table__
    assoc_table = AssocTable.__table__

    t1 = job_table.alias('t1')
    t2 = assoc_table.alias('t2')
    cols = [t1.c.id, t1.c.jobid, t1.c.associd, t1.c.wckey,
            t1.c.wckeyid, t1.c.uid, t1.c.gid, t1.c.resvid,
            t1.c.partition, t1.c.blockid, t1.c.cluster,
            t1.c.account, t1.c.eligible, t1.c.submit, t1.c.start,
            t1.c.end, t1.c.suspended, t1.c.name, t1.c.track_steps,
            t1.c.state, t1.c.comp_code, t1.c.priority, t1.c.req_cpus,
            t1.c.alloc_cpus, t1.c.alloc_nodes, t1.c.nodelist,
            t1.c.node_inx, t1.c.kill_requid, t1.c.qos,
            t2.c.user, t2.c.cluster, t2.c.acct, t2.c.lft]

    # since I am only concerned with a unique cluster, I do not
    # need to order rows by cluster name
    q = select(cols).\
        select_from(t1.outerjoin(t2, t1.c.associd == t2.c.id)).\
        where(((t1.c.state == '3') | (t1.c.state == '4') |
               (t1.c.state == '5') | (t1.c.state == '6') |
               (t1.c.state == '7')) &
              ((t1.c.cluster == 'veredas') | (t2.c.cluster == 'veredas'))).\
        order_by(desc("t1.cluster, jobid, submit")).\
        limit(1000)

    print(q)


def test8():
    """This call is for the latest git version of slurm

    select <job_fields> from <cluster>_job_table as t1
        left join <cluster>_assoc_table as t2
            on t1.id_assoc=t2.id_assoc
        left join <cluster>_resv_table as t3
            on t1.id_resv=t3.id_resv &&
    ((t1.time_start && (t3.time_start < t1.time_start &&
                       (t3.time_end >= t1.time_start || t3.time_end = 0))) ||
    ((t3.time_start < t1.time_submit &&
     (t3.time_end >= t1.time_submit || t3.time_end = 0)) ||
     (t3.time_start > t1.time_submit)))

    (a) NO usage_start; NO usage_end
        where(
        (t1.state='STATE_1' || t1.state='STATE_2' || ...)
        )

    (b) WITH usage_start; NO usage_end
        where(
        (t1.state='STATE_1' &&
            (t1.time_end && (t1.time_end >= USAGE_START))) ||
        (t1.state='STATE_2' &&
            (t1.time_end && (t1.time_end >= USAGE_START))) || ...
        )

    (c) WITH usage_start; WITH usage_end
        where(
        (t1.state='STATE_1' &&
            (t1.time_end &&
             (t1.time_end between USAGE_START and USAGE_END))) ||
        (t1.state='STATE_2' &&
            (t1.time_end &&
             (t1.time_end between USAGE_START and USAGE_END))) || ...
        )

    (d) NO usage_start; WITH usage_end
        where(
        (t1.state='STATE_1' &&
            (t1.time_end && (t1.time_end <= USAGE_END))) ||
        (t1.state='STATE_2' &&
            (t1.time_end && (t1.time_end <= USAGE_END))) || ...
        )


    group by id_job, time_submit desc
    """
