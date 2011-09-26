import common

def configure_host(host):
    pass

def run_job(host,job):
    tpl = common.get_command(host,job)
    command = tpl[0]
    args = tpl[1]
    print "VBoxManage --nologo guestcontrol '%s' execute --image '%s' --username '%s' --password '%s' --wait-exit --wait-stdout --%s" % (host["vbox_name"], command, host["vbox_user"], host["vbox_pass"], args)
