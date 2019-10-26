"""View module for handling requests about alerts"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from helloDanhApi.models import Alert, AlertPlacement, CustomUser


class AlertSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for alerts

    Arguments:
        serializers
    """
    class Meta:
        model = Alert
        url = serializers.HyperlinkedIdentityField(
            view_name='alert',
            lookup_field='id'
        )
        fields = ('id', 'url', 'alert_enabled', 'alert', 'alert_placement')
        depth = 1


class Alerts(ViewSet):
    """Alerts for helloDanh"""

    # def create(self, request):
    #     """Handle POST operations

    #     Returns:
    #         Response -- JSON serialized Alert instance
    #     """
    #     new_alert = Alert()
    #     new_alert.alert = request.data["alert"]
    #     alert_placement = AlertPlacement.objects.get(pk=request.data["alert_placement"])
    #     custom_user = CustomUser.objects.get(user=request.auth.user)
    #     alert_enabled = True
    #     new_alert.alert_placement = alert_placement
    #     new_alert.user = custom_user
    #     new_alert.alert_enabled = alert_enabled
    #     new_alert.save()

    #     serializer = AlertSerializer(new_alert, context={'request': request})

    #     return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single alert

        Returns:
            Response -- JSON serialized alert instance
        """
        try:
            alert = Alert.objects.get(pk=pk)
            serializer = AlertSerializer(alert, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for an alert

        Returns:
            Response -- Empty body with 204 status code
        """
        alert = Alert.objects.get(pk=pk)
        alert.alert = request.data["alert"]
        alert.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def list(self, request):
        """Handle GET requests to alert resource

        Returns:
            Response -- JSON serialized list of alerts
        """
        try:
            user = CustomUser.objects.get(user=request.auth.user)
            alerts_of_user = Alert.objects.filter(user=user)

        except Alert.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        serializer = AlertSerializer(alerts_of_user, many=True, context={'request': request})
        return Response(serializer.data)