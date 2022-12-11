from decimal import Decimal
from djmoney.money import Money

from django.conf import settings
from inventory.models import Item
from mainapp.models import DeliveryOptions


class Basket:
    """
    A base Basket class, providing some default behaviors that
    can be inherited or overrided, as necessary.
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def add(self, item, qty = 1, override_qty = False):
        """
        Adding and updating the users basket session data
        """
        item_id = str(item.id)

        if item_id not in self.basket:
            self.basket[item_id] = {'qty': 0, 'price':  str(item.selling_price().amount)}
        
        if override_qty:
            self.basket[item_id]["qty"] = qty
        else:
            self.basket[item_id]['qty'] += qty

        self.save()

    def __iter__(self):
        """
        Collect the item_id in the session data to query the database
        and return items
        """
        item_ids = self.basket.keys()
        items = Item.objects.filter(id__in=item_ids)
        basket = self.basket.copy()

        for item in items:
            basket[str(item.id)]["item"] = item

        for item in basket.values():
            item["price"] = Money(item["price"], 'MWK')
            item["total_price"] = item["price"] * int(item["qty"])
            yield item

    def __len__(self):
        """
        Get the basket data and count the qty of items
        """
        return sum(item["qty"] for item in self.basket.values())

    def update(self, item, qty):
        """
        Update values in session data
        """
        item_id = str(item)
        if item_id in self.basket:
            self.basket[item_id]["qty"] = qty
        self.save()

    def get_subtotal_price(self):
        return sum(item["price"] * item["qty"] for item in self.basket.values())

    def get_delivery_price(self):
        newprice =  Money(0.00, 'MWK')

        if "purchase" in self.session:
            newprice = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_id"]).delivery_price

        return newprice

    def get_total_price(self):
        newprice = Money(0.00, 'MWK')
        subtotal = sum(Money(item["price"], 'MWK') * item["qty"] for item in self.basket.values())

        if "purchase" in self.session:
            newprice = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_id"]).delivery_price

        total = subtotal + newprice
        return total

    def basket_update_delivery(self, deliveryprice=Money(0.0, 'MWK')):
        subtotal = sum(Money(item["price"], 'MWK') * item["qty"] for item in self.basket.values())
        total = subtotal + Money(deliveryprice, 'MWK')
        return total

    def delete(self, item):
        """
        Delete item from session data
        """
        item_id = str(item)
        if item_id in self.basket:
            del self.basket[item_id]
            self.save()

    def clear(self):
        # Remove basket from session
        del self.session[settings.BASKET_SESSION_ID]
        del self.session["address"]
        del self.session["purchase"]
        self.save()

    def save(self):
        self.session.modified = True
    
