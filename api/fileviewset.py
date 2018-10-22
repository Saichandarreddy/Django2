from api.headers import *
from api.models import *
from rest_framework.decorators import detail_route, list_route
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ('title','record','uploaded_at')

@api_view(['get'])
#@permission_classes((IsAuthenticated,))
def fileList(request):
    try:
        queryset = Records.objects.all()
        images = RecordSerializer(queryset.data,status=status.HTTP_200_OK)
    except Exception as e :
        return Response({'error':{'code':5000,'message':'Generic System Failure-{0}'.format(e)}},status=status.HTTP_200_OK)
    
@api_view(['post'])
#@permission_classes((IsAuthenticated,))
def fileUpload(request):
    try:
        with transaction.atomic(savepoint=False):
            print(request.FILES.getlist('myfiles'))
            if request.method == 'POST' and request.FILES.getlist('myfiles'):
                for myfile in request.FILES.getlist('myfiles'):
                    #if Images.objects.filter(image= 'images/'+myfile.name.replace(' ','_')).exists():
                    #    return Response({'error':{'code':5000,'message':'Error-{0}'.format('File exists')}},status=status.HTTP_200_OK)
                    if 'type' in request.data and request.data['type'] == 'image':
                        imgobj = Images()
                        imgobj.image = myfile
                        imgobj.save()
                    else:
                        recobj = Records()
                        recobj.title = request.data['title']
                        recobj.record = myfile
                        recobj.save()
                return Response({'message':'Upload Success'},status=status.HTTP_200_OK)
            else:
                return Response({'error':{'code':5000,'message':'Error-{0}'.format('Invalid Request')}},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error':{'code':5000,'message':'Error-{0}'.format(e)}},status=status.HTTP_200_OK)
        
@api_view(['post'])
#@permission_classes((IsAuthenticated,))
def fileDelete(request):
    try:
        with transaction.atomic(savepoint=False):
            if request.method == 'POST' and request.data['id']:
                imgobj = Images.objects.filter(pk=request.data['id']).first()
                if imgobj is not None:
                    imgobj.delete()
                return Response({'message':'Deleted - {} '.format('Image deleted')},status=status.HTTP_200_OK)
            else:
                return Response({'error':{'code':5000,'message':'Error-{0}'.format('Invalid Request')}},status=status.HTTP_200_OK)
    except FileNotFoundError as e:
        return Response({'error':{'code':5000,'message':'Error-{0}'.format('File not found')}},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error':{'code':5000,'message':'Error-{0}'.format(e)}},status=status.HTTP_200_OK)
        
@api_view(['post'])
#@permission_classes((IsAuthenticated,))
def fileUpdate(request):
    try:
        with transaction.atomic(savepoint=False):
            if request.method == 'POST' and request.data['date'] and request.data['myfile']:
                imgobj = Images.objects.filter(uploaded_at__icontains = request.data['date']).first()
                print(request.data['date'],type(request.data['date']))
                if imgobj is not None:
                    os.remove(os.path.join(settings.MEDIA_ROOT, imgobj.image.name))
                    imgobj.image = request.FILES['myfile']
                    imgobj.save()
                return Response({'message':'Deleted - {} '.format('Image Updated')},status=status.HTTP_200_OK)
            else:
                return Response({'error':{'code':5000,'message':'Error-{0}'.format('Invalid Request')}},status=status.HTTP_200_OK)
    except FileNotFoundError as e:
        return Response({'error':{'code':5000,'message':'Error-{0}'.format('File not found')}},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error':{'code':5000,'message':'Error-{0}'.format(e)}},status=status.HTTP_200_OK)

@api_view(['post'])
#@permission_classes((IsAuthenticated,))
def pdfUpload(request):
    try:
        with transaction.atomic(savepoint=False):
            if request.method == 'POST' and request.FILES['myfile']:
                myfile = request.FILES['myfile']
                try:
                    path = settings.MEDIA_ROOT+'/Pdfs/'+myfile.name
                    os.remove(path)
                    print('deleted -',myfile.name)
                    message = 'Updated'
                except FileNotFoundError as e:
                    message = 'Created'
                    pass
                fs = FileSystemStorage(location=settings.MEDIA_ROOT+'/Pdfs/')
                filename = fs.save(myfile.name, myfile)
                return Response({'message':'{}-{}'.format(message,filename)},status=status.HTTP_200_OK)
            else:
                return Response({'error':{'code':5000,'message':'Error-{0}'.format('Invalid Request')}},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error':{'code':5000,'message':'Error-{0}'.format(e)}},status=status.HTTP_200_OK)

