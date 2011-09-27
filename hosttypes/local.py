import string
import platform
import common

def configure_host(host):
    host["platform"] = platform.system().lower()

def run_job(host,job):
    tpl = common.get_command(host,job)
    command = tpl[0]
    args = tpl[1]
    argv = [command]
    argv.extend(args)
    common.exec_job(argv)
