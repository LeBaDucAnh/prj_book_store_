from django import template

register = template.Library()

@register.filter(name='currency')
def currency(number):
    return "Rs "+str(number)

@register.filter(name='float')
def convert_to_float(value):
    return float(value)


@register.filter(name='multiply')
def multiply(number , number1):
    return number * number1

@register.filter(name='fullname')
def get_fullname(Customer, cus_id):
        return Customer.objects.filter(id = cus_id).values('fullname')

@register.simple_tag
def rating_stars(rating):
    full_stars = int(rating)
    empty_stars = 5 - full_stars

    html = '<div class="star-ratings-css">\n'
    html += '<ul>\n'

    for i in range(full_stars):
        html += '<li class="active">&#9733;</li>\n'

    for i in range(empty_stars):
        html += '<li>&#9734;</li>\n'

    html += '</ul>\n'
    html += '</div>\n'

    return html