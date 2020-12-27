import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_auditd_installed(host):
    auditd_package_name = _get_auditd_package_name(host.system_info.distribution)
    auditd_package = host.package(auditd_package_name)
    assert auditd_package.is_installed


def test_auditd_service(host):
    service_name = "auditd"
    service = host.service(service_name)
    assert service.is_running
    assert service.is_enabled


def _get_auditd_package_name(host_distro):
    return {
        "centos": "audit",
        "debian": "auditd",
    }.get(host_distro, "auditd")
