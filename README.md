## C.A.D. Cours à domicile

### Installation

```
git clone <this repo>
cd  <this repo>
virtualenv -p python3 ve
source ve/bin/activate
pip3 install -r requirements.txt
source source.sh env.dev.sh
./manage.py makemigrations
./manage.py migrate
./manage.py runserver
```

## ToDo:
* [X] Add messages to the site admin
* [X] Fix visible email addresses
* [X] Use html/css in mails
* [X] create a cron job to store the log files once a days, and remove those who are older than 3(?) months
* [X] Fix workflow when engaging coaches
* [X] Write tests
* [X] Verify requests choosing
* [X] Send notifications by mail
* [X] Final schedule by admin
* [X] Start and End hours in followElements
* [X] Add admin filtering in lists
* [ ] setup CI/CD
* [X] Test coach swap
* [X] Add password retrieving
