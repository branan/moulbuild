import userconfig
import hosttypes
from hosttypes.common import PlatformError

available_hosts = []

for host in userconfig.allowed_hosts:
    try:
        hosttypes.__dict__[host["type"]].configure_host(host)
        available_hosts.append(host)
    except:
        pass # if there are any errors configuring a host, we just ignore that host
    

def dispatch(job):
    for host in job["hosts"]:
        if host in available_hosts:
            try:
                hosttypes.__dict__[host["type"]].run_job(host,job)
                return
            except PlatformError:
                pass
    raise RuntimeError("None of the listed platforms for this target were available!")