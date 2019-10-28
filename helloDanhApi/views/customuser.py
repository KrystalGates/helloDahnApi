"""View module for handling requests about user"""
from django.http import HttpResponseServerError
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from helloDanhApi.models import CustomUser


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for custom user

    Arguments:
        serializers
    """
    class Meta:
        model = CustomUser
        url = serializers.HyperlinkedIdentityField(
            view_name='custom_user',
            lookup_field='id'
        )
        fields = ('id', 'url', 'address', 'phone_number', 'user', 'user_id')
        depth = 1


class CustomUsers(ViewSet):
    """Custom user for helloDanh"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for a user

        Returns:
            Response -- JSON serialized user instance
        """
        try:
            user = CustomUser.objects.get(pk=pk)
            serializer = CustomUserSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for an user

        Returns:
            Response -- Empty body with 204 status code
        """
        user = CustomUser.objects.get(pk=pk)
        user.alert = request.data["alert"]
        user.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for an user

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            user = CustomUser.objects.get(pk=pk)
            user.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except CustomUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['get'], detail=False)
    def currentuser(self, request):

        try:
            custom_user = CustomUser.objects.get(user=request.auth.user)
        except CustomUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomUserSerializer(custom_user, context={'request': request})
        return Response(serializer.data)
