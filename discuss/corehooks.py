from server import hooks


@hooks.register("API_V1_URL_PATTERNS")
def register_discuss_urls():
    return "", "discuss.api.v1.urls"
