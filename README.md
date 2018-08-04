# bcpol

Blockchain polish (testing) toolset.

## Config

By default, bcpol uses `./bcpol.json` as the configuration. One sample:

```
$ cat bcpol.json
{
    "deploy": {
        "nodes": {
            "us-west-1": 3,
            "ap-northeast-1": 2
        },
        "image": "ethereum/client-go"
    }
}
```

## Deploy

```
$ bcpol deploy
$ ./bcpol.py deploy
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

## Get Information

After a deployment, we can manipulate specific nodes.

```
$ ./bcpol.py info
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
$ ./bcpol.py run --node i-09a022fe64f9bd260 'free -m'
              total        used        free      shared  buff/cache   available
Mem:            486          50          39           1         396         400
Swap:             0           0           0
```

## Terminate

```
$ ./bcpol.py terminate
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
