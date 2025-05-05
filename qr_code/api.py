from django.http import HttpResponse
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import QRCode, QRCodeType
from .serializers import QRCodeSerializer,QRCodeTypeSerializer
import io
from .make_qr_factory import generate_qr_code

class QRCodeTypeViewSet(viewsets.ModelViewSet):
    permissions_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = QRCodeTypeSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return QRCodeType.objects.all()
        else:
            # Handle unauthenticated users
            return QRCodeType.objects.none()
        
class QRCodeViewSet(viewsets.ModelViewSet):
    permissions_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = QRCodeSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.request.user.qr_codes.all()
        else:
            return QRCode.objects.none()

    @staticmethod
    def send_file(buffer, filename, content_type="image/png"):
        buffer.seek(0)
        response = HttpResponse(buffer.read(), content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename={filename}'
        response['Content-Length'] = buffer.getbuffer().nbytes
        buffer.close()
        return response

    def create(self, request, *args, **kwargs):
        print("creating")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(owner=self.request.user)

            if not instance.qr_type:
                return Response({'error': 'QR Code Type is required.'}, status=status.HTTP_400_BAD_REQUEST)

            config = {
                "border": instance.border,
                "scale": instance.scale,
                "unit": instance.unit,
                "dark": instance.dark,
                "light": instance.light,
                "data_dark": instance.data_dark,
                "data_light": instance.data_light,
            }

            try:
                qr_type = QRCodeType.objects.get(pk=instance.qr_type.id)
            except QRCodeType.DoesNotExist:
                return Response({'error': 'Invalid QR Code Type.'}, status=status.HTTP_400_BAD_REQUEST)

            if instance.information and qr_type:
                buffer = generate_qr_code(qr_type.type_name, instance.information, config)
                return self.send_file(buffer, filename=f"{instance.name}.png", content_type="image/png")

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['GET'])
    def generate_qr(self, request, pk=None):
        try:
            instance = QRCode.objects.get(pk=pk)
        except QRCode.DoesNotExist:
            return Response({'error': 'QRCode not found'}, status=status.HTTP_404_NOT_FOUND)
        config = {
                "border" : instance.border,
                "scale" : instance.scale,
                "unit" : instance.unit,
                "dark" : instance.dark,
                "light" : instance.light,
                "data_dark" : instance.data_dark,
                "data_light" : instance.data_light,
            }
        
        type = QRCodeType.objects.get(pk=instance.qr_type.id)
        if instance.information != {} and type:
            buffer = generate_qr_code(type.type_name,instance.information, config)
            return self.send_file(buffer, filename=f"{instance.name}.png")
        
        return Response({'error': 'Information not available for this QRCode'}, status=status.HTTP_400_BAD_REQUEST)