# Playbooks for Deploying ETH

## Configs

```
$ pip install ansible
$ sudo mkdir -p /etc/ansible
$ sudo ln -sf ~/.bcli/sessions/latest/ansible.ini /etc/ansible/hosts
```

## Setup and Start ETH

```
$ cd playbooks/ethereum
(bcli)$ ansible-playbook setup-envs.yml
(bcli)$ ansible-playbook setup-geth.yml
(bcli)$ ansible-playbook start-geth.yml
```

## Add Peers with Each Other

```
(bcli)$ ansible-playbook add-peers.yml
```

## List Peers

```
(bcli)$ ansible-playbook list-peers.yml
```
