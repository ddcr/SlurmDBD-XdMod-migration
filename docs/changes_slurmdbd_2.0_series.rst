* Changes in SLURM 2.2.7
========================
 -- Fixed issue with accounting when asking for jobs with a hostlist.

* Changes in SLURM 2.2.6
========================
 -- When enforcing accounting, fix polling for unknown uids for users after
    the slurmctld started.  Previously one would have to issue a reconfigure
    to the slurmctld to have it look for new uids.
 -- Fixed issue in accounting where it was possible for a new
    association/wckey to be set incorrectly as a default the new object
    was added after an original default object already existed.  Before
    the slurmctld would need to be restarted to fix the issue.

* Changes in SLURM 2.2.4
========================
 -- In accounting_storage/filetxt plugin, substitute spaces within job names,
    step names, and account names with an underscore to insure proper parsing.
 -- Improve handling of job updates when using limits in accounting, and
    updating jobs as a non-admin user.

* Changes in SLURM 2.2.3
========================
 -- Fix for handling job names with a "'" in the name within MySQL accounting.
    Patch from Gerrit Renker, CSCS.

* Changes in SLURM 2.2.2
========================
 -- Report the StartTime of a job as "Unknown" rather than the year 2106 if its
    expected start time was too far in the future for the backfill scheduler
    to compute.
 -- Fix for accounting_storage/mysql plugin to correctly query cluster based
    transactions.
 -- Fix issue when updating database for clusters that were previously deleted
    before upgrade to 2.2 database.

* Changes in SLURM 2.2.1
========================
 -- Fix setting derived exit code correctly for jobs that happen to have the
    same jobid.
 -- Better checking for time overflow when rolling up in accounting.

* Changes in SLURM 2.2.0
========================
 -- Fix for sacct --state to work correctly when not specifying a start time.

* Changes in SLURM 2.2.0.rc1
============================
 -- Mysql plugin works correctly without the SlurmDBD
 -- Added the derived exit code to the slurmctld job record and the derived
    exit code and string to the job record in the SLURM db.
 -- Added ability to use sstat/sacct against the batch step.
 -- Added ability to enforce new limits given to associations/qos on
    pending jobs.
 -- Increase max message size for the slurmdbd from 1000000 to 16*1024*1024
 -- Increase number of active threads in the slurmdbd from 50 to 100
 -- Fixed small bug in src/common/slurmdb_defs.c reported by Bjorn-Helge Mevik
 -- Fixed bug in selecting jobs based on sacct -N option
 -- Fixed issue where node index wasn't stored correcting when using DBD.
 -- Patch to improve threadsafeness in the mysql plugins.

* Changes in SLURM 2.2.0.pre12
==============================
 -- Fix bug that can result in duplicate job termination records in accounting
    for job termination when slurmctld restarts or reconfigures.
 -- Added the derived_ec (exit_code) member to job_info_t.  exit_code captures
    the exit code of the job script (or salloc) while derived_ec contains the
    highest exit code of all the job steps.
 -- Added SLURM_JOB_EXIT_CODE and SLURM_JOB_DERIVED_EC variables to the
    EpilogSlurmctld environment
 -- More work done on the accounting_storage/pgsql plugin, still beta.
    Patch from Hongjia Cao (NUDT).
 -- Add locks around the MySQL calls for proper operation if the non-thread
    safe version of the MySQL library is used.

* Changes in SLURM 2.2.0.pre11
==============================
 -- Add support for serveral new trigger types: SlurmDBD failure/restart,
    Database failure/restart, Slurmctld failure/restart.

* Changes in SLURM 2.2.0.pre10
==============================
 -- Various Patchs from Hongjia Cao dealing with bugs found in sacctmgr and
    the slurmdbd.

* Changes in SLURM 2.2.0.pre9
=============================
 -- Change slurmdb_coord_table back to acct_coord_table to keep consistant
    with < 2.1.
 -- Added ability to change a users name in accounting.
 -- Added a grouping=individual for sreport size reports.
 -- Fix bug in sacct processing of --fields= option.

* Changes in SLURM 2.2.0.pre8
=============================
 -- Remove AccountingStoragePass and JobCompPass from configuration RPC and
    scontrol show config command output. The use of SlurmDBD is still strongly
    recommended as SLURM will have limited database functionality or protection
    otherwise.
 -- Added keeping track of the qos a job is running with in accounting.
 -- Added ability for sacct to query jobs by qos and a range of timelimits.

