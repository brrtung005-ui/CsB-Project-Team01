from inventory_manager import InventoryManager


def get_non_empty_string(prompt: str) -> str:
    """Helper to validate non-empty text input."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Error: Input cannot be empty. Please try again.")


def get_positive_int(prompt: str, allow_zero: bool = True) -> int:
    """Helper to validate non-negative integers."""
    while True:
        try:
            val = int(input(prompt).strip())
            if allow_zero and val >= 0:
                return val
            elif not allow_zero and val > 0:
                return val
            print("Error: Value must be positive." if not allow_zero else "Error: Value cannot be negative.")
        except ValueError:
            print("Error: Invalid number. Please enter a valid integer.")


def get_positive_float(prompt: str) -> float:
    """Helper to validate positive float amounts."""
    while True:
        try:
            val = float(input(prompt).strip())
            if val >= 0:
                return val
            print("Error: Price cannot be negative.")
        except ValueError:
            print("Error: Invalid price. Please enter a valid number.")


def display_items_table(items: list):
    """Prints items in a formatted readable table."""
    if not items:
        print("\n--> No records found.")
        return

    print("\n" + "=" * 70)
    print(f"{'ID':<8} | {'Item Name':<20} | {'Category':<15} | {'Qty':<6} | {'Price ($)':<8}")
    print("-" * 70)
    for item in items:
        print(f"{item.item_id:<8} | {item.name:<20} | {item.category:<15} | {item.quantity:<6} | {item.price:<8.2f}")
    print("=" * 70)


def main():
    manager = InventoryManager("inventory_data.json")

    while True:
        print("\n=== SMALL SHOP INVENTORY MANAGEMENT ===")
        print("1. Add Item")
        print("2. View All Items")
        print("3. Search / Filter Items")
        print("4. Update Item")
        print("5. Delete Item")
        print("6. Show Summary Report")
        print("7. Exit")

        choice = input("\nSelect an option (1-7): ").strip()

        if choice == "1":
            print("\n--- Add New Item ---")
            item_id = get_non_empty_string("Enter Unique Item ID (e.g., ITEM01): ").upper()
            if item_id in manager.items:
                print(f"Error: Item ID '{item_id}' already exists!")
                continue
            name = get_non_empty_string("Enter Item Name: ")
            category = get_non_empty_string("Enter Category: ")
            quantity = get_positive_int("Enter Initial Quantity: ")
            price = get_positive_float("Enter Unit Price ($): ")

            if manager.add_item(item_id, name, category, quantity, price):
                print(f"[Success] Item '{name}' added successfully.")

        elif choice == "2":
            print("\n--- All Inventory Items ---")
            display_items_table(manager.get_all_items())

        elif choice == "3":
            print("\n--- Search / Filter ---")
            print("1. Search by Name")
            print("2. Filter by Category")
            sub_choice = input("Select choice (1-2): ").strip()
            
            if sub_choice == "1":
                q = get_non_empty_string("Enter name keyword: ")
                results = manager.search_by_name(q)
                display_items_table(results)
            elif sub_choice == "2":
                cat = get_non_empty_string("Enter category: ")
                results = manager.filter_by_category(cat)
                display_items_table(results)
            else:
                print("Invalid sub-option selected.")

        elif choice == "4":
            print("\n--- Update Item ---")
            item_id = get_non_empty_string("Enter Item ID to update: ").upper()
            if item_id not in manager.items:
                print(f"Error: No item found with ID '{item_id}'.")
                continue

            print("(Leave blank to keep existing value)")
            name = input("New Name: ").strip()
            category = input("New Category: ").strip()
            
            qty_str = input("New Quantity: ").strip()
            quantity = int(qty_str) if qty_str.isdigit() else None

            price_str = input("New Price ($): ").strip()
            try:
                price = float(price_str) if price_str else None
            except ValueError:
                price = None

            if manager.update_item(
                item_id,
                name=name if name else None,
                category=category if category else None,
                quantity=quantity,
                price=price
            ):
                print(f"[Success] Item '{item_id}' updated successfully.")

        elif choice == "5":
            print("\n--- Delete Item ---")
            item_id = get_non_empty_string("Enter Item ID to delete: ").upper()
            if item_id not in manager.items:
                print(f"Error: No item found with ID '{item_id}'.")
                continue

            confirm = input(f"Are you sure you want to delete '{manager.items[item_id].name}'? (y/N): ").strip().lower()
            if confirm == 'y':
                if manager.delete_item(item_id):
                    print(f"[Success] Item '{item_id}' deleted.")
            else:
                print("[Cancelled] Deletion cancelled.")

        elif choice == "6":
            print("\n--- Inventory Summary ---")
            summary = manager.get_summaries()
            print(f"Total Unique Product Lines: {summary['total_items']}")
            print(f"Total Stock Valuation:     ${summary['total_value']:.2f}")
            print(f"Low Stock Alert (< 5 qty):  {summary['low_stock_count']} items")
            if summary['low_stock_items']:
                print("\nItems needing restock:")
                display_items_table(summary['low_stock_items'])

        elif choice == "7":
            print("\nExiting program. All changes saved.")
            break
        else:
            print("Invalid selection. Please choose an option between 1 and 7.")


if __name__ == "__main__":
    main()