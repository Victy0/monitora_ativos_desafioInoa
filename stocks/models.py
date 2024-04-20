from django.db import models
from django.utils import timezone
from django.utils.dateformat import format
from django.utils.translation import gettext_lazy as _

from users.models import User


class Stock(models.Model):
    id_stock = models.AutoField(_("identificador do registro de ativo"), primary_key=True)
    name = models.CharField(_("nome do ativo"), max_length=50)
    acronym = models.CharField(_("sigla do ativo"), max_length=10, unique=True)
    sector = models.CharField(_("setor de operação do ativo"), max_length=100, null=True)
    is_brazilian = models.BooleanField(_("indicativo se ativo é brasileiro"), default=True)
    
    class Meta:
        db_table = "stock"
        
    def __str__(self):
        return self.name + '(' + self.acronym + ')'
    
class UserStock(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    max_price = models.DecimalField(_("valor máximo do túnel estático definido pelo usuário"), max_digits=10, decimal_places=2)
    min_price = models.DecimalField(_("valor mínimo do túnel estático definido pelo usuário"), max_digits=10, decimal_places=2)
    update_frequency = models.CharField(_("frequencia em minutos de atualização dos dados do ativo definido pelo usuário"), max_length=20)
    
    class Meta:
        db_table = "user_stock"
        
    def __str__(self):
        return '(Usuário: ' + str(self.id_user) + '; Ativo: ' + str(self.id_stock) + ')'
    
class StockHistory(models.Model):
    id_stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(_("data de criação do registro de usuário no sistema"), default=timezone.now)
    previous_close = models.DecimalField(_("preço do frechamento anterior"), max_digits=10, decimal_places=2, default=0)
    open_price = models.DecimalField(_("preço de aberuta do ativo"), max_digits=10, decimal_places=2, default=0)
    max_price = models.DecimalField(_("preço de máxima do ativo"), max_digits=10, decimal_places=2, default=0)
    min_price = models.DecimalField(_("preço de mínima do ativo"), max_digits=10, decimal_places=2, default=0)
    volume = models.BigIntegerField(_("volume do ativo"), default=0)
    
    class Meta:
        db_table = "stock_history"
        
    def __str__(self):
        return '(Ativo: ' + str(self.id_stock) + ';' + 'Data:' + format(self.creation_date, 'DD/MM/YYYY %H:%M') + ')'