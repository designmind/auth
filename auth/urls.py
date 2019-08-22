"""auth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from fb_auth.views import *
import re


# http: // localhost: 8000 / read/  # access_token=EAAjWs6ZAQEZCwBAIrYXlIfLbV3CjIcYQPsGTEgJcvK88OVHeTZCrZBzpD4Xgtvn68YLubowU7lGlT9pPNb3pxclri7oM7ewqhZAJ0ZApjWr4mLUpvhi7dvVDZCnYINRPyEaM6RO1NN4A8rQnwwEqDaxLZAS2HbwoHtkXw5ZCl8CtRIgVEwZCiwse0Ubu6KzkZCgcMYZD
# &data_access_expiration_time = 1569263830 & expires_in = 4969 & reauthorize_required_in = 7775999 & state = %7Bst % 3Dpewpew % 2C + ds % 3D + pupu % 7D

urlpatterns = [
    path('admin/', admin.site.urls),
    path('read/', auth),
    # path('', home, name="home"),
    path('gA/', gA_auth),
    path('login/upload/', upload,  name="upload"),
    path('login/download', download),
    path("login/", login, name="login"),
    path("read/scrape", scrape)
    # re_path('read/?', auth)
    # path('read/#<int:number>/', auth),
    # re_path(r'^read/#access_token=*.&/$', test)
    # re_path(r'^read/?P<slug>(?:#access_token=([0-9A-Fa-f])/)?$', test)
    # re_path(r'^read/(?P<slug>[0-9A-Fa-f])', test).
    # re_path(r'read/(?P<slug>#access_token=.*&)/$', test)
    # re_path('read/', test)
]

#
# read/?code=AQDWGyXsEopslWzmtfh4n8YmEKmkgd6UdB2U0tt9yveESmfxxrbdlwBTrSnVY8Wydb9tUbVIbTt9tt9Wri93pzY2JxfMX6XASoWEwvciI-UiP3BaN-h0kkiHv16i9RcMfSTRgV1EvQMUT9Ksgx2CjyaVbrhYUM6N7A2wJu72ZcALIVuUoqEryegZDvSWg8j5axXV2k23idv1J-IIftnhC9B80OfwPyun-ZBwFS7oLAEHh6ccDvG0W95KF1DkrmRd4H902bGOY6GQ7tL2wPmY_pBYGrdYXEhJy-9vPmTAzoz3WLkK_RzoB3nHi_9cwz3OtRe5Ja2COs0T8Yt5n2OU9xCz&state=%7Bst%3Dpewpew%2C+ds%3D+pupu%7D#_=_


# ^ articles/  # access_token=(?P<slug>[0-9A-Fa-f]+)


# local_t = "http://localhost:8000/read/#access_token=EAAjWs6ZAQEZCwBAIrYXlIfLbV3CjIcYQPsGTEgJcvK88OVHeTZCrZBzpD4Xgtvn68YLubowU7lGlT9pPNb3pxclri7oM7ewqhZAJ0ZApjWr4mLUpvhi7dvVDZCnYINRPyEaM6RO1NN4A8rQnwwEqDaxLZAS2HbwoHtkXw5ZCl8CtRIgVEwZCiwse0Ubu6KzkZCgcMYZD&data_access_expiration_time=1569263830&expires_in=4969&reauthorize_required_in=7775999&state=%7Bst%3Dpewpew%2C+ds%3D+pupu%7D"
# lt = "read/#access_token=EAAjWs6ZAQEZCwBAIrYXlIfLbV3CjIcYQPsGTEgJcvK88OVHeTZCrZBzpD4Xgtvn68YLubowU7lGlT9pPNb3pxclri7oM7ewqhZAJ0ZApjWr4mLUpvhi7dvVDZCnYINRPyEaM6RO1NN4A8rQnwwEqDaxLZAS2HbwoHtkXw5ZCl8CtRIgVEwZCiwse0Ubu6KzkZCgcMYZD&data_access_expiration_time=1569263830&expires_in=4969&reauthorize_required_in=7775999&state=%7Bst%3Dpewpew%2C+ds%3D+pupu%7D"
#
#
# re.search('read/#access_token=*.&', lt)
# # 1569263830&expires_in=4969&reauthorize_required_in=7775999&state=%7Bst%3Dpewpew%2C+ds%3D+pupu%7D
#
# read/  # /access_token=.*&data_access_expiration_time=.*&expires_in=.*&reauthorize_required_in=.*&state=.*&
