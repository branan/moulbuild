class PlatformError(RuntimeError):
    def __init__(self,msg):
        RuntimeError.__init__(self,msg)

def verify_precond_same_host(host,pre_jobs):
    for j in pre_jobs:
        if j["build_host"] is not host:
            raise PlatformError(host["platform"])

def verify_preconditions(host,job):
    try:
        verify_precond_same_host(host,job["precond_same_host"])
    except KeyError:
        pass

def get_command(host,job):
    verify_preconditions(host,job)
    command = host["script_path"]
    try:
        command = command + job["command"][host["platform"]]
    except KeyError:
        raise PlatformError(host["platform"])
    job["build_host"] = host
    arg_dict = {}
    args = ""
    try:
        arg_host = job["client_args"]["build_host"] # we make a copy so we can override arguments if necessary
        arg_dict = dict(arg_host["client_args"])
        if arg_host is host:
            arg_dict["host"] = "localhost"
    except KeyError:
        pass
    if len(arg_dict) == 0:
        return (command,args)
    for arg, val in arg_dict.items():
        args = args + " --%s" % (arg)
        if len(val):
            args = args + "='%s'" % (val)
    return (command,args)
