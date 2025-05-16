def process_social_account_picture(user, extra_data):

    picture_url = extra_data.get('picture')

    if picture_url:
        user.profile_picture = picture_url
        user.save()
