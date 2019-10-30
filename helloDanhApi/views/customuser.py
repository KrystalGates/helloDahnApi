"""View module for handling requests about user"""
from django.http import HttpResponseServerError
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from helloDanhApi.models import CustomUser
from helloDanhApi.models import Contact


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
        fields = ('id', 'url', 'address', 'phone_number', 'user', 'contacts')
        depth = 2


class CustomUsers(ViewSet):
    """Custom user for helloDanh"""

    def update(self, request, pk=None):
        """Handle PUT requests for an user

        Returns:
            Response -- Empty body with 204 status code
        """
        custom_user = CustomUser.objects.get(pk=pk)
        custom_user.address = request.data["address"]
        custom_user.phone_number = request.data["phone_number"]

        user = User.objects.get(pk=pk)
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.email = request.data["email"]
        user.username = request.data["email"]

        user.save()
        custom_user.user = user
        custom_user.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def currentuser(self, request):

        try:
            custom_user = CustomUser.objects.get(user=request.auth.user)
        except CustomUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomUserSerializer(custom_user, context={'request': request})
        return Response(serializer.data)
