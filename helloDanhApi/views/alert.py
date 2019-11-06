"""View module for handling requests about alerts"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from helloDanhApi.models import Alert, CustomUser


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
        fields = ('id', 'url', 'subject', 'alert', 'alert_placement_id')
        depth = 1


class Alerts(ViewSet):
    """Alerts for helloDanh"""

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
        edit_alert = Alert.objects.get(pk=pk)
        edit_alert.alert = request.data["alert"]
        edit_alert.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def list(self, request):
        """Handle GET requests to alert resource

        Returns:
            Response -- JSON serialized list of alerts
        """
        try:
            user = CustomUser.objects.get(user=request.auth.user)
            alerts_of_user = Alert.objects.filter(user=user)
            alert_placement = self.request.query_params.get('alert_placement_id', None)

            if alert_placement is not None:
                alert = alerts_of_user.filter(alert_placement=alert_placement).get()
                serializer = AlertSerializer(
                alert, many=False, context={'request': request}
                )
            else:
                serializer = AlertSerializer(
                alerts_of_user, many=True, context={'request': request}
                )

        except Alert.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data)
