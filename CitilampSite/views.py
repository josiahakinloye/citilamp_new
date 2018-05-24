from django.shortcuts import render_to_response


def custom_404_handler(requesr):
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response
