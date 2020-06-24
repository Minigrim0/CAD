## C.A.D. Cours à domicile

### Installation

```
git clone <this repo>
cd  <this repo>
virtualenv -p python3 ve
source ve/bin/activate
pip3 install -r requirements.txt
./manage.py makemigrations
./manage.py migrate
./manage.py runserver
```

## ToDo:
once uploaded : create a cron job to store the log files once a days, and remove those who are older than 3(?) months
