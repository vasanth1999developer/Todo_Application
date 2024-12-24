from djchoices import ChoiceItem, DjangoChoices


class StatusChoices(DjangoChoices):
       
    """Holds the choices of status."""
    
    pending = ChoiceItem("pending", "Pending")
    completed = ChoiceItem("completed", "Completed")
