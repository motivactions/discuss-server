from server import hooks


@hooks.register("API_V1_URL_PATTERNS")
def register_auths_urls():
    return "authentications/authentics/", "providers.authentics.api.urls"
