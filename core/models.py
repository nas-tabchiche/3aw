from django.db import models


class Policy(models.Model):
    """
    Web Application Firewall Policy

    fields:
    """

    VARIABLES = (
        ("host", "Host"),
        ("headers", "Request headers"),
        ("body", "Request body"),
    )

    OPERATORS = (
        ("contains", "Contains"),
        ("equals", "Equals"),
        ("starts-with", "Starts With"),
        ("ends-with", "Ends With"),
        ("matches", "Matches"),
    )

    ACTIONS = (("block", "Block"), ("alert", "Alert"), ("log", "Log"))

    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    variable = models.CharField(max_length=255, choices=VARIABLES)
    selector = models.CharField(max_length=255)
    operator = models.CharField(max_length=255, choices=OPERATORS)
    value = models.CharField(max_length=255)
    action = models.CharField(max_length=255, choices=ACTIONS)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Policies"
