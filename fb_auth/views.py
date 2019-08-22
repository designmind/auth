from glob import glob
from django.http import HttpResponse
import sys
import os
from .forms import UploadFileForm
import openpyxl
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import render
import requests
import pypyodbc
import urllib.request
import ast
import urllib.request as urllib2
from urllib.parse import urlparse
from urllib.parse import parse_qs
import urllib.parse
from urllib import parse
from django.http import HttpResponse, HttpResponseRedirect
from cryptography.fernet import Fernet
from fb_auth.HelloAnalytics import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import pandas as pd
import datetime
import os.path
from ftplib import FTP
from wsgiref.util import FileWrapper
import mimetypes
from django.utils.encoding import smart_str
from io import BytesIO
import zipfile

myFacebookID = '100002345472592'
CLIENT_SECRET = '4d15d66d150b8bebb07df3418e44bb2c'
appID = '2487866891441148'

dir_path = os.path.dirname(os.path.realpath(__file__))
fb_path = os.path.join(dir_path, 'facebook-result.csv')
ga_path = os.path.join(dir_path, 'gA-details.json')
pub_pages_dict = {}


def print_hello():
    return "Hello world"


def home(request):
    return render(request, 'index.htm', {'what': 'Django File Upload'})

# Function for getting facebook page data


def scrape(request):
    obj1 = request.get_full_path()
    name = parse.parse_qs(parse.urlsplit(obj1).query)["q"][0]
    current_page_access_token = pub_pages_dict[name]
    fooo = "https://graph.facebook.com/v4.0/me?access_token=" + current_page_access_token
    current_id = requests.get(fooo).json()["id"]

    me_posts = 'https://graph.facebook.com/v4.0/' + current_id + \
        '/posts?fields=message,likes.limit(1).summary(true),comments.limit(0).summary(true)' + \
        '&access_token=' + current_page_access_token
    rPosts = requests.get(me_posts).json()

    post_info = {}
    for post in rPosts.get('data'):
        total_likes = post.get('likes').get('summary').get('total_count')
        comment_count = post.get('comments').get('summary').get('total_count')
        post_info[post.get('id')] = {'content': post.get(
            'message'), 'total_likes': total_likes, 'comment_count': comment_count}

    post_info_data_frame = pd.DataFrame.from_dict(post_info, orient='index')
    post_info_data_frame[datetime.datetime.today().strftime(
        '%Y-%m-%d')] = post_info_data_frame["total_likes"].map(str) + " / " + post_info_data_frame["comment_count"].map(str)
    post_info_data_frame.drop(
        {'total_likes', 'comment_count'}, axis=1, inplace=True)
    post_info_data_frame.index.name = "Post ID"
    metrics_csv_file_path = os.path.join(
        settings.MEDIA_ROOT, name.replace(" ", "-") + '-metrics.csv')

    df = post_info_data_frame

    if (os.path.exists(metrics_csv_file_path)):
        olddf = pd.read_csv(
            metrics_csv_file_path)
        olddf.drop(olddf.columns[olddf.columns.str.contains(
            'unnamed', case=False)], axis=1, inplace=True)
        if olddf.columns[-1] != datetime.datetime.today().strftime('%Y-%m-%d'):
            result = pd.merge(olddf, df, how='outer',
                              on=['Post ID', 'content'])
            result.drop(df.columns[df.columns.str.contains(
                'unnamed', case=False)], axis=1, inplace=True)
            result.to_csv(metrics_csv_file_path)
            output = result
        else:
            df.to_csv(metrics_csv_file_path)
            output = df
    return render(request, 'base.html', {'output': output})

# displays the pages that the user owns


def auth(request):
    url = "https://www.facebook.com/v3.2/dialog/oauth?"
    FBparams = {'client_id': appID, 'redirect_uri': 'https://ec2-18-219-4-199.us-east-2.compute.amazonaws.com/read',
                'state': '{st=pewpew, ds= pupu}', 'response_type': 'code'}
    r = requests.get(url, data=FBparams)
    putInBrowser = r.url + "?" + r.request.body
    obj1 = request.get_full_path()
    code = parse_qs(obj1)["/read/?code"][0]

    info_dict = {'client_id': appID, 'client_secret': CLIENT_SECRET,
                 'redirect_uri': 'https://ec2-18-219-4-199.us-east-2.compute.amazonaws.com/read', 'code': code}
    AT_url = 'https://graph.facebook.com/v3.2/oauth/access_token'

    token_raw = requests.get(AT_url, info_dict)
    ACCESS_TOKEN = eval(token_raw.text)["access_token"]

    urlLongLived = "https://graph.facebook.com/v3.2/oauth/access_token?"
    FBparamsLongLived = {'redirect_uri': '"https://ec2-18-219-4-199.us-east-2.compute.amazonaws.com/read"', 'grant_type': 'fb_exchange_token', 'client_id': appID, 'client_secret': CLIENT_SECRET,  'fb_exchange_token':
                         ACCESS_TOKEN}
    rLongLived = requests.get(urlLongLived, data=FBparamsLongLived)
    LongLivedUrl = rLongLived.url + "?" + rLongLived.request.body
    LongLivedToken = eval(requests.get(LongLivedUrl).text)["access_token"]

    me_endpoint = 'https://graph.facebook.com/v2.12/me/accounts'
    pub_page_request = requests.get(
        me_endpoint, {'access_token': LongLivedToken})
    pub_pages = eval(pub_page_request.text.replace('false', 'False'))['data']
    for x in pub_pages:
        pub_pages_dict[x['name']] = x['access_token']

    names_of_pages = list(pub_pages_dict)
    button_page = {}

    for y in range(len(names_of_pages)):
        page_numner = "page" + str(y)
        button_page[page_numner] = names_of_pages[y]
    return render(request, 'page_selection.html', button_page)


def login(request):
    return render(request, 'login.html')


def handle_uploaded_file(f):
    with open(ga_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def absolute_file_paths(directory):
    return glob(os.path.join(directory, "**"))

# takes all files in the media folder and zips them up


def download(request):
    # Files (local path) to put in the .zip
    # FIXME: Change this (get paths from DB etc)
    # filenames = ["/home/ubuntu/auth/media/Van Gogh Gucci Gang-facebook-result.csv",
    #              "/home/ubuntu/auth/media/Church of the Flying Spaghetti Monster-facebook-result.csv"]
    filenames = absolute_file_paths(settings.MEDIA_ROOT)
    # Folder name in ZIP archive which contains the above files
    # E.g [thearchive.zip]/somefiles/file2.txt
    # FIXME: Set this to something better
    zip_subdir = "data_files_" + datetime.datetime.today().strftime('%Y-%m-%d')
    zip_filename = "%s.zip" % zip_subdir

    # Open StringIO to grab in-memory ZIP contents
    s = BytesIO()

    # The zip compressor
    zf = zipfile.ZipFile(s, "w")

    for fpath in filenames:
        # Calculate path for file in zip
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)

        # Add file, at correct path
        zf.write(fpath, zip_path)

    # Must close zip for all contents to be written
    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = HttpResponse(
        s.getvalue(), content_type="application/x-zip-compressed")
    # ..and correct content-disposition
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    return resp

# upload a json containing the google analytics credentials of the user


def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/gA')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def getURLS(request):

    obj = request.get_full_path()

    return render(request, 'base.html', {'output': obj})

# saves the searches that were made to get to user's website


def gA_auth(request):

    output = main(ga_path)
    name = output.get('profileInfo').get('profileName')
    rows = output.get('rows')
    df = pd.DataFrame(rows)
    df.columns = ["Search Engine", "Search term",
                  datetime.datetime.today().strftime('%Y-%m-%d')]

    csv_file_path = os.path.join(settings.MEDIA_ROOT, 'ga-result.csv')
    if (os.path.exists(csv_file_path) and os.stat(csv_file_path).st_size != 0):
        old_data = pd.read_csv(
            csv_file_path)
        most_recent_update = old_data.columns[len(old_data.columns) - 1]
        old_data.drop(old_data.columns[old_data.columns.str.contains(
            'unnamed', case=False)], axis=1, inplace=True)
        if (most_recent_update != datetime.datetime.today().strftime('%Y-%m-%d')):
            result = pd.merge(old_data, df, how='outer', on=[
                              'Search Engine', 'Search term'])
            result.to_csv(
                csv_file_path)

        output = old_data
    else:
        df.to_csv(csv_file_path)
        output = df
    return render(request, 'base.html', {'output': output})
