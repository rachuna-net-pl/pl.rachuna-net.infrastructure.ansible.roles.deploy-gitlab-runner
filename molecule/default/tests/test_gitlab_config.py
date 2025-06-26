import pytest
import re

GITLAB_RUNNER_PACKAGE_NAME = "gitlab-runner"
SUDO_CONFIG_PATH = "/etc/sudoers"

@pytest.mark.parametrize("distro, expected_entry", [
    ("ubuntu", "docker.io"),
    ("almalinux", "docker-ce"),
    ("alpine", "docker"),
])
def test_docker_installed(host,distro, expected_entry):
    os_name = host.system_info.distribution
    if distro in os_name:
        package = host.package(expected_entry)
        assert package.is_installed, "Pakiet "+expected_entry+" nie jest zainstalowany!"
    

def test_gitlab_runner_installed(host):
    package = host.package(GITLAB_RUNNER_PACKAGE_NAME)
    assert package.is_installed, "Pakiet "+GITLAB_RUNNER_PACKAGE_NAME+" nie jest zainstalowany!"


def test_gitlab_runner_status(host):
    content = host.run("sudo gitlab-runner status").stdout
    assert re.search(r"Service\sis\srunning", content), f"Błąd! Gitlab-runner is not running"