* Changes in SLURM 2.2.0.pre6
=============================
 -- When using the SlurmDBD messages waiting to be sent will be combined
    and sent in one message.
 -- Accounting - When removing associations if jobs are running, those jobs
    must be killed before proceeding.  Before the jobs were killed
    automatically thus causing user confusion on what is most likely an
    admin's mistake.

* Changes in SLURM 2.2.0.pre5
=============================
 -- Add node state flag of JOB_RESIZING. This will only exist when a job's
    accounting record is being written immediately before or after it changes
    size. This permits job accounting records to be written for a job at each
    size.
 -- Make calls to jobcomp and accounting_storage plugins before and after a job
    changes size (with the job state being JOB_RESIZING). All plugins write a
    record for the job at each size with intermediate job states being
    JOB_RESIZING.
 -- Added to contribs foundation for Perl extension for slurmdb library.
 -- Better postgres support for accounting, still beta.
 -- Speed up job start when using the slurmdbd.

* Changes in SLURM 2.2.0.pre3
=============================
 -- Added slurmdb api for accessing slurm DB information.

* Changes in SLURM 2.2.0.pre2
=============================
 -- Massive change to the schema in the storage_accounting/mysql plugin.  When
    starting the slurmdbd the process of conversion may take a few minutes.
    You might also see some errors such as 'error: mysql_query failed: 1206
    The total number of locks exceeds the lock table size'.  If you get this,
    do not worry, it is because your setting of innodb_buffer_pool_size in
    your my.cnf file is not set or set too low.  A decent value there should
    be 64M or higher depending on the system you are running on.  See
    RELEASE_NOTES for more information.  But setting this and then
    restarting the mysqld and slurmdbd will put things right.  After this
    change we have noticed 50-75% increase in performance with sreport and
    sacct.

* Changes in SLURM 2.1.16
=========================
 -- Set Lft and Rgt correctly when adding association.  Fix for regression
    caused in 2.1.15, cosmetic fix only.
 -- Fix to make jobcomp/(pg/my)sql correctly work when the database name is
    different than the default.

* Changes in SLURM 2.1.11
=========================
 -- Fixed sacct when querying against a jobid the start time is not set.

* Changes in SLURM 2.1.10
=========================
 -- Make sure account and wckey for a job are lower case before inserting into
    accounting.

* Changes in SLURM 2.1.9
========================
 -- Fixed sacct to display correct timelimits for jobs from accounting.
 -- Fixed sacct when running as root by default query all users as documented.
 -- Fixed deadlock if using accounting and cluster changes size in the
    database.  This can happen if you mistakenly have multiple primary
    slurmctld's running for a single cluster, which should rarely if ever
    happen.
 -- Fixed sacct -c option.

* Changes in SLURM 2.1.8
========================
 -- Accounting, fixed bug where if removing an object a rollback wasn't
    possible.
 -- When a cluster first registers with the SlurmDBD only send nodes in an
    non-usable state.  Before all nodes were sent.
 -- Alter sacct to be able to query jobs by association id.
 -- Fix accounting transaction logs when deleting associations to put the
    ids instead of the lfts which could change over time.

* Changes in SLURM 2.1.5
========================
 -- Fixed mysql plugin to reset classification when adding a
    previously deleted cluster.

* Changes in SLURM 2.1.4
========================
 -- Fixed display of Ave/MaxCPU in sacct for jobs. Steps were printed
    correctly.

* Changes in SLURM 2.1.3-1
==========================
 -- sacct - fixed bug when checking jobs against a reservation
 -- Fix accounting when comment of down/drained node has double quotes in it.

* Changes in SLURM 2.1.2
========================
 -- Adjust get_wckeys call in slurmdbd to allow operators to list wckeys.

* Changes in SLURM 2.1.1
========================
 -- Fixed setting the start time when querying in sacct to the
    beginning of the day if not set previously.
 -- Fix issue when changing parents of an account in accounting all children
    weren't always sent to their respected slurmctlds until a restart.
 -- Fix issue where a 2.0 sacct could not talk correctly to a 2.1 slurmdbd.
 -- Update correctly the wckey when changing it on a pending job.
 -- Set wckeyid correctly in accounting when cancelling a pending job.
 