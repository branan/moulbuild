import common

def configure_host(host):
    pass

def run_job(host,job):
    tpl = common.get_command(host,job)
    command = tpl[0]
    args = tpl[1]
    print "ssh %s@%s %s %s" % (host["ssh_user"], host["ssh_host"], command, args)
