#!/bin/bash
# . pystart.sh または source pystart.shとして実行(./pystartではない)

#!/bin/bash

# IPアドレスを取得
full_ip=$(ifconfig  | grep '192' | head -n 1 |  awk '{ print $2 }' | cut -d'/' -f1)

# 最後のオクテットを取得
last_octet=$(echo $full_ip | awk -F. '{print $4}')

# 変数に格納
ip_last_octet=$last_octet

# 確認のため出力
# echo "IPアドレスの最後のオクテット: $ip_last_octet"

source .venv$ip_last_octet/bin/activate

# git pull origin master
