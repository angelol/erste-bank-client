# erste-bank-client

This is a python client for the Erste Bank (Austrian Bank) that allows you to download account statements (Kontoauszüge) as a csv file. It uses George, therefore, the Verfüger needs to be freigeschaltet for George.
### Simple usage:
```python
from erste import ErsteClient
iban = 'XXX' # IBAN of your Erste Bank account
username = 'XXX' # please fill in your Verfügernummer
password = 'XXX' # please fill in your George password

client = ErsteClient(username, password, iban=iban)

begin_date = date.today()-timedelta(days=5)
end_date = date.today()
csv_data = client.get_csv(begin_date, end_date)
```

The above example makes an additional API call to get the internal account id from the iban. For better performance, find the internal account id like this:

```python
client = ErsteClient(username, password, iban=iban)
print client.account_id
```

And then use the account_id instead of IBAN. Initialization of ErsteClient changes to:

```python
client = ErsteClient(username, password, account_id=account_id)
```
This is recommended for better performance.
### Prerequisites
```bash
pip install rsa requests
```

### TODO
* It's not available as a pip package right now
* There is a lot more functionality that the client could offer like sending out wire statements etc. For my personal use case, I only need the Kontoauszüge. If you want to add that functionality, I'm happy to accept patches.
* Only tested in Python 2.7. I have no idea if it works in Python 3.