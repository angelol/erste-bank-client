# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
import json
import settings
import os
import re
from datetime import date
import rsa
import binascii
from datetime import timedelta
from django.utils.functional import cached_property

class ErsteClient(object):
    def __init__(self, username, password, iban=None, account_id=None):
        self.username = username
        self.password = password
        self.iban = iban
        self._account_id = account_id

    @cached_property
    def access_token(self):
        def RSA(n, e, salt, password):
            """ Translated from site javascript code:
        
                var rsa = new RSAKey();
                rsa.setPublic(modulus, exponent);	
                return rsa.encrypt(salt + "\t" + password);
            """
            n = int(n, base=16)
            e = int(e, base=16)
            message = "%s\t%s" % (salt, password)
            cypherbytes = rsa.encrypt(message.encode('utf-8'), rsa.PublicKey(n, e))
            return binascii.b2a_hex(cypherbytes)
    
        s = requests.Session()
        url = 'https://login.sparkasse.at/sts/oauth/authorize?response_type=token&client_id=georgeclient'
        r = s.get(url)
        # print r.headers
        r = s.post(url, data={
            'javaScript': 'jsOK',
            'SAMLRequest': 'ignore',
        })
        match = re.search(r'var random = "(.*?)";', r.text)
        salt = match.groups()[0]
    
        match = re.search('name="modulus" value="(.*)?"', r.text)
        modulus = match.groups()[0]

        match = re.search('name="exponent" value="(.*)?"', r.text)
        exponent = match.groups()[0]
    
        rsaEncrypted = RSA(modulus, exponent, salt, self.password)

        post_data = {
            'rsaEncrypted': rsaEncrypted,
            'saltCode': salt,
            'j_username': self.username
        }
        # print 'post_data: ', post_data
        url = 'https://login.sparkasse.at/sts/oauth/authorize?client_id=georgeclient&response_type=token'
        r = s.post(url, data=post_data, allow_redirects=False)
        # print 'r.headers: ', r.headers
        match = re.search(r'#access_token=(.*?)&', r.headers['location'])
        if match:
            token = match.groups()[0]
            return token

    # print r.text.encode('utf-8')
    @property
    def account_id(self):
        if not self._account_id:
            r = requests.get('https://api.sparkasse.at/proxy/g/api/my/accounts', headers={'Authorization': 'bearer %s' % self.access_token})
            data = r.json()
            # print 'data: ', data
            for account in data['collection']:
                accountno = account.get('accountno')
                if accountno and accountno.get('iban') == self.iban:
                    self._account_id = account['id']
        return self._account_id
    
    def get_csv(self, start_date, end_date):
        strf_format = '%Y-%m-%dT%H:%M:%S'
        
        url = 'https://api.sparkasse.at/proxy/g/api/my/transactions/export.csv?from=%(start_date)s&to=%(end_date)s&lang=de&separator=;&mark=%%22&fields=booking,receiver,amount,currency,reference,referenceNumber,valuation' % {'start_date': start_date.strftime(strf_format), 'end_date': end_date.strftime(strf_format)}
        r = requests.post(url, 
            data={
                'access_token': self.access_token,
                'id': self.account_id,
            })
        return r.text
        
