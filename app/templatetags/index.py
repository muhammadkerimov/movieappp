from django import template

register = template.Library()

@register.filter(name='multiply')
def add1(value):
    """Multiplies the value by the argument."""
    try:
        return value+1 
    except (ValueError, TypeError):
        return value
    


@register.filter(name='duration_format')
def duration_format(value):
    """Format a timedelta object (DurationField) as 'HH:MM:SS'."""
    total_seconds = int(value.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f'{hours:02} hours {minutes:02} minutes'



@register.filter(name='getfilename')
def filename(value):
    
    name = value.split('/')[-1]
    return name



@register.filter(name='decreaseword')
def decreaseword(value):
    
    name = ' '.join(value.split(' ')[:10])+'...'
    return name