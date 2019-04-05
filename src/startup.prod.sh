pip3 install -r requirements.txt
chmod +x wait-for-it.sh
./wait-for-it.sh anno_db:5432 --timeout=0
uwsgi --ini uwsgi.ini