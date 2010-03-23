# Context processors.
from django.conf import settings

def template_elements(request):
    # Return a dictionary of values
    return {
        'template_header': 'includes/header.html',
        'template_nav': 'includes/nav.html',
        'template_footer': 'includes/footer.html',
    }

def path_info(request):
    return {
        'path_info': request.META['PATH_INFO'].split('/')[1],
    }

def layout_elements(request):
    return {
        'form_actions': '<ul><li><input type="submit" name="save" value="save" id="save" /></li><li><input type="button" name="go-back" value="go back" id="go-back" /></li></ul>',
    }

def google_analytics(request):
    analytics = None
    if settings.GOOGLE_ANALYTICS_KEY:
        analytics = u"""<script type="text/javascript"> var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www."); document.write(unescape("%%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%%3E%%3C/script%%3E"));</script><script type="text/javascript">try { var pageTracker = _gat._getTracker(%s); pageTracker._trackPageview(); } catch(err) {}</script>""" % (settings.GOOGLE_ANALYTICS_KEY,)
    return {
        'google_analytics': analytics,
    }