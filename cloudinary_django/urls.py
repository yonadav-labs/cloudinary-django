from django.conf.urls import patterns, url, include

from django.contrib import admin
admin.autodiscover()

import feed.views as feed

urlpatterns = patterns('',
    # URL for listing all images:
    url(r'^$', feed.upload),
    # URL for uploading an image
    url(r'^upload$', feed.upload),
    # The direct upload functionality reports to this URL when an image is uploaded.
    url(r'^upload/complete$', feed.direct_upload_complete),
    # Delete canceled image
    url(r'^delete/(?P<public_id>\w+)/$', feed.delete_image),
    # Add the admin functionality:
    (r'^admin/', include(admin.site.urls)),
)
