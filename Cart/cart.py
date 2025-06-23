class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "product_id": product.id,
                "name": product.nombre,
                "quantity": quantity,
                "description": product.descripcion,
                "price": float(product.precio),
                "image": product.imagen.url
            }
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def save(self):
        self.session["cart"] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def decrement(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]["quantity"] -= 1
            if self.cart[product_id]["quantity"] < 1:
                self.remove(product)
            else:
                self.save()
        else:
            print("El producto no existe en el carrito")

    def clear(self):
        self.session["cart"] = {}
        self.session.modified = True

    def get_total(self):
        total = 0
        for item in self.cart.values():
            if isinstance(item, dict) and "price" in item and "quantity" in item:
                total += float(item["price"]) * item["quantity"]
        return int(round(total))

    def __iter__(self):
        for item in self.cart.values():
            yield item

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())
