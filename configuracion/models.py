from django.db import models


class Config(models.Model):
    titulo = models.CharField(max_length=50, default="SoftAndPlay")
    impuesto = models.DecimalField(max_digits=5, decimal_places=2, default=12)
    logo = models.ImageField(upload_to = 'fondos/', default = 'fondos/logo.png')
    logo_horizontal = models.ImageField(upload_to = 'fondos/', default = 'fondos/logo_horizontal.png')
    fondo_login_desktop = models.ImageField(upload_to = 'fondos/', default = 'fondos/fondo_portada.jpg')
    fondo_login_mobile = models.ImageField(upload_to = 'fondos/', default = 'fondos/fondo_portada.jpg')
    fondo_pantalla_mexicana = models.ImageField(upload_to = 'fondos/', default = 'fondos/fondo_pantalla_mexicana.jpg')
    fondo_pantalla_bingo = models.ImageField(upload_to = 'fondos/', default = 'fondos/fondo_pantalla_bingo.png')
    fondo_carton_bingo = models.ImageField(upload_to = 'fondos/', default = 'fondos/fondo_carton_bingo.png')
    fondo_carton_lotoMX = models.ImageField(upload_to = 'fondos/', default = 'fondos/fondo_carton_lotoMX.png')
    tapa_balota_bingo = models.ImageField(upload_to = 'fondos/', default = 'fondos/tapa_balota_bingo.png')
    tapa_carta_lotoMX = models.ImageField(upload_to = 'fondos/', default = 'fondos/tapa_carta_lotoMX.png')
    fondo_tablero_bingo_75 = models.ImageField(upload_to = 'fondos/', default = 'fondos/fondo_tablero_bingo_75.png')
    class Meta:
        constraints = [models.CheckConstraint(check=models.Q(impuesto__gte=0) & models.Q(impuesto__lte=100), name='config_impuesto_range')]
