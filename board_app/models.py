from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    """
    Board model representing a project/kanban board.
    
    Attributes:
        title: Board title
        owner: User who created and owns the board
        members: Users who are members of the board
        member_count: Count of board members (cached)
        ticket_count: Count of tasks/tickets (cached)
        tasks_to_do_count: Count of tasks with status 'todo' (cached)
        tasks_high_prio_count: Count of high priority tasks (cached)
    """
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owner_boards'
    )
    members = models.ManyToManyField(
        User,
        related_name='member_boards',
        blank=True
    )
    member_count = models.IntegerField(default=0)
    ticket_count = models.IntegerField(default=0)
    tasks_to_do_count = models.IntegerField(default=0)
    tasks_high_prio_count = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Board'
        verbose_name_plural = 'Boards'
        ordering = ['-id']

    def __str__(self):
        return f'{self.title} (Owner: {self.owner.email})'
