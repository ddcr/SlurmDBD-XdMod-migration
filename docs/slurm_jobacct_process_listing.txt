FLOW OF THE ROUTINE
===================

extern List mysql_jobacct_process_get_jobs(mysql_conn_t *mysql_conn, uid_t uid,
					   acct_job_cond_t *job_cond)

	(1)
		/* slurm_get_private_data
		* get private data from slurmctld_conf object
		*/
        extern slurm_dbd_conf_t *slurmdbd_conf;
        slurmdbd_conf->private_data

        Option PrivateData from slurmdbd.conf: 
			    This controls what type of information is hidden from regular users. 
			    By default, all information is visible to all users. User SlurmUser, 
			    root, and users with AdminLevel=Admin can always view all information. 
			    Multiple values may be specified with a comma separator.

	(2) if(job_cond && job_cond->used_nodes) { ... } NOT RELEVANT because we do not
	    select option [-N | --nodes] in sacct, SO job_cond->used_nodes = 0


	(3) Establish limits of the query for the jobs
		setup_job_cond_limits(mysql_conn, job_cond, &extra);

	(4) NOT RELEVANT TO US
	    if(!is_admin && (private_data & PRIVATE_DATA_JOBS)) { ... }

	(5) Build string query concatenating all options

	(6) Do the actual mysql query and order queried data as 
	    "order by t1.cluster, jobid, submit desc"
        Some job numbers will probably appear more than once (duplicates)

	(6) Now retrieve the data from mysql

	(7) Parsing of the returned data with error checking

	    while((row = mysql_fetch_row(result))) {

	    	(7.1) If JobID is repeated get the most recent job (check its submission time)

	    	(7.2)  NOT RELEVANT TO US because we only have one cluster and
	    	       our query is not against any particular node or list of nodes
	    	       (we do not set sacct with option [-N|--nodes])

	    			/* check the bitmap to see if this is one of the jobs
		              we are looking for */
		            if(!good_nodes_from_inx(local_cluster_list,
											(void **)&curr_cluster,
											row[JOB_REQ_NODE_INX], submit))
						continue;

			(7.3)   Correct ANOMALOUS jobs which ended
							if(job->end) {
								job_ended = 1;
								if(!job->start || (job->start > job->end))
												job->start = job->end;
							}

			(7.4)	Compute job->elapsed
			        NOTE: We do not consider the truncation of the start and end times of jobs
			              that overlap with specified interval time of sacct [interval set with
			              --startime and --endtime]

			        Actual computation: 
			        job->suspended = atoi(row[JOB_REQ_SUSPENDED]);
					if(!job->start) {
						job->elapsed = 0;
					} else if(!job->end) {
						job->elapsed = now - job->start;
					} else {
						job->elapsed = job->end - job->start;
					}
					job->elapsed -= job->suspended;
					if((int)job->elapsed < 0)
						job->elapsed = 0;

			(7.5)   WE CONSIDER ALL JOBS AND DO NOT CONSIDER STEP JOBS 

	    }