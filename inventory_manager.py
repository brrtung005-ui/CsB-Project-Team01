import json
import os
from inventory_item import InventoryItem


class InventoryManager:
    """
    Manages inventory items using a dictionary for fast O(1) lookups by Item ID.
    Handles data persistence (JSON) and safely manages corrupted/missing files.
    """

    def __init__(self, data_filename: str = "inventory_data.json"):
        self.data_filename = data_filename
        # Dictionary structure: { item_id: InventoryItem }
        # Chosen for constant-time lookups and easy updates/deletions by ID.
        self.items = {}
        self.load_data()

    def load_data(self):
        """Loads inventory from JSON file. Preserves corrupted files safely."""
        if not os.path.exists(self.data_filename):
            print(f"[Info] File '{self.data_filename}' not found. Starting with empty inventory.")
            return

        try:
            with open(self.data_filename, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                self.items = {
                    item_data["item_id"]: InventoryItem.from_dict(item_data)
                    for item_data in raw_data
                }
            print(f"[Success] Loaded {len(self.items)} items from '{self.data_filename}'.")
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            backup_filename = f"corrupted_{self.data_filename}"
            print(f"\n[ERROR] '{self.data_filename}' is damaged or corrupted!")
            print(f"[Safety Action] Renaming damaged file to '{backup_filename}' to prevent data loss.")
            if os.path.exists(self.data_filename):
                os.rename(self.data_filename, backup_filename)
            self.items = {}

    def save_data(self):
        """Saves current inventory state to JSON file."""
        try:
            data_to_save = [item.to_dict() for item in self.items.values()]
            with open(self.data_filename, "w", encoding="utf-8") as f:
                json.dump(data_to_save, f, indent=4)
        except IOError as e:
            print(f"[ERROR] Could not save data: {e}")

    # --- Core Features ---

    def add_item(self, item_id: str, name: str, category: str, quantity: int, price: float) -> bool:
        if item_id in self.items:
            return False  # ID already exists
        new_item = InventoryItem(item_id, name, category, quantity, price)
        self.items[item_id] = new_item
        self.save_data()
        return True

    def get_all_items(self) -> list:
        return list(self.items.values())

    def search_by_name(self, query: str) -> list:
        query_lower = query.strip().lower()
        return [
            item for item in self.items.values()
            if query_lower in item.name.lower()
        ]

    def filter_by_category(self, category: str) -> list:
        cat_lower = category.strip().lower()
        return [
            item for item in self.items.values()
            if item.category.lower() == cat_lower
        ]

    def update_item(self, item_id: str, name: str = None, category: str = None, quantity: int = None, price: float = None) -> bool:
        if item_id not in self.items:
            return False
        
        item = self.items[item_id]
        if name:
            item.name = name
        if category:
            item.category = category
        if quantity is not None:
            item.quantity = quantity
        if price is not None:
            item.price = price
            
        self.save_data()
        return True

    def delete_item(self, item_id: str) -> bool:
        if item_id in self.items:
            del self.items[item_id]
            self.save_data()
            return True
        return False

    def get_summaries(self) -> dict:
        """Calculates low stock items (< 5 threshold) and total inventory value."""
        total_items = len(self.items)
        total_stock_value = sum(item.quantity * item.price for item in self.items.values())
        low_stock_threshold = 5
        low_stock_items = [item for item in self.items.values() if item.quantity < low_stock_threshold]
        
        return {
            "total_items": total_items,
            "total_value": total_stock_value,
            "low_stock_count": len(low_stock_items),
            "low_stock_items": low_stock_items
        }