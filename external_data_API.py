#!/usr/bin/env python3
import time
import collections
import random
import math
import requests
import string
import json
import django
import os
import tableauserverclient as TSC
from datetime import datetime
os.environ['DJANGO_SETTINGS_MODULE'] = 'asset_catalog.settings'
django.setup()
from asset_catalog.settings import MEDIA_ROOT, AUTH_LDAP_BIND_DN, AUTH_LDAP_BIND_PASSWORD, AUTH_LDAP_SERVER_URI, TABLEAU_USER, TABLEAU_PASSWORD, ALTERYX_KEY, ALTERYX_SECRET
from asset_mgmt.models import AssetCatalog, User, AssetType, AlteryxStudio, TableauServer, TableauSite
from ldap3 import Server, Connection, SUBTREE
import re


class Gallery(object):
    def __init__(self, apiLocation, apiKey, apiSecret):
        self.apiLocation = apiLocation
        self.apiKey = apiKey
        self.apiSecret = apiSecret

    def buildOauthParams(self):
        return {'oauth_consumer_key': self.apiKey,
                'oauth_nonce': self.generate_nonce(5),
                'oauth_signature_method': 'HMAC-SHA1',
                'oauth_timestamp': str(int(math.floor(time.time()))),
                'oauth_version': '1.0'}

    '''Finds workflows in a subscription'''

    def subscription(self):
        method = 'GET'
        url = self.apiLocation + '/workflows/subscription/'
        params = self.buildOauthParams()
        signature = self.generateSignature(method, url, params)
        params.update({'oauth_signature': signature})
        output = requests.get(url, params=params)
        return output.text

    def subscription_admin(self):
        method = 'GET'
        url = self.apiLocation.replace('v1', 'admin/v1/workflows/')
        params = self.buildOauthParams()
        signature = self.generateSignature(method, url, params)
        params.update({'oauth_signature': signature})
        output = requests.get(url, params=params)
        return output.text

    '''Returns the questions for the given Alteryx Analytics App'''

    def questions(self, appId):
        method = 'GET'
        url = self.apiLocation + '/workflows/' + appId + '/questions/'
        params = self.buildOauthParams()
        signature = self.generateSignature(method, url, params)
        params.update({'oauth_signature': signature})
        output = requests.get(url, params=params)
        return output, output.content

    '''Queue an app execution job. Returns ID of the job'''

    def executeWorkflow(self, appId, *kwpos, **kwargs):
        if('payload' in kwargs):
            print('Payload included: %s' % kwargs['payload'])
            data = kwargs['payload']
            method = 'POST'
            url = self.apiLocation + '/workflows/' + appId + '/jobs/'
            params = self.buildOauthParams()
            signature = self.generateSignature(method, url, params)
            params.update({'oauth_signature': signature})
            output = requests.post(url, json=data, headers={'Content-Type':'application/json'}, params=params)
        else:
            print('No Payload included')
            method = 'POST'
            url = self.apiLocation + '/workflows/' + appId + '/jobs/'
            params = self.buildOauthParams()
            signature = self.generateSignature(method, url, params)
            params.update({'oauth_signature': signature})
            output = requests.post(url, params=params)
            
        return output,output.content


    '''Returns the jobs for the given Alteryx Analytics App'''

    def getJobs(self, appId):
        method = 'GET'
        url = self.apiLocation + '/workflows/' + appId + '/jobs/'
        params = self.buildOauthParams()
        signature = self.generateSignature(method, url, params)
        params.update({'oauth_signature': signature})
        output = requests.get(url, params=params)
        return output, output.content

    '''Retrieves the job and its current state'''

    def getJobStatus(self, jobId):
        method = 'GET'
        url = self.apiLocation + '/jobs/' + jobId + '/'
        params = self.buildOauthParams()
        signature = self.generateSignature(method, url, params)
        params.update({'oauth_signature': signature})
        output = requests.get(url, params=params)
        return output, output.content

    '''Returns the output for a given job (FileURL)'''

    def getJobOutput(self, jobID, outputID):
        method = 'GET'
        url = '/jobs/' + jobID + '/output/' + '/outputID/'
        params = self.buildOauthParams()
        signature = self.generateSignature(method, url, params)
        params.update({'oauth_signature': signature})
        output = requests.get(url, params=params)
        return output, output.content

    '''Returns the App that was requested'''

    def getApp(self, appId):
        method = 'GET'
        url = self.apiLocation + '/' + appId + '/package/'
        params = self.buildOauthParams()
        signature = self.generateSignature(method, url, params)
        params.update({'oauth_signature': signature})
        output = requests.get(url, params=params)
        return output, output.content

    '''Generate pseudorandom number'''

    def generate_nonce(self, length=5):
        return ''.join([str(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase)) for i in
                        range(length)])

    def generateSignature(self, httpMethod, url, params):
        import urllib.parse
        import hmac
        import binascii
        import hashlib
        from requests.utils import quote
        from base64 import b64encode

        """returns HMAC-SHA1 sign"""

        q = lambda x: quote(x, safe="~")
        sorted_params = collections.OrderedDict(sorted(params.items()))
        normalized_params = urllib.parse.urlencode(sorted_params)
        base_string = "&".join((httpMethod.upper(), q(url), q(normalized_params)))

        sig = hmac.new(("&".join([self.apiSecret, ''])).encode("utf8"), base_string.encode("utf8"), hashlib.sha1).digest()
        byte_array = b64encode(sig)
        # convert the byte array to UTF-8 characters using the decode function
        return byte_array.decode("utf-8")

# {
#     "id": "57617163e802472538af4fb0",
#     "subscriptionId": "503bac188031af11f8f8e478",
#     "public": true,
#     "runDisabled": true,
#     "packageType": 0,
#     "uploadDate": "2016-06-15T15:16:51.718Z",
#     "fileName": "Adobe Analytics Toolkit.yxwz",
#     "metaInfo": {
#       "name": "Adobe Analytics Toolkit",
#       "description": "Toolkit that contains configuration applications and an Adobe Connector tool (macro) that pulls custom reports from the Adobe Marketing Cloud API.",
#       "author": "Taylor Cox",
#       "copyright": "",
#       "url": "",
#       "urlText": "",
#       "outputMessage": "Authentication Successful!",
#       "noOutputFilesMessage": ""
#     },
#     "isChained": true,
#     "version": 1,
#     "runCount": 0,
#     "workerTag": ""
#   },


class TableauAPI(object):
    def __init__(self, apiLocation, apiUser, apiPass, site_id):
        self.tableau_auth = TSC.TableauAuth(apiUser, apiPass, site_id)
        self.server = TSC.Server(apiLocation)
        self.location = apiLocation
        self.sitename = site_id

    def get_workbooks_tableau(self):
        tableau_products = []
        with self.server.auth.sign_in(self.tableau_auth):
            request_options = TSC.RequestOptions(pagesize=1000)
            site_id = self.server.site_id
            all_workbooks, pagination_item = self.server.workbooks.get(request_options)
            for book in all_workbooks:
                self.server.workbooks.populate_preview_image(book)
                product_url = self.location + '/#/site/' + self.sitename + '/views/product_view'
                project_image = book.preview_image
                product = {'product_name': book.name, 'product_id': book.id, 'create_at': book.created_at,
                           'updated_at': book.updated_at, 'project_name': book.project_name,
                           'owner_id': book.owner_id,
                           'owner_user': '', 'views': 0, 'product_url': product_url, 'project_image': book.id + '.png',
                           'content_url': book.content_url}
                tableau_products.append(product)

                # path = os.path.join(MEDIA_ROOT, book.id + '.png')
                # f = open(path, 'wb')
                # f.write(bytearray(project_image))
                # f.close()

        return tableau_products, site_id, pagination_item.total_available

    def get_tableau_views(self):
        with self.server.auth.sign_in(self.tableau_auth):
            request_options = TSC.RequestOptions(pagesize=1000)
            product_view = {}
            all_views, pagination_item = self.server.views.get(request_options, usage=True)
            for view in all_views:
                if view.workbook_id not in product_view:
                    product_view[view.workbook_id] = {'url': view.content_url.replace('sheets/', ''), 'count': 0, 'total': 0}
                product_view[view.workbook_id]['count'] += 1
                product_view[view.workbook_id]['total'] += int(view.total_views)
            return product_view

    def get_tableau_users(self):
        with self.server.auth.sign_in(self.tableau_auth):
            request_options = TSC.RequestOptions(pagesize=1000)
            all_users, pagination_item = self.server.users.get(request_options)
            return {user.id: user.name for user in all_users}


