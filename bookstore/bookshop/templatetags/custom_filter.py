from django import template

register = template.Library()

@register.filter(name='currency')
def currency(number):
    return "Rs "+str(number)



@register.filter(name='multiply')
def multiply(number , number1):
    return number * number1

@register.filter(name='fullname')
def get_fullname(Customer, cus_id):
        return Customer.objects.filter(id = cus_id).values('fullname')