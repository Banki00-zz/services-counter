from django.db import models


# Create your models here.
class TypeOfWork(models.Model):
    """Вид работ(стрижка, окрашивание и т.д.)"""
    title = models.CharField(max_length=50, verbose_name="Название работ")
    fix_percent = models.IntegerField(null=True, verbose_name="Процент от услуги")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


class AddService(models.Model):
    price = models.IntegerField()
    sum_for_worker = models.IntegerField(blank=True, null=True)
    service = models.ForeignKey(TypeOfWork, on_delete=models.CASCADE)
    date_add = models.DateTimeField(auto_now_add=True, null = True)

    def __str__(self):
        return self.service.title

    class Meta:
        verbose_name = "Оказаная услуга"
        verbose_name_plural = "Оказанные услуги"