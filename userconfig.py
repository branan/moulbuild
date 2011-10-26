# This file defines the available systems and the available targets.

# HOSTS
localhost = {
    "type" : "local",
    "script_path" : "/home/branan/plasma/urulive/scripts/",
    "client_args" : {
        "user" : "branan",
        "host" : "bokrug",
        "srv_root" : "/home/branan/plasma/urulive/server/"
    }
}

buildbox = {
    "type" : "ssh",
    "platform" : "windows",
    "script_path" : "C:\\urulive\\scripts\\",
#    "vbox_name" : "Uru Build Server",
#    "vbox_user" : "buildbot",
#    "vbox_pass" : "password",
    "ssh_user" : "buildbot",
    "ssh_host" : "192.168.1.35",
    "client_args" : {
    }
}

live_server = {
    "type" : "ssh",
    "platform" : "linux",
    "script_path" : "/home/buildbot/scripts/",
    "ssh_user" : "buildbot",
    "ssh_host" : "guildofwriters.com",
    "client_args" : {
        "srv_root" : "/var/srv/urulive/"
    }
}

allowed_hosts = [localhost,buildbox,live_server]


# TARGETS
cwe_client = {
    "hosts" : [localhost,buildbox],
    "command" : {
        "windows" : "build_cwe.bat",
    },
}

cwe_python = {
    "hosts" : [localhost,buildbox],
    "command" : {
        "windows" : "build_python.bat"
    },
    "depends" : [cwe_client],
    "precond_same_host" : [cwe_client]
}

build_datafiles = {
    "hosts" : [localhost,buildbox],
    "command" : {
        "windows" : "build_datafiles.py",
        "linux" : "build_datafiles.py"
    },
}

build_server = {
    "hosts" : [live_server,localhost,buildbox],
    "command" : {
        "windows" : "build_server.bat"
    },
}

stop_server = {
    "hosts" : [live_server,localhost],
    "command" : {
        "linux" : "stop_server.sh",
        "windows" : "stop_server.bat"
    },
}

install_cwe = {
    "hosts" : [localhost,buildbox],
    "command" : {
        "windows" : "install_cwe.py"
    },
    "depends" : [cwe_client, cwe_python, stop_server],
    "precond_same_host" : [cwe_client,cwe_python],
    "client_args" : stop_server
}

install_server = {
    "hosts" : [live_server,localhost,buildbox],
    "command" : {
        "linux" : "install_server.py",
        "windows" : "install_server.py"
    },
    "depends" : [stop_server,build_server],
    "precond_same_host" : [build_server],
    "client_args" : stop_server
}

install_datafiles = {
    "hosts" : [localhost,buildbox],
    "command": {
        "windows" : "install_datafiles.py",
        "linux" : "install_datafiles.py",
    },
    "depends" : [build_datafiles,stop_server],
    "precond_same_host" : [build_datafiles],
    "client_args" : stop_server
}

generate_manifests = {
    "hosts" : [live_server,localhost],
    "command" : {
        "windows" : "build_manifest.py",
        "linux" : "build_manifest.py"
    },
    "depends" : [install_datafiles, install_cwe, install_server],
    "precond_same_host" : [stop_server]
}

start_server = {
    "hosts" : [live_server,localhost],
    "command" : {
        "linux" : "start_server.sh",
        "windows" : "start_server.bat",
    },
    "depends" : [generate_manifests, install_cwe],
    "precond_same_host" : [generate_manifests]
}

main_target = start_server
