import common

def configure_host(host):
    arguments = host["client_args"]
    arguments["user"] = host["ssh_user"]
    arguments["host"] = host["ssh_host"]

def run_job(host,job):
    tpl = common.get_command(host,job)
    command = tpl[0]
    args = tpl[1]
    argv = ["ssh", "%s@%s" % (host["ssh_user"], host["ssh_host"]), command]
    argv.extend(args)
    common.exec_job(argv)
