# Universal Subtitles, universalsubtitles.org
# 
# Copyright (C) 2010 Participatory Culture Foundation
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see 
# http://www.gnu.org/licenses/agpl-3.0.html.

from django.contrib.sites.models import Site
from django.conf import settings
from utils.translation import get_user_languages_from_request

def run_locally(request):
    return {"RUN_LOCALLY": getattr(settings, "RUN_LOCALLY", False)} 

def current_site(request):
    try:
        return { 'current_site': Site.objects.get_current() }
    except Site.DoesNotExist:
        return { 'current_site': '' }
    
def current_commit(request):
    return {'LAST_COMMIT_GUID': settings.LAST_COMMIT_GUID}

def custom(request):
    return {
        'GOOGLE_ANALYTICS_NUMBER': settings.GOOGLE_ANALYTICS_NUMBER,
        'MIXPANEL_TOKEN': settings.MIXPANEL_TOKEN,
        'DEBUG': settings.DEBUG
    }

def user_languages(request):
    return {
        'USER_LANGUAGES': get_user_languages_from_request(request)
    }
