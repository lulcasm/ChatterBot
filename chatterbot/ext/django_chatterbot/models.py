from django.db import models
from django.utils import timezone


class Statement(models.Model):
    """
    A statement represents a single spoken entity, sentence or
    phrase that someone can say.
    """

    text = models.CharField(
        blank=False,
        null=False,
        max_length=255
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        help_text='The date and time that this statement was created at.'
    )

    extra_data = models.CharField(max_length=500)

    response = models.OneToOneField(
        'Statement',
        related_name='in_response_to',
        null=True
    )

    def __str__(self):
        if len(self.text.strip()) > 60:
            return '{}...'.format(self.text[:57])
        elif len(self.text.strip()) > 0:
            return self.text
        return '<empty>'

    def __init__(self, *args, **kwargs):
        super(Statement, self).__init__(*args, **kwargs)

        # Responses to be saved if the statement is updated with the storage adapter
        self.response_statement_cache = []

    def add_extra_data(self, key, value):
        """
        Add extra data to the extra_data field.
        """
        import json

        if not self.extra_data:
            self.extra_data = '{}'

        extra_data = json.loads(self.extra_data)
        extra_data[key] = value

        self.extra_data = json.dumps(extra_data)

    def serialize(self):
        """
        :returns: A dictionary representation of the statement object.
        :rtype: dict
        """
        import json
        data = {}

        if not self.extra_data:
            self.extra_data = '{}'

        data['text'] = self.text
        data['in_response_to'] = {'text': self.in_response_to.text}
        data['created_at'] = self.created_at
        data['extra_data'] = json.loads(self.extra_data)

        return data


class Conversation(models.Model):
    """
    A sequence of statements representing a conversation.
    """

    root = models.OneToOneField(
        'Statement',
        related_name='conversation',
        help_text='The initiating statement in a conversation.'
    )

    def __str__(self):
        return str(self.id)

