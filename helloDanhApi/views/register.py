from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.registration.views import RegisterView

    class CustomRegisterSerializer(RegisterSerializer):

        email = serializers.EmailField(required=True)
        password1 = serializers.CharField(write_only=True)
        first_name = serializers.CharField(required=True)
        last_name = serializers.CharField(required=True)
        address = serializers.CharField(required=True)

        def get_cleaned_data(self):
            super(CustomRegisterSerializer, self).get_cleaned_data()

            return {
                'password1': self.validated_data.get('password1', ''),
                'email': self.validated_data.get('email', ''),
                'name': self.validated_data.get('name', ''),
                'date_of_birth': self.validated_data.get('date_of_birth', ''),
            }

    class CustomUserDetailsSerializer(serializers.ModelSerializer):

        class Meta:
            model = User
            fields = ('email','name','date_of_birth')
            read_only_fields = ('email',)

    class CustomRegisterView(RegisterView):
        queryset = User.objects.all()