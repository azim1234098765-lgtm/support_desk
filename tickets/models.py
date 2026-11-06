from accounts.models import User
from django.db import models


class Category(models.Model):
  name = models.CharField(
      max_length=100, unique=True, verbose_name='Название категории'
  )

  class Meta:
    verbose_name = 'Категория'
    verbose_name_plural = 'Категории'

  def __str__(self):
    return self.name


class Ticket(models.Model):
  class Status(models.TextChoices):
    NEW = 'new', 'Новое'
    IN_PROGRESS = 'in_progress', 'В работе'
    RESOLVED = 'resolved', 'Решено'

  title = models.CharField(max_length=255, verbose_name='Название обращения')
  description = models.TextField(verbose_name='Описание проблемы')
  category = models.ForeignKey(
      Category,
      on_delete=models.SET_NULL,
      null=True,
      related_name='tickets',
      verbose_name='Категория',
  )
  status = models.CharField(
      max_length=20,
      choices=Status.choices,
      default=Status.NEW,
      verbose_name='Статус',
  )
  author = models.ForeignKey(
      User,
      on_delete=models.CASCADE,
      related_name='tickets',
      verbose_name='Автор',
  )
  created_at = models.DateTimeField(
      auto_now_add=True, verbose_name='Дата создания'
  )
  updated_at = models.DateTimeField(
      auto_now=True, verbose_name='Дата изменения'
  )

  class Meta:
    verbose_name = 'Обращение'
    verbose_name_plural = 'Обращения'
    ordering = ['-created_at']

  def __str__(self):
    return f'[{self.get_status_display()}] {self.title}'


class Comment(models.Model):
  ticket = models.ForeignKey(
      Ticket,
      on_delete=models.CASCADE,
      related_name='comments',
      verbose_name='Обращение',
  )
  author = models.ForeignKey(
      User, on_delete=models.CASCADE, verbose_name='Автор комментария'
  )
  text = models.TextField(verbose_name='Текст комментария')
  created_at = models.DateTimeField(
      auto_now_add=True, verbose_name='Дата создания'
  )

  class Meta:
    verbose_name = 'Комментарий'
    verbose_name_plural = 'Комментарии'
    ordering = ['created_at']

  def __str__(self):
    return f'Комментарий от {self.author.username} к тикету #{self.ticket.id}'