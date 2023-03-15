from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Publisher
from .serializers import PublisherSerializer

class PublisherAPIView(APIView):
    def get(self, request):
        publishers = Publisher.objects.all()
        serializer = PublisherSerializer(publishers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PublisherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        publisher = Publisher.objects.get(pk=pk)
        publisher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
