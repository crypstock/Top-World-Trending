
import requests
import datetime
import hashlib
import hmac
import os

class AmazonAPIClient:
    def __init__(self):
        self.access_key = os.getenv('AMAZON_ACCESS_KEY')
        self.secret_key = os.getenv('AMAZON_SECRET_KEY')
        self.associate_tag = os.getenv('AMAZON_ASSOCIATE_TAG')
        self.region = 'us-east-1'
        self.service = 'ProductAdvertisingAPI'
        
    def sign(self, key, msg):
        return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

    def getSignatureKey(self, key, dateStamp, regionName, serviceName):
        kDate = self.sign(('AWS4' + key).encode('utf-8'), dateStamp)
        kRegion = self.sign(kDate, regionName)
        kService = self.sign(kRegion, serviceName)
        kSigning = self.sign(kService, 'aws4_request')
        return kSigning

    def search_products(self, query='laptop'):
        if not all([self.access_key, self.secret_key, self.associate_tag]):
            raise ValueError("Amazon API credentials not found. Please set them in Secrets.")
            
        method = 'GET'
        host = 'webservices.amazon.com'
        uri = '/paapi5/searchitems'
        endpoint = f'https://{host}{uri}'

        now = datetime.datetime.utcnow()
        amz_date = now.strftime('%Y%m%dT%H%M%SZ')
        date_stamp = now.strftime('%Y%m%d')

        payload = {
            "Keywords": query,
            "SearchIndex": "All",
            "Resources": [
                "ItemInfo.Title",
                "Offers.Listings.Price",
                "Images.Primary.Medium"
            ],
            "PartnerTag": self.associate_tag,
            "PartnerType": "Associates",
            "Marketplace": "www.amazon.com"
        }

        canonical_headers = f'host:{host}\n'
        signed_headers = 'host'
        payload_hash = hashlib.sha256(str(payload).encode('utf-8')).hexdigest()
        canonical_request = f"{method}\n{uri}\n\n{canonical_headers}\n{signed_headers}\n{payload_hash}"

        algorithm = 'AWS4-HMAC-SHA256'
        credential_scope = f"{date_stamp}/{self.region}/{self.service}/aws4_request"
        string_to_sign = f"{algorithm}\n{amz_date}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}"

        signing_key = self.getSignatureKey(self.secret_key, date_stamp, self.region, self.service)
        signature = hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

        authorization_header = (
            f"{algorithm} Credential={self.access_key}/{credential_scope}, "
            f"SignedHeaders={signed_headers}, Signature={signature}"
        )

        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'X-Amz-Date': amz_date,
            'Authorization': authorization_header
        }

        response = requests.post(endpoint, headers=headers, json=payload)
        return response.json()
