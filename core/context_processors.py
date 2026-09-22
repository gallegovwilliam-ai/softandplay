from configuracion.models import Config

def configuracion(request):
    """
      The context processor must return a dictionary.
    """
    config, created = Config.objects.get_or_create(pk=1)
    return {'config':config} 
