dir_data="$HOME/gethDataDir"
file_genesis="${dir_data}/genesis.json"
file_logs="${dir_data}/geth.log"

geth --datadir "$dir_data" init "$file_genesis"

nohup geth --datadir "$dir_data" --networkid 917 2>"$file_logs" &
