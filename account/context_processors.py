def theme_context(request):
    if request.user.is_authenticated:
        return {"current_theme": request.user.theme_preference}
    return {"current_theme": "light"}
