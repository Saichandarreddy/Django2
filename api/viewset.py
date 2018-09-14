from api.headers import *
from api.serializers import UserSerializer

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id','name','mobile')

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

@permission_classes((IsAuthenticated, ))
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
            else:
                session = request.session.session_key
                request.session.set_expiry(60*30)
            resp={}
            resp["session_key"] = request.session
            resp["csrf"]= django.middleware.csrf.get_token(request)
            resp['message']='Login Successful'
            return Response(resp,status=status.HTTP_200_OK)
        else:
            return Response({'error':{'code':5000,'message':'Incorrect username/password'}},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error':{'code':5000,'message':'Error-{0}'.format(e)}},status=status.HTTP_200_OK)

@api_view(['get'])
def logout(request):
    try:
        auth.logout(request)
        response = HttpResponse()
        response.delete_cookie('sessionid')
        response.delete_cookie('csrftoken')
        return Response({'message':'Success'},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error':{'code':5000,'message':'Error-{0}'.format(e)}},status=status.HTTP_200_OK)

@permission_classes((IsAuthenticated, ))
@api_view(['post'])
def createuser(request):
    try:
        with transaction.atomic(savepoint=False):
            if request.method == 'POST':
                usrp = UserProfile()
                usrp.create(request.data)
                return Response({'message':'User created'},status=status.HTTP_200_OK)
            else:
                return Response({'error':{'code':5000,'message':'Error-{0}'.format('Invalid Request')}},status=status.HTTP_200_OK)
    except Django2Exception as e:
        print(e,'error')
        return Response({'error':{'code':5000,'message':'Error-{0}'.format(e)}},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error':{'code':5000,'message':'Error-{0}'.format(e)}},status=status.HTTP_200_OK)

@api_view(['get'])
def getUsers(request):
    try:
        queryset = UserProfile.objects.all()
        users = UserProfileSerializer(queryset,many=True)
        return Response(users.data,status=status.HTTP_200_OK)
    except DjangoException as e:
        return Response({'error':{'code':5000,'message':'Error-{0}'.format(e)}},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error':{'code':5000,'message':'Error-{0}'.format(e)}},status=status.HTTP_200_OK)