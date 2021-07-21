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

- [x] Add messages to the site admin
- [x] Fix visible email addresses
- [x] Use html/css in mails
- [x] create a cron job to store the log files once a days, and remove those who are older than 3(?) months
- [x] Fix workflow when engaging coaches
- [x] Write tests
- [x] Verify requests choosing
- [x] Send notifications by mail
- [x] Final schedule by admin
- [x] Start and End hours in followElements
- [x] Add admin filtering in lists
- [ ] setup CI/CD
- [x] Test coach swap
- [x] Add password retrieving
