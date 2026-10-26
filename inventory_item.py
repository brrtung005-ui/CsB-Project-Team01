class InventoryItem:
    """Represents a single item in the shop inventory."""

    def __init__(self, item_id: str, name: str, category: str, quantity: int, price: float):
        self.item_id = item_id
        self.name = name
        self.category = category
        self.quantity = quantity
        self.price = price

    def to_dict(self) -> dict:
        """Convert object to dictionary for JSON persistence."""
        return {
            "item_id": self.item_id,
            "name": self.name,
            "category": self.category,
            "quantity": self.quantity,
            "price": self.price,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Reconstruct object from dictionary loaded from JSON."""
        return cls(
            item_id=data["item_id"],
            name=data["name"],
            category=data["category"],
            quantity=int(data["quantity"]),
            price=float(data["price"]),
        )
        