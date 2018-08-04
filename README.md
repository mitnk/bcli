# bcli

Blockchain polish (testing) toolset.

## Set Up

### Setup bcli with Python Virtual ENV

**NOTE:** Python 3 needed.

```
$ python -m venv ~/.local/share/bcli
$ source ~/.local/share/bcli/bin/activate
# now we are inside the Virtual ENV
(bcli)$

# cd to project root dir, and then
(bcli)$ cd ~/projects/bcli
(bcli)$ pip install -U pip
(bcli)$ pip install -r requirements.txt

# cd to bcli package
(bcli)$ cd bcli
(bcli)$ ./bcli.py --help
```

You should see output like the following:

```
usage: bcli [-h] {deploy,info,run,terminate} ...

positional arguments:
  {deploy,info,ssh,run,terminate}
    deploy              Deploy blockchain to EC2
    info                get states of BC
    run                 run a command
    terminate           terminate all AWS resources
```

### Setup AWS Credential

**Option 1 - With Config files**

In file `~/.aws/credentials`:

```
[default]
aws_access_key_id = YOUR_KEY
aws_secret_access_key = YOUR_SECRET
```

**Option 2 - With System Envs**

```
$ export AWS_ACCESS_KEY_ID=<YOUR-KEY>
$ export AWS_SECRET_ACCESS_KEY=<YOUR-SECRET>
```

See more in [boto3 docs on environment configs](http://boto3.readthedocs.io/en/latest/guide/configuration.html#environment-variable-configuration).

## Configs for Deploying

By default, bcli uses `./bcli.json` as the configuration. One sample:

```
$ cat bcli.json
{
    "deploy": {
        "nodes": {
            "us-west-1": 2,
            "ap-southeast-1": 3
        }
    }
}
```

## Deploy EC2 Instances

```
$ ./bcli.py deploy
[INFO][2018-08-04 21:02:52,518] creating 3 nodes in ap-southeast-1
[INFO][2018-08-04 21:02:54,347] created: ['i-06e91c0e14bca62bf', 'i-02b7950e91fa9f5d0', 'i-0d45c78728ffb8503']
[INFO][2018-08-04 21:02:54,347] creating 2 nodes in us-west-1
[INFO][2018-08-04 21:02:56,344] created: ['i-07d82121fe957ef37', 'i-09a022fe64f9bd260']
[INFO][2018-08-04 21:02:56,344] checking state of instances ...
[INFO][2018-08-04 21:03:09,942] instance ('ap-southeast-1', 'i-02b7950e91fa9f5d0') is ready
[INFO][2018-08-04 21:03:10,378] instance ('ap-southeast-1', 'i-0d45c78728ffb8503') is ready
[INFO][2018-08-04 21:03:10,967] instance ('us-west-1', 'i-07d82121fe957ef37') is ready
[INFO][2018-08-04 21:03:11,572] instance ('us-west-1', 'i-09a022fe64f9bd260') is ready
[INFO][2018-08-04 21:03:22,013] instance ('ap-southeast-1', 'i-06e91c0e14bca62bf') is ready
[INFO][2018-08-04 21:03:23,898] all instances are ready now
[INFO][2018-08-04 21:03:25,950] assign new SG to instance: i-02b7950e91fa9f5d0
[INFO][2018-08-04 21:03:26,461] assign new SG to instance: i-0d45c78728ffb8503
[INFO][2018-08-04 21:03:27,112] assign new SG to instance: i-06e91c0e14bca62bf
[INFO][2018-08-04 21:03:29,803] assign new SG to instance: i-07d82121fe957ef37
[INFO][2018-08-04 21:03:30,462] assign new SG to instance: i-09a022fe64f9bd260
```

After deploying, we will get the new created node IDs. This information will
also be written into a local file for later use.  (e.g. `info`)

## Use Ansible

We have generated the Ansible’s inventory file after doing `bcli.py deploy`:

```
(bcli)$ cat sessions/latest/ansible.ini
[us-west-1]
i-00fdc0553bd437015  ansible_host=54.67.111.215  ansible_user=ubuntu  ansible_ssh_private_key_file=/Users/mitnk/projects/bcli/bcli/sessions/latest/key-us-west-1.pem
i-03bc8a0207f119257  ansible_host=54.153.8.243  ansible_user=ubuntu  ansible_ssh_private_key_file=/Users/mitnk/projects/bcli/bcli/sessions/latest/key-us-west-1.pem

[ap-southeast-1]
i-0cf3ae93815cf8587  ansible_host=52.221.188.215  ansible_user=ubuntu  ansible_ssh_private_key_file=/Users/mitnk/projects/bcli/bcli/sessions/latest/key-ap-southeast-1.pem
...
```

With this Ubuntu image, we have to run following command first to make ansible
work properly.

```
(bcli)$ ansible -i sessions/latest/ansible.ini all -a hostname
i-0cf3ae93815cf8587 | FAILED! => {
    "changed": false,
    "module_stderr": "Shared connection to 52.221.188.215 closed.\r\n",
    "module_stdout": "/bin/sh: 1: /usr/bin/python: not found\r\n",
    "msg": "MODULE FAILURE",
...

(bcli)$ ./bcli.py run 'sudo ln -sf /usr/bin/python3 /usr/bin/python'
[INFO][2018-08-05 00:29:20,379] run cmd on i-00fdc0553bd437015 ...
[INFO][2018-08-05 00:29:23,668] run cmd on i-03bc8a0207f119257 ...
[INFO][2018-08-05 00:29:26,674] run cmd on i-0cf3ae93815cf8587 ...
[INFO][2018-08-05 00:29:27,841] run cmd on i-0c4c41acab493f2e8 ...
[INFO][2018-08-05 00:29:29,063] run cmd on i-0e3bacc2d4efa7127 ...

(bcli)$ ansible -i sessions/latest/ansible.ini all -a hostname
i-0e3bacc2d4efa7127 | SUCCESS | rc=0 >>
ip-172-31-12-15
i-0c4c41acab493f2e8 | SUCCESS | rc=0 >>
ip-172-31-14-56
...
```

## Get Information

After a deployment, we can manipulate specific nodes.

```
$ ./bcli.py info
{
    "session_id": "20180804210252",
    "nodes": {
        "ap-southeast-1": [
            {
                "type": "t2.nano",
                "tags": null,
                "ipv4": "52.221.190.226",
                "id": "i-02b7950e91fa9f5d0"
            },
            {
                "type": "t2.nano",
                "tags": null,
                "ipv4": "54.254.129.197",
                "id": "i-0d45c78728ffb8503"
            },
            {
                "type": "t2.nano",
                "tags": null,
                "ipv4": "13.250.105.164",
                "id": "i-06e91c0e14bca62bf"
            }
        ],
        "us-west-1": [
            {
                "type": "t2.nano",
                "tags": null,
                "ipv4": "54.183.133.91",
                "id": "i-07d82121fe957ef37"
            },
            {
                "type": "t2.nano",
                "tags": null,
                "ipv4": "18.144.3.92",
                "id": "i-09a022fe64f9bd260"
            }
        ]
    }
}
```

## Run a random command in one node

```
$ ./bcli.py run --node i-09a022fe64f9bd260 'free -m'
              total        used        free      shared  buff/cache   available
Mem:            486          50          39           1         396         400
Swap:             0           0           0
```

## Terminate

```
$ ./bcli.py terminate
[INFO][2018-08-04 21:07:50,390] Terminating resources in us-west-1 ...
[INFO][2018-08-04 21:07:51,822] - terminated i-07d82121fe957ef37
[INFO][2018-08-04 21:07:52,414] - terminated i-09a022fe64f9bd260
[INFO][2018-08-04 21:07:53,183] - deleted security groups: ['sg-7520030d']
[INFO][2018-08-04 21:07:53,183] Terminating resources in ap-southeast-1 ...
[INFO][2018-08-04 21:07:54,976] - terminated i-06e91c0e14bca62bf
[INFO][2018-08-04 21:07:55,426] - terminated i-02b7950e91fa9f5d0
[INFO][2018-08-04 21:07:55,887] - terminated i-0d45c78728ffb8503
[INFO][2018-08-04 21:07:56,471] - deleted security groups: ['sg-6016a418']
```