def process_tableau_info(workbooks, views, users):
    for book in workbooks:
        if book['product_id'] in views:
            book['product_url'] = book['product_url'].replace('product_view', views[book['product_id']]['url'])
            book['views'] = views[book['product_id']]['total']
        else:
            book['product_url'] = book['product_url'].replace('product_view', book['content_url'])

        if book['owner_id'] in users:
            book['owner_user'] = users[book['owner_id']]
        else:
            book['owner_user'] = 'tableau_server'
    return workbooks


def get_bcbsnc_user(alteryx_owner, tableau_owner):
    if alteryx_owner:
        email = alteryx_owner['email']
        user_filter = "(&(objectCategory=person)(objectClass=user)(mail=" + email + "))"
    else:
        username = tableau_owner
        user_filter = "(&(objectCategory=person)(objectClass=user)(uid=" + username + "))"
    base_dn = 'dc=bcbsnc,dc=com'
    ldap_server = AUTH_LDAP_SERVER_URI.replace('ldap://', '')
    server = Server(ldap_server, port=636, use_ssl=True)
    connect = Connection(server, user=AUTH_LDAP_BIND_DN, password=AUTH_LDAP_BIND_PASSWORD)
    connect.bind()
    attributes = ["cn", "sn", "givenname", "displayname", "telephonenumber", "mail", "manager", "title", "employeenumber"]
    result = connect.search(search_base=base_dn, search_filter=user_filter, search_scope=SUBTREE, attributes=attributes)

    if result:
        user_info = connect.response[0]['attributes']
        connect.unbind()
        bcbsnc_user = User.objects.filter(username=user_info['cn'])
        user_name = user_info['cn']
        first_name = user_info['givenName']
        last_name = user_info['sn']
        user_email = user_info['mail']
        full_name = user_info['displayName']
        user_title = user_info['title']
        employee_number = user_info['employeeNumber']
        if not bcbsnc_user.exists():
            bcbsnc_user = User.objects.create_user(username=user_name, email=user_email, first_name=first_name, last_name=last_name)
        else:
            bcbsnc_user = bcbsnc_user.first()
            bcbsnc_user.email = user_email
            bcbsnc_user.first_name = first_name
            bcbsnc_user.last_name = last_name
            bcbsnc_user.save()
        user_profile = bcbsnc_user.profile
        user_profile.employee_number = employee_number
        user_profile.title = user_title
        user_profile.display_name = full_name
        user_profile.save()

        return user_profile
    else:
        connect.unbind()
        user_name = 'alteryx_server' if alteryx_owner else 'tableau_server'
        user = User.objects.filter(username=user_name)
        if not user.exists():
            user = User.objects.create_user(username=user_name, email=user_name + "@bcbsnc.com")
            return user.profile
        return user.first().profile


def get_alteryx_studio(studio_id, studio_name):
    studio = AlteryxStudio.objects.filter(name=studio_name, studio_id=studio_id)
    if studio_name not in {'Operational Informatics', 'Marketing Analytics', 'Enterprise Analytics'}:
        print(studio_name)
    if studio.exists():
        alteryx_studio = studio.first()
        if alteryx_studio.name != studio_name:
            alteryx_studio.name = studio_name
            alteryx_studio.save()
        return alteryx_studio
    else:
        alteryx_studio = AlteryxStudio.objects.create(studio_id=studio_id, name=studio_name)
        return alteryx_studio


def get_tableau_server(server_url):
    tableau_server = server_url.split('//')[1].split('.')[0]
    server = TableauServer.objects.filter(code=tableau_server)
    if server.exists():
        return server.first()
    else:
        server = TableauServer.objects.create(name=tableau_server.upper(), description=server_url, code=tableau_server)
        return server


def get_tableau_site(tableau_site):
    site = TableauSite.objects.filter(code=tableau_site)
    if site.exists():
        return site.first()
    else:
        site = TableauSite.objects.create(name=tableau_site, description=tableau_site, code=tableau_site)
        return site


def update_tableau_workbooks(workbooks, tableau_server, tableau_site):
    server = get_tableau_server(tableau_server)
    site = get_tableau_site(tableau_site)
    for book in workbooks:
        owner_user = get_bcbsnc_user('', book['owner_user'])
        tableau_prod = AssetCatalog.objects.filter(asset_id=book['product_id'], asset_type__name__icontains='Tableau')
        if tableau_prod.exists():
            tableau_prod = tableau_prod.first()
            tableau_prod.name = book['product_name']
            tableau_prod.created_at = book['create_at']
            tableau_prod.modified_at = book['updated_at']
            tableau_prod.project_name = book['project_name']
            tableau_prod.business_owner = owner_user
            tableau_prod.asset_developer = owner_user
            tableau_prod.use_count = book['views']
            tableau_prod.asset_url = book['product_url']
            tableau_prod.image_url = book['project_image']
            tableau_prod.asset_server = server
            tableau_prod.asset_site = site
            tableau_prod.save()
        else:
            asset_type = AssetType.objects.filter(name__icontains='Tableau').first()
            name = book['product_name']
            asset_id = book['product_id']
            created_at = book['create_at']
            modified_at = book['updated_at']
            project_name = book['project_name']
            business_owner = owner_user
            developer = owner_user
            use_count = book['views']
            asset_url = book['product_url']
            image_url = book['project_image']
            tableau_prod = AssetCatalog.objects.create(name=name, asset_id=asset_id, asset_type=asset_type,
                                                       created_at=created_at, modified_at=modified_at,
                                                       project_name=project_name, business_owner=business_owner,
                                                       use_count=use_count, asset_url=asset_url, image_url=image_url,
                                                       asset_developer=developer, asset_site=site, asset_server=server)


def get_tableau_workbooks(tableau_location, tableau_site, tableau_username, tableau_password):
    tableau_api = TableauAPI(tableau_location, tableau_username, tableau_password, site_id=tableau_site)
    workbooks, site_id, total_item = tableau_api.get_workbooks_tableau()

    if len(workbooks) > 0:
        views = tableau_api.get_tableau_views()
        users = tableau_api.get_tableau_users()
        tableau_prod = process_tableau_info(workbooks, views, users)
        update_tableau_workbooks(tableau_prod, tableau_location, tableau_site)


def import_tableau():
    # There isn't any workbook in CM site for Production Server and give error for Development Server
    # https: // tableau.github.io / server - client - python / docs / page - through - results
#    tableau_sites = ["SalesMktgAnalytics", "EntAnalytics", "MedExp", "CM"]
    tableau_sites = ["SalesMktgAnalytics", "CallCenter", "CM", "ClaimsOps", "CommandCenter", "EntAnalytics", "MedExp", "NM", "pdmops", "QMO", "SIU"]
    tableau_servers = ["http://gviz.bcbsnc.com"]
    tableau_options = [(server, site) for server in tableau_servers for site in tableau_sites]
    for options in tableau_options:
        get_tableau_workbooks(options[0], options[1], TABLEAU_USER, TABLEAU_PASSWORD)


