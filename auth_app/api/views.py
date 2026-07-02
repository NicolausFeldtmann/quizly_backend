from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import RegistrationSerializer

class RegistrationView(APIView):
    """View to create user account, if serializer given valid data."""
    permission_classes = [AllowAny]

    def post(self, request):
        """Function to handle POST-request for account crewation."""
        """Returns statuscode depending of validation status of given data."""
        serializer = RegistrationSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()

            data = {
                'username': saved_account.username,
                'email': saved_account.email,
                'user_id': saved_account.pk
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CookieTokenObtainPairView(TokenObtainPairView):
    """View to set access and refresh cookies if login was successfull."""
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """Function sets cookies necessary for user athentication."""
        response = super().post(request, *args, **kwargs)
        refresh = response.data.get("refresh")
        access = response.data.get("access")

        response.set_cookie(
            key="access_token",
            value=access,
            httponly=True,
            secure=True,
            samesite="Lax"
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh,
            httponly=True,
            secure=True,
            samesite="Lax"
        )
        response.data = {"message": "Login successfull."}
        return response

class CookieRefreshView(TokenRefreshView):
    """View to recreate and hand over new access cookie, if refresh token is valid."""
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """Handles POST-request of refresh cookie. Returns new access cookie."""
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token is None:
            return Response(
                {"detail": "Refresh token notfound"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = self.get_serializer(data={"refresh": refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response(
                {"detail": "Refresh token invalid!"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        access_token = serializer.validated_data.get("access")
        response = Response({"detail": "Token refreshed!"})
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="Lax"
        )
        return response

class LogoutView(APIView):
    """View to handle user logout."""
    """Eraseses access and refresh cookie of user."""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        response = Response({"detail": "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid."}, status=status.HTTP_200_OK)
        response.delete_cookie("access_token", path="/")
        response.delete_cookie("refresh_token", path="/")
        return response