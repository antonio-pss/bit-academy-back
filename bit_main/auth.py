from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    refresh['id'] = user.id
    refresh['email'] = user.email
    refresh['name'] = user.name
    refresh['is_active'] = user.is_active
    refresh['date_joined'] = user.date_joined.isoformat() if user.date_joined else None
    refresh['avatar'] = user.avatar

    access = refresh.access_token
    refresh['id'] = user.id
    refresh['email'] = user.email
    refresh['name'] = user.name
    refresh['is_active'] = user.is_active
    refresh['date_joined'] = user.date_joined.isoformat() if user.date_joined else None
    refresh['avatar'] = user.avatar

    return {
        'access': str(access),
        'refresh': str(refresh),
    }