Ansible Role do automatyzacji instalacji i konfiguracji GitLab Runnerów. Ta rola automatyzuje instalację i konfigurację GitLab Runnerów na różnych dystrybucjach Linuksa.

---
## Obsługiwane platformy

- Debian (wszystkie wersje)
- Ubuntu (wszystkie wersje)
- Alpine (wszystkie wersje)
- Enterprise Linux (EL) 7, 8, 9

---
## Wymagania

- Ansible w wersji 2.9 lub wyższej
- Docker (opcjonalnie, może być zainstalowany przez rolę)

---
## Zmienne roli

| Zmienna                         | Domyślna wartość                                                        | Opis                                                                                           |
|--------------------------------|------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|
| `input_debug`                  | `false`                                                                | Włączenie trybu debugowania                                                                    |
| `input_install_docker`         | `true`                                                                 | Czy instalować Dockera                                                                         |
| `input_gitlab_runner_configuration` | Zobacz poniżej                                                    | Konfiguracja GitLab Runnerów, w tym liczba równoczesnych runnerów, timeouty sesji i lista runnerów |

---
### Przykład `input_gitlab_runner_configuration`

```yaml
input_gitlab_runner_configuration:
  concurrent: 100
  check_interval: 0
  shutdown_timeout: 0
  session_timeout: 3600
  runners:
    - name: "molecule test"
      url: "https://gitlab.com"
      register_runner:
        # id: 12345678 # Jeśli nie jest ustawione, nowy runner zostanie wygenerowany przez API GitLab
        register_gitlab_api_token: "{{ lookup('env', 'GITLAB_TOKEN') }}"
        description: "default runner"
        tag_list: ["none"]
        runner_type: "group_type"
        group_id: 12345678
        access_level: "not_protected"
        # token: "***" # Jeśli nie jest ustawione, nowy runner zostanie wygenerowany przez API GitLab
      executor: "docker"
      docker:
        tls_verify: false
        image: "docker:latest"
        privileged: true
        disable_entrypoint_overwrite: false
        oom_kill_disable: false
        disable_cache: false
        volumes:
          - "/cache"
          - "/var/run/docker.sock:/var/run/docker.sock"
        shm_size: 0
```

---
## Przegląd zadań

- Instalacja wymaganych pakietów i Dockera (opcjonalnie, kontrolowane przez `input_install_docker`)
- Rejestracja GitLab Runnerów przez API GitLab, jeśli ID lub token runnera nie są podane
- Konfiguracja GitLab Runnerów zgodnie z podaną konfiguracją

---
## Przykład użycia

```yaml
- hosts: gitlab_runners
  roles:
    - role: deploy-gitlab-runner
      vars:
        input_debug: true
        input_gitlab_runner_configuration:
          concurrent: 100
          check_interval: 0
          shutdown_timeout: 0
          session_timeout: 3600
          runners:
            - name: "molecule test"
              url: "https://gitlab.com"
              register_runner:
                id: "{{ lookup('env', 'GITLAB_RUNNER_ID') }}"
                register_gitlab_api_token: "{{ lookup('env', 'GITLAB_TOKEN') }}"
                description: "molecule test"
                tag_list: ["none"]
                runner_type: "group_type"
                group_id: "{{ lookup('env', 'GITLAB_GROUP_REPOSITORY_ID') }}"
                access_level: "not_protected"
                token: "{{ lookup('env', 'GITLAB_RUNNER_TOKEN') }}"
              executor: "docker"
              docker:
                tls_verify: false
                image: "docker:latest"
                privileged: true
                disable_entrypoint_overwrite: false
                oom_kill_disable: false
                disable_cache: false
                volumes:
                  - "/cache"
                  - "/var/run/docker.sock:/var/run/docker.sock"
                shm_size: 0

```

---
## Testowanie

Rola jest testowana za pomocą Molecule na następujących platformach:

- Ubuntu 24.10
- Alpine 3.21.2
- AlmaLinux 9.6

Molecule używa sterownika `molecule-proxmox` do testów.

