from allauth.account.signals import user_logged_in
from allauth.socialaccount.models import SocialAccount
from django.dispatch import receiver
from user.models import user_details 

@receiver(user_logged_in)
def handle_user_logged_in(request, user, **kwargs):
    try:
        # Get the social account for Google
        social_account = SocialAccount.objects.filter(user=user, provider='google').first()
        extra_data = social_account.extra_data if social_account else {}

        # Use the email from sociallogin first (adapter should have set it)
        email = extra_data.get("email") or user.email
        name = extra_data.get("name") or user.get_full_name() or user.username

        # Debug print to verify values:
        print("Google login - email:", email)
        print("Google login - name:", name)

        if not email:
            # In case email is still not provided, log an error:
            print("Error: Email is missing for the Google login user.")
            return

        # Create or update the user_details record
        user_data, created = user_details.objects.get_or_create(
            user_email=email,
            defaults={
                "user_name": name,
                "user_passwd": None,  # No password for social login
            }
        )
        # Update name if necessary
        if user_data.user_name != name:
            user_data.user_name = name
            user_data.save()

        # Set custom session variables
        request.session["user_id"] = user_data.user_id
        request.session["user_email"] = user_data.user_email
        request.session["user_name"] = user_data.user_name

    except Exception as e:
        print("Google login session error:", e)