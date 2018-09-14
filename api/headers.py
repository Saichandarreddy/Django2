from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework.decorators import (api_view, permission_classes,detail_route, list_route)
from django.contrib import auth
from rest_framework import (status,serializers,viewsets)
from rest_framework.response import Response
import django
from rest_framework.decorators import detail_route, list_route
from datetime import (datetime,timedelta)
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from api.models import *