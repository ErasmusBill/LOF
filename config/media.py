import mimetypes
import os

from django.conf import settings
from django.http import FileResponse, Http404, HttpResponseNotModified
from django.utils.http import http_date
from django.utils._os import safe_join
from django.views.static import was_modified_since


def serve_media(request, path):
    if not settings.MEDIA_ROOT:
        raise Http404("MEDIA_ROOT is not set.")

    fullpath = safe_join(settings.MEDIA_ROOT, path)
    if not os.path.exists(fullpath):
        raise Http404("Media file not found.")

    statobj = os.stat(fullpath)
    if not was_modified_since(
        request.META.get("HTTP_IF_MODIFIED_SINCE"),
        statobj.st_mtime,
        statobj.st_size,
    ):
        return HttpResponseNotModified()

    content_type, encoding = mimetypes.guess_type(fullpath)
    response = FileResponse(open(fullpath, "rb"), content_type=content_type)
    response["Last-Modified"] = http_date(statobj.st_mtime)
    if encoding:
        response["Content-Encoding"] = encoding
    return response
