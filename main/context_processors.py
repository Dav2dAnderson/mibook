def user_context(request):
    if request.user.is_authenticated:
        return {'profile_user': request.user}
    return []