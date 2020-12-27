Auditd
======

Install and load a basic set of security rules to auditd service.

**NOTE:** These are Generic rules which should work on all systems. 

**NOTE:** Some rules can also generate quite a lot of messages in the logs. Unwanted messages can be filtered out as required.

More specific rules should be seperately created for applications/systems.

Requirements
------------

Supported OS:
  - Debian 10
  - RedHat 8

**NOTE:** Currently auditd doesn't run under containers, such as Docker/Podman. 

Role Variables
--------------

```
# Collect local events
# Auditd doesn't collect events when running in a container and can only be used to aggregate logs from other systems.
auditd_local_events: "{{ false if ansible_virtualization_role | default(null) == 'guest' and ansible_virtualization_type in ('docker','podman') else true}}"

# Write log file options
auditd_write_logs: true 
auditd_log_file: "/var/log/audit/audit.log"
auditd_log_group: "{{ auditd__log_group }}"
# Debian: adm
# RedHat: root

# Format of log (RAW, ENRICHED)
auditd_log_format: "ENRICHED"

# Method of flushing records to dish (none, incremental, incremental_async, data, sync)
auditd_flush: "INCREMENTAL_ASYNC"

# How many records to write before forced disk flush; when using incremental flush
auditd_freq: 50 

# Keep 7 128MB for a total of 896 maximum. 
auditd_max_log_file:  128
auditd_num_logs: 7 

# Boost the auditd nice value
auditd_priority_boost: 4 

# Method of communication between audit daemon and dispatcher
auditd_disp_qos: lossy 
# lossy: non-blocking
# lossess: blocking

# The dispatcher is a program that is started by the audit daemon at starts up. 
# It will pass a copy of all audit events to that application's stdin.
auditd_dispatcher: /sbin/audispd 

# Controls how computer node names are inserted into the audit event stream.
# Choices: none, hostname, fqdn, numeric, and user.
auditd_name_format: NONE 

# Identifies the machine if user is given as the name_format option
auditd_name: null 
# Example: mydomain

# Action to take when the system has detected that the max file size limit has been reached.
auditd_max_log_file_action: ROTATE 
# ignore
# syslog
# suspend
# rotate
# keep_logs

# Perform action when under given value in MB
auditd_space_left: 75 
# Action to perform when low disk space
auditd_space_left_action: SYSLOG 
# ignore
# syslog
# email
# exec
# suspend
# single
# halt

# Check action_mail_acct to see if domain name can be resolved.
auditd_verify_email: true 

# Valid email address, sendmail setup required if not local address.
auditd_action_mail_acct: root 

# Perform last chance action when breach given value in MB
auditd_admin_space_left: 50 
# Action to perform when admin_space_left is breached
auditd_admin_space_left_action: SUSPEND 

# Action to take when disk is full.
auditd_disk_full_action: SUSPEND 

# Action to take when error detected when writing audit events to disk or rotating logs.
auditd_disk_error_action: SUSPEND 

# Use tcp_wrappers to discern connection attempts that are from allowed machines.
auditd_use_libwrap: true 

# If given, listen on port for records from remote systems. 
auditd_tcp_listen_port: null #60 

# how many pending (requested but unaccepted) connections are allowed.
auditd_tcp_listen_queue: 5 

# How many concurrent connections from one IP address is allowed.
auditd_tcp_max_per_addr: 1 

# Which client ports are allowed for incoming connections. If not specified, any port is allowed.
# Making sure that clients send from a privileged port (1-1023) is a security feature to prevent log injection 
# attacks by untrusted users.
auditd_tcp_client_ports: 1-1023

# Close inactive connections if client cannot shutdown the connection cleanly. 0 to disable check.
auditd_tcp_client_max_idle: 0 

# Use kerberos 5 for authentication and encryption
auditd_enable_krb5: false 
#  principal for this server.
auditd_krb5_principal: auditd 
# Location of the key for this client's principal
auditd_krb5_key_file: null #etc/audit/audit.key 

# Network originating events will be distributed to the audit dispatcher for processing.
auditd_distribute_network: false 

# How big to make the internal queue of the audit event dispatcher
auditd_q_dpeth: 400

# Number to time to try to restart a plugin.
auditd_max_restarts: 10

# Connection type
auditd_transport: "TCP"
# TCP: clear text tcp connection
# KRB5: Kerberos 5 used for authentication and encryption

# Location to load plugins from
auditd_plugin_dir: "/etc/audit/plugins.d"

# Action when overflowing its internal queue detected.
auditd_overflow_action: "SYSLOG"

# Rules
#######

# Max number of outstanding audit buffers allowed
auditd_buffer_size: 8192

# This determine how long to wait in burst of events
auditd_backlog_wait_time: 0

# Set failure mode to syslog
auditd_failure_mode: 1
#  0=silent
#  1=printk
#  2=panic

# Ignore errors when reading rules from a file. This causes auditctl to always return a success exit code. 
auditd_ignore_errors: false

# Make the rules immutable
auditd_immutable_rules: false

# Filter out specific messages to reduce noise
auditd_filter_list: []
# Examples:
#  - arch: b64
#    fields:
#      dir: /var/lock/lvm
#    key: locklvm
#  - syscall: adjtimex
#    arch: b64
#    fields:
#      auid: unset
#      uid: chrony
#      subj_type: chronyd_t
#  - syscall: connect
#    arch: b64
#    fields:
#      a2: 16
#      success: 1
#      uid: chrony
#  - fields:
#      uid: username
#      dir: /usr/bin/whoami
#      perm: x

# uid to start users lookup range
auditd_user_uid: 1000

# Log every 32bit syscall on 64bit by default
auditd_32bit_api: "{{ true if ansible_architecture == 'x86_64' else false }}"

# Ignore SELinux AVC records
auditd_filter_selinux_avc: true

# Log root user power abuses (viewing home directories)
auditd_power_abuse: true

# Log code injections vt ptrace
auditd_code_injection: true

# Log all user file deletions
auditd_user_file_delete: true

# Log changes to /tmp & /var/tmp
auditd_tmp_changes: true

# Log commands run as root
auditd_root_commands: true

# Log unsuccessful access by users
auditd_unauthorized_access: true

# Log unsuccessful creation
auditd_failed_creation: true

# Log unsuccessful modifications
auditd_failed_modification: true

# Log network connections
auditd_network_connect: true

# Audit package manage 
auditd_package_manager_execs: "{{ auditd__package_manager_execs }}"
# Debian:
#   - /usr/bin/dpkg
#   - /usr/bin/apt-add-repository
#   - /usr/bin/apt-get
#   - /usr/bin/aptitude
#   - /usr/bin/apt
#   - /usr/bin/wajig
# RedHat:
#   - /usr/bin/rpm
#   - /usr/bin/yum
#   - /usr/bin/dnf
#   - /usr/bin/dnf-3
auditd_package_manager_files: "{{ auditd__package_manager_files }}"
# Debian:
#   - /etc/apt/sources.list
#   - /etc/apt/sources.list.d
# RedHat:
#   - /etc/yum.repos.d

# Audit system network files
auditd_network_files: "{{ auditd__network_files }}"
# Debian:
#   - /etc/hosts
#   - /etc/resolv.conf
#   - /etc/network/
# RedHat:
#   - /etc/hosts
#   - /etc/resolv.conf
#   - /etc/sysconfig/network
#   - /etc/sysconfig/network-scripts
#   - /etc/networks
#   - /etc/NetworkManager/

# Audit system firewall files
auditd_firewall_files: "{{ auditd__firewall_files }}"
# Debian:
#   - /etc/nftables.conf
#   - /etc/firewalld
#   - /etc/lib/firewalld
#   - /etc/iptables.up.rules
# RedHat:
#   - /etc/nftables
#   - /etc/firewalld
#   - /etc/lib/firewalld
#   - /etc/sysconfig/iptables
#   - /etc/sysconfig/ip6tables
```

Dependencies
------------

None

Example Playbook
----------------

```
- hosts: servers
  tasks:
    - name: "Include auditd"
      include_role:
        name: auditd
```

License
-------

LGPLv3

Author Information
------------------

- Robert Brightling | [GitLab](https://gitlab.com/brightling) | [GitHub](https://github.com/rbrightling)
