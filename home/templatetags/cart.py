from django import template

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(menu , cart ):
    keys = cart.keys()
    for id in keys:
        if int(id) == menu.id:
            return True

    return False


@register.filter(name='cart_quantity')
def cart_quantity(menu , cart ):
    keys = cart.keys()
    for id in keys:
        if int(id) == menu.id:
            return cart.get(id)

    return 0

@register.filter(name='price_total')
def price_total(menu , cart ):
    return menu.price * cart_quantity(menu,cart)

@register.filter(name='total_cart_price')
def total_cart_price(menues,cart):
    sum=0
    for prdct in menues:
        sum += price_total(prdct , cart)

    return sum