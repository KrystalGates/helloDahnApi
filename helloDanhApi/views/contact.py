"""View module for handling requests about contacts"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from helloDanhApi.models import Contact, CustomUser


class ContactSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for contacts

    Arguments:
        serializers
    """
    class Meta:
        model = Contact
        url = serializers.HyperlinkedIdentityField(
            view_name='contact',
            lookup_field='id'
        )
        fields = ('id', 'url', 'first_name', 'last_name', 'email', 'address', 'phone_number', 'user')
        depth = 2


class Contacts(ViewSet):
    """Contacts for helloDanh"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Contact instance
        """
        new_contact = Contact()
        new_contact.first_name = request.data["first_name"]
        new_contact.last_name = request.data["last_name"]
        new_contact.address = request.data["address"]
        new_contact.email = request.data["email"]
        new_contact.phone_number = request.data["phone_number"]
        custom_user = CustomUser.objects.get(user=request.auth.user)
        new_contact.user = custom_user
        new_contact.save()

        serializer = ContactSerializer(new_contact, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single contact

        Returns:
            Response -- JSON serialized contact instance
        """
        try:
            contact = Contact.objects.get(pk=pk)
            serializer = ContactSerializer(contact, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a contact

        Returns:
            Response -- Empty body with 204 status code
        """
        contact = Contact.objects.get(pk=pk)
        contact.first_name = request.data["first_name"]
        contact.last_name = request.data["last_name"]
        contact.email = request.data["email"]
        contact.address = request.data["address"]
        contact.phone_number = request.data["phone_number"]

        contact.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a contact

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            contact = Contact.objects.get(pk=pk)
            contact.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Contact.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def list(self, request):
        """Handle GET requests to contact resource

        Returns:
            Response -- JSON serialized list of contacts
        """
        try:
            user = CustomUser.objects.get(user=request.auth.user)
            contacts_of_user = Contact.objects.filter(user=user)

        except Contact.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        serializer = ContactSerializer(contacts_of_user, many=True, context={'request': request})
        return Response(serializer.data)

