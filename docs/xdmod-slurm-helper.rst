XdMod: sacct
============

XdMod issues a call to sacct with the following options:
--allusers --parsable2 --noheader --allocations
[--allclusters | --cluster veredas]
--format jobid, jobidraw, cluster, partition, account,
        group, gid, user, uid, submit, eligible,
        start, end, elapsed, exitcode, state,
        nnodes, ncpus, reqcpus, reqmem, timelimit,
        nodelist, jobname
--states CANCELLED, COMPLETED, FAILED, NODE_FAIL, PREEMPTED,
         TIMEOUT
--starttime  if not set:
                checks the most recent job end datetime in
                database 'shredded_job' of XdMod:

                    $maxDateTime = $shredder->getJobMaxDateTime();
                    $start = new DateTime($maxDateTime);
                    $start->add(new DateInterval('PT1S')); (PT1S=1 second)
                    $start->setTimezone($utc);
             else:
                use the earliest date possible:
                    $start = DateTime::createFromFormat('U', 24 * 60 * 60)
                    U = Seconds since the Unix Epoch
                        (January 1 1970 00:00:00 GMT)
--endtime
            $end = new DateTime('now');
            $end->sub(new DateInterval('P1D')); (P1D=1 day)
            $end->setTime(23, 59, 59);
            $end->setTimezone($utc);

            $args[] = '--endtime';
            $args[] = $end->format('Y-m-d\TH:i:s');


==============================================================================
def datetime_format_python_to_PHP(python_format_string):
    """Given a python datetime format string, attempts to convert it to the nearest PHP datetime format string possible. 
    """
    python2PHP = {"%a": "D", "%a": "D", "%A": "l", "%b": "M", "%B": "F", "%c": "", "%d": "d", "%H": "H", "%I": "h", "%j": "z", "%m": "m", "%M": "i", "%p": "A", "%S": "s", "%U": "", "%w": "w", "%W": "W", "%x": "", "%X": "", "%y": "y", "%Y": "Y", "%Z": "e" }

    php_format_string = python_format_string
    for py, php in python2PHP.items():
        php_format_string = php_format_string.replace(py, php)
    
    return php_format_string