def process_alteryx(subscription):
    exclusions = {'David.Angevine', 'Lili.Dong', 'Todd.Howell', 'Taylor.Cox', 'Krishna.Parikh', 'Kiran.Kumar',
                  'Eshwar.Singareddy', 'Deepak.Venkatesh', 'Sigen.Agsebagil', 'Shane.Chang', 'Charley.Naney',
                  'Erik.Jensen', 'Michael.Hieronymus', 'Rajasekhar.Tumu', 'Chinmayee.Nayak'}
    url = "http://alteryx.bcbsnc.com/gallery/#!app/alteryx_name/alteryx_id"
    studio = set([workflow['subscriptionName']] for workflow in subscription)
    for workflow in subscription:
        if workflow['subscriptionName'] not in exclusions:
            owner_user = get_bcbsnc_user(workflow['publishedVersionOwner'], '')
            alteryx_prod = AssetCatalog.objects.filter(asset_id=workflow['id'], asset_type__name__icontains='Alteryx')
            studio = get_alteryx_studio(workflow['subscriptionId'], workflow['subscriptionName'])
            if alteryx_prod.exists():
                alteryx_prod = alteryx_prod.first()
                alteryx_prod.name = workflow['metaInfo']['name']
                alteryx_prod.created_at = datetime.fromtimestamp(int(re.split('\(|\)', workflow['uploadDate'])[1][:10])).date()
                alteryx_prod.business_owner = owner_user
                alteryx_prod.asset_developer = owner_user
                alteryx_prod.use_count = workflow['runCount']
                alteryx_prod.asset_url = url.replace('alteryx_name', workflow['metaInfo']['name']).replace('alteryx_id', workflow['id'])
                alteryx_prod.image_url = ''
                alteryx_prod.asset_studio = studio
                alteryx_prod.save()
            else:
                asset_type = AssetType.objects.filter(name__icontains='Alteryx').first()
                name = workflow['metaInfo']['name']
                description = workflow['metaInfo']['description']
                asset_id = workflow['id']
                content_type = 'Alteryx Workflow' if workflow['packageType'] else 'Alteryx App'
                created_at = datetime.fromtimestamp(int(re.split('\(|\)', workflow['uploadDate'])[1][:10])).date()
                project_name = ''
                business_owner = owner_user
                developer = owner_user
                use_count = workflow['runCount']
                asset_url = url.replace('alteryx_name', workflow['metaInfo']['name']).replace('alteryx_id', workflow['id'])
                image_url = ''
                alteryx_prod = AssetCatalog.objects.create(name=name, asset_id=asset_id, asset_type=asset_type,
                                                           created_at=created_at, project_name=project_name,
                                                           business_owner=business_owner, description=description,
                                                           use_count=use_count, asset_url=asset_url, image_url=image_url,
                                                           content_type=content_type, asset_studio=studio,
                                                           asset_developer=developer)


def import_alteryx():
    gallery_url = "http://alteryx.bcbsnc.com/gallery/api/v1"
    studios = [
        # {'key': "8D2DB82B57695AE7e5aeb8e20875bacc46f757e591cc8774ac5390d",
        #  'secret': "04d1a6fa187928bf5af906f336ee3c43db8d8e517b144e14784eff1e52f01d66"},
        {'key': ALTERYX_KEY,
         'secret': ALTERYX_SECRET}
    ]
    for studio in studios:
        alteryx = Gallery(gallery_url, studio['key'], studio['secret'])
        alteryx_subs = alteryx.subscription()
        process_alteryx(json.loads(alteryx_subs))


def set_asset_type():
    product_type = AssetType.objects.filter(name="Tableau Dashboard").first()
    products = AssetCatalog.objects.all()
    for product in products:
        product.asset_type = product_type
        product.save()


def main():
    try:
#        get_bcbsnc_user({'email': "Yoelvis.Oses@bcbsnc.com"}, '')
        import_tableau()
#        import_alteryx()
#        set_asset_type()
    except Exception as err:
        y = str(err)


if __name__ == "__main__":
    main()