import common

def configure_host(host):
    pass

def run_job(host,job):
    tpl = common.get_command(host,job)
    command = tpl[0]
    args = tpl[1]
    argv = ["VBoxManage", "--nologo", "guestcontrol", host["vbox_name"], "execute", "--image", command, "--username", host["vbox_user"], "--password", host["vbox_pass"], "--wait-exit", "--wait-stdout", "--verbose"]
    if len(args) != 0:
        argv.append("--")
        argv.extend(args)
    common.exec_job(argv)
