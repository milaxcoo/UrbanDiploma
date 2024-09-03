from django.db import models

class Quote(models.Model):
    text = models.TextField(verbose_name="Text of the quote")
    author = models.CharField(max_length=100, verbose_name="Author of the quote")

    def __str__(self):
        return f'"{self.text}" - {self.author}'
