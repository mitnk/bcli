# bcpol

Blockchain polish (testing) toolset.

## The Goal

todo

## Config

By default, bcpol use `./bcpol.json` as the configuration. One sample:

```
$ cat bcpol.json
{
    "deploy": {
        "nodes": {
            "us-west-1": 3,
            "ap-northeast-1": 2,
            "eu-west-2": 2
        },
        "image": "ethereum/client-go"
    }
}
```

## Deploy

```
$ bcpol deploy
{
    "nodes": {
        "us-west-1": ["93c0f1715", "d9575e92", "fc6e52ba"],
        "ap-northeast-1": ["18267410f", "cd2426d5"],
        "eu-west-2": ["f49e5f4b7", "eecd3017"]
    }
}
```

After deploying, we will get the new created node IDs. These information will
also be written into a file `deploy.output` for later use.  (e.g. `stats`)

## Stop/Start/etc

After a deployment, we can manipulate specific nodes.

```
# stop one node in us-west-1
$ bcpol stop d9575e92
stopped
$ bcpol start d9575e92
started
```

Run a random command in one node

```
$ bcpol run d9575e92 "whatever cmd we want"
```

## Monitoring

There are two commands can be used to check the status of the blockchain.

### check out the logs in one node

```
$ bcpol logs 93c0f1715

WARN [07-27|15:41:57.437] Sanitizing cache to Go's GC limits       provided=1024 updated=330
INFO [07-27|15:41:57.438] Maximum peer count                       ETH=25 LES=0 total=25
INFO [07-27|15:41:57.440] Starting peer-to-peer node               instance=Geth/v1.8.13-unstable-93c0f171/linux-amd64/go1.10.3
INFO [07-27|15:41:57.440] Allocated cache and file handles         database=/home/xxxx/gethDataDir/geth/chaindata cache=247 handles=512
INFO [07-27|15:41:57.475] Initialised chain configuration          config="{ChainID: 917 Homestead: ...
INFO [07-27|15:41:57.476] Disk storage enabled for ethash caches   dir=/home/xxxx/gethDataDir/geth/ethash count=3
INFO [07-27|15:41:57.476] Disk storage enabled for ethash DAGs     dir=/home/xxxx/.ethash
...
```

### Checkout the states of the whole blockchain

```
$ bcpol stats
{
    "peer_count": 6,
    "difficulty": 10000,
    "balances": {
        "abc": 345.6789,
        "eee": 1232356767.098,
        "xxx": 50000.0
    },
    "mining": true,
    "blocks": [
        {"_id": 001, "hash": "abc", "ts": 1532747717.659872},
        {"_id": 002, "hash": "eee", "ts": 1532747739.370306},
        ...
    ],
    ...
}
```

## Download

We can download the final state (data), and use it in later testing. For
example, use `snapshot-0728.data` as the initial states in next version of
docker image.

```
$ bcpol stopall
$ bcpol backup ./snapshot-0728.data
```

## Terminate

Use `bcpol stopall` to stop all activities of the blockchain.

Use `bcpol terminate` to shutdown all nodes and terminate all resources on AWS.
