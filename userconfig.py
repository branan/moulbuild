# This file defines the available systems and the available targets.

# General configuration
# server_type = "pldotnet"
server_type = "dirtsand"

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

build_pldotnet = {
    "hosts" : [live_server,localhost,buildbox],
    "command" : {
        "windows" : "build_pldotnet.bat"
    },
}

stop_pldotnet = {
    "hosts" : [live_server,localhost],
    "depends" : [cwe_client, cwe_python, build_pldotnet],
    "command" : {
        "linux" : "stop_pldotnet.sh",
        "windows" : "stop_pldotnet.bat"
    },
}

build_dirtsand = {
    "hosts" : [live_server,localhost,buildbox],
    "command" : {
        "linux" : "build_dirtsand.sh"
    },
}

stop_dirtsand = {
    "hosts" : [live_server,localhost],
    "depends" : [cwe_client, cwe_python, build_dirtsand],
    "command" : {
        "linux" : "stop_dirtsand.sh",
    },
}
stop_server = locals()['stop_'+server_type]

install_cwe = {
    "hosts" : [localhost,buildbox],
    "command" : {
        "windows" : "install_cwe.py"
    },
    "depends" : [cwe_client, cwe_python, stop_server],
    "precond_same_host" : [cwe_client,cwe_python],
    "client_args" : stop_server
}

install_pldotnet = {
    "hosts" : [live_server,localhost,buildbox],
    "command" : {
        "linux" : "install_pldotnet.py",
        "windows" : "install_pldotnet.py"
    },
    "depends" : [stop_pldotnet,build_pldotnet],
    "precond_same_host" : [build_pldotnet],
    "client_args" : stop_pldotnet
}

install_dirtsand = {
    "hosts" : [live_server,localhost,buildbox],
    "command" : {
        "linux" : "install_dirtsand.py",
    },
    "depends" : [stop_dirtsand,build_dirtsand],
    "precond_same_host" : [build_dirtsand],
    "client_args" : stop_dirtsand
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
    "depends" : [install_datafiles, install_cwe],
    "precond_same_host" : [stop_server],
    "client_args" : stop_server
}

start_pldotnet = {
    "hosts" : [live_server,localhost],
    "command" : {
        "linux" : "start_pldotnet.sh",
        "windows" : "start_pldotnet.bat",
    },
    "depends" : [generate_manifests, install_pldotnet],
    "precond_same_host" : [generate_manifests]
}

start_dirtsand = {
    "hosts" : [live_server,localhost],
    "command" : {
        "linux" : "start_dirtsand.sh",
    },
    "depends" : [generate_manifests, install_dirtsand],
    "precond_same_host" : [generate_manifests]
}

main_target = locals()['start_'+server_type]
