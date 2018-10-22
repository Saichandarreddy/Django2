from api.headers import *
from api.serializers import UserSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id','display_name','mobile')

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

@api_view(['post'])
def login(request):
    try:
        rd = request.data
        print(request)
        user = auth.authenticate(username=rd['username'],password=rd['password'])
        if user is not None:
            auth.login(request, user)
            if not request.session.session_key:
                session = request.session.create()
                session = request.session.session_key
            else:
                session = request.session.session_key
                request.session.set_expiry(60*30)
            resp={}
            resp["session_key"] = session
            resp["csrftoken"]= django.middleware.csrf.get_token(request)
            resp['message']='Login Successful'
            return Response(resp,status=status.HTTP_200_OK)
        else:
            return Response({'error':{'code':5000,'message':'Incorrect username/password'}},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error':{'code':5000,'message':'Error-{0}'.format(e)}},status=status.HTTP_200_OK)


@api_view(['get'])
@csrf_exempt
def logout(request):
    try:
        auth.logout(request)
        response = HttpResponse()
        response.delete_cookie('sessionid')
        response.delete_cookie('csrftoken')
        return Response({'message':'Success'},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error':{'code':5000,'message':'Error-{0}'.format(e)}},status=status.HTTP_200_OK)


@api_view(['post'])
def createuser(request):
    try:
        with transaction.atomic(savepoint=False):
            if request.method == 'POST':
                usrp = UserProfile()
                usrp.create(request.data)
                return Response({'message':'User created'},status=status.HTTP_200_OK)
            else:
                return Response({'error':{'code':5000,'message':'Error -> {0}'.format('Invalid Request')}},status=status.HTTP_200_OK)
    except Django2Exception as e:
        return Response({'error':{'code':e.code,'message':'Error -> {0}'.format(e.message)}},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error':{'code':5000,'message':'Error -> {0}'.format(e)}},status=status.HTTP_200_OK)

@api_view(['get'])
@permission_classes((IsAuthenticated,))
def getUsers(request):
    try:
        queryset = UserProfile.objects.all()
        users = UserProfileSerializer(queryset,many=True)
        return Response(users.data,status=status.HTTP_200_OK)
    except DjangoException as e:
        return Response({'error':{'code':5000,'message':'Error-{0}'.format(e)}},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error':{'code':5000,'message':'Error-{0}'.format(e)}},status=status.HTTP_200_OK)