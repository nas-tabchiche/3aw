from django.db import models


class Instance(models.Model):
    """
    Web Application Firewall Instance
    """

    host = models.CharField(max_length=255)
    port = models.IntegerField()


class Rule(models.Model):
    """
    Web Application Firewall Rule

    fields:
        name: name of the rule
        description: description of the rule
        action: action to take if the rule matches
        pattern: regular expression to match
        instances: instances where the rule is applied
    """

    name = models.CharField(max_length=255)
    description = models.TextField()
    action = models.CharField(max_length=255)
    pattern = models.CharField(max_length=255)
    instances = models.ManyToManyField(Instance)
