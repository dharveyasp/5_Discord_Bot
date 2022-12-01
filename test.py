import ssl
# import certifi
from urllib.request import urlopen

request = "https://example.com"
urlopen(request, context=ssl.create_default_context())
