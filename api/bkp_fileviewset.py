from api.headers import *
from rest_framework.decorators import detail_route, list_route

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id','image','uploaded_at')

class ImageViewSet(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated,)
    queryset = Images.objects.all()
    serializer_class = ImageSerializer

    def list(self,request):
        try:
            images = ImageSerializer(self.queryset,many=True)
            return Response(images.data,status=status.HTTP_200_OK)
        except Exception as e :
            return Response({'error':{'code':5000,'message':'Generic System Failure-{0}'.format(e)}},status=status.HTTP_200_OK)
    
    @list_route(methods=['post'])
    def upload(self,request):
        try:
            with transaction.atomic(savepoint=False):
                if request.method == 'POST' and request.FILES['myfile']:
                    imgobj = Images()
                    imgobj.image = request.FILES['myfile']
                    imgobj.save()
                    return Response({'message':'Upload Success'},status=status.HTTP_200_OK)
                else:
                    return Response({'error':{'code':5000,'message':'Error-{0}'.format('Invalid Request')}},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':{'code':5000,'message':'Error-{0}'.format(e)}},status=status.HTTP_200_OK)
        
    @list_route(methods=['post'])
    def delete(self,request):
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
        
    @list_route(methods=['post'])
    def update(self,request):
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
