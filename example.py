# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from erste import ErsteClient
from datetime import date, timedelta

def main():
    iban = 'XXX' # IBAN of your Erste Bank account
    username = 'XXX' # please fill in your Verfügernummer
    password = 'XXX' # please fill in your George password
    
    client = ErsteClient(username, password, iban=iban)
    
    begin_date = date.today()-timedelta(days=5)
    end_date = date.today()
    csv_data = client.get_csv(begin_date, end_date)
    print csv_data
    
if __name__ == '__main__':
    main()
