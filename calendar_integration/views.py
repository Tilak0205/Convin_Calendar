import os
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View
from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.discovery
from google_auth_oauthlib import flow as google_flow
from googleapiclient.discovery import build
from django.shortcuts import render
from google_auth_oauthlib.flow import Flow


class GoogleCalendarInitView(View):
    def get(self, request):
        flow = InstalledAppFlow.from_client_secrets_file(
            os.path.join(settings.BASE_DIR, 'calendar_integration/client_secrets.json'),
            scopes=['https://www.googleapis.com/auth/calendar.readonly',
            'https://www.googleapis.com/auth/calendar',
          'https://www.googleapis.com/auth/userinfo.email',
          'https://www.googleapis.com/auth/userinfo.profile',
          'openid'],
          redirect_uri=settings.GOOGLE_REDIRECT_URI
        )
        auth_url, _ = flow.authorization_url(prompt='consent')
        # return redirect(auth_url)
        return redirect(auth_url)

# class GoogleCalendarRedirectView(View):
#     def get(self, request):
#         code = request.GET.get('code')

#         flow = InstalledAppFlow.from_client_secrets_file(
#             os.path.join(settings.BASE_DIR, 'calendar_integration/client_secrets.json'),
#             scopes=['https://www.googleapis.com/auth/calendar.readonly',
#             'https://www.googleapis.com/auth/calendar',
#           'https://www.googleapis.com/auth/userinfo.email',
#           'https://www.googleapis.com/auth/userinfo.profile',
#           'openid'],
#         )
#         flow.redirect_uri = settings.GOOGLE_REDIRECT_URI

#         flow.fetch_token(code=code)

#         credentials = flow.credentials
#         service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)

#         events = service.events().list(calendarId='primary').execute()
#         # Handle events data as per your requirements

#         return HttpResponse('Calendar events retrieved successfully!')


class GoogleCalendarRedirectView(View):
    def get(self, request):
        code = request.GET.get('code')

        flow = Flow.from_client_secrets_file(
            os.path.join(settings.BASE_DIR, 'calendar_integration/client_secrets.json'),
            scopes=['https://www.googleapis.com/auth/calendar.readonly',
            'https://www.googleapis.com/auth/calendar',
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile',
            'openid'],
            redirect_uri=settings.GOOGLE_REDIRECT_URI
        )
        flow.fetch_token(code=code)

        credentials = flow.credentials
        service = build('calendar', 'v3', credentials=credentials)

        # Retrieve the calendar events
        events_result = service.events().list(calendarId='primary', maxResults=10).execute()
        events = events_result.get('items', [])

        # Print the events list
        for event in events:
            print(f"Event: {event['summary']}")
            print(f"Start: {event['start'].get('dateTime', event['start'].get('date'))}")
            print(f"End: {event['end'].get('dateTime', event['end'].get('date'))}")
            print('---')

        # You can render a template or return a response to the user
        # Example:
        return HttpResponse("Events printed successfully on the console!")
