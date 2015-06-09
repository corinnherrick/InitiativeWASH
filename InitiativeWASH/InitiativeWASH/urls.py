from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
# from rtwilio.views import TwilioBackendView
from rapidsms_telerivet.views import TelerivetBackendView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    # RapidSMS core URLs
    (r'^accounts/', include('rapidsms.urls.login_logout')),
    url(r'^$', 'rapidsms.views.dashboard', name='rapidsms-dashboard'),
    # RapidSMS contrib app URLs
    (r'^httptester/', include('rapidsms.contrib.httptester.urls')),
    #(r'^locations/', include('rapidsms.contrib.locations.urls')),
    (r'^messagelog/', include('rapidsms.contrib.messagelog.urls')),
    (r'^messaging/', include('rapidsms.contrib.messaging.urls')),
    (r'^registration/', include('rapidsms.contrib.registration.urls')),

    #TELERIVET
    (r'^telerivet/', TelerivetBackendView.as_view(backend_name='telerivet')),

    #TWILIO
    # url(r"^backend/twilio/$", TwilioBackendView.as_view(backend_name="twilio-backend")),
    # url(r'^backend/twilio/status-callback/$', status_callback, name='twilio-status-callback'),

    #TROPO
    # url(r'^tropo/', message_received, kwargs={'backend_name': 'my-tropo-backend'}, name='tropo'),

    # Third party URLs
    (r'^selectable/', include('selectable.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
