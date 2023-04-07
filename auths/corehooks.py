from server import hooks


@hooks.register("API_V1_URL_PATTERNS")
def register_auth_urls():
    return "authentications/", "auths.api.auth.urls"


@hooks.register("API_V1_URL_PATTERNS")
def register_users_urls():
    return "users/", "auths.api.v1.urls"


@hooks.register("API_V1_URL_PATTERNS")
def register_me_urls():
    return "me/", "auths.api.v1.urls_me"
