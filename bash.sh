#!/bin/bash


sudo locale-gen en_US.UTF-8
sudo update-locale

python3 -m %HOME/.geo_venv

source ~/.geo_venv/bin/activate

pip install -r requirements.txt

task1="0 */2 * * * /home/user/.venv/bin/python3 /opt/geodata/fetch.py"

task2="2 */2 * * * /home/user/.venv/bin/python3 /opt/geodata/subscribe.py Statusmail"

temp_file="/tmp/mycron"

crontab -l > $temp_file 2>/dev/null

grep -qxF "$task1" $temp_file || echo "$task1"  >> $temp_file

grep -qxF "$task2" $temp_file || echo "$task2"  >> $temp_file

crontab $temp_file

rm $temp_file

echo "Crontab updated with new task"
