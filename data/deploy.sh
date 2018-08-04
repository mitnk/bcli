sudo chown -R ubuntu:ubuntu /usr/local
wget 'https://hugo.wang/media/geth' -O /usr/local/bin/geth
chmod +x /usr/local/bin/geth

dir_data="$HOME/gethDataDir"
file_genesis="${dir_data}/genesis.json"
file_logs="${dir_data}/geth.log"

mkdir -p $dir_data
wget 'https://hugo.wang/media/genesis.json' -O "$file_genesis"

geth --datadir "$dir_data" init "$file_genesis"

nohup geth --datadir "$dir_data" --networkid 917 2>"$file_logs" &
