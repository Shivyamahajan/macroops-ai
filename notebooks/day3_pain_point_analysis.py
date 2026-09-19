import pandas as pd

orders    = pd.read_csv('data/dummy/orders.csv')
picking   = pd.read_csv('data/dummy/picking.csv')
delivery  = pd.read_csv('data/dummy/delivery.csv')
inventory = pd.read_csv('data/dummy/inventory.csv')
workforce = pd.read_csv('data/dummy/workforce.csv')

print("=== PAIN POINT NUMBERS ===\n")

# Pain Point 1 — SLA
breach_rate = orders['sla_breached'].mean() * 100
avg_delay   = orders['delivery_delay_minutes'].mean()
print(f"SLA Breach Rate: {breach_rate:.1f}%")
print(f"Average Delay:   {avg_delay:.2f} minutes")
print(f"Status breakdown:\n{orders['status'].value_counts()}\n")

# Pain Point 2 — Picking
slow_picks    = (picking['pick_duration_minutes'] > 20).sum()
slow_pct      = slow_picks / len(picking) * 100
missing_orders = (picking['items_missing'] > 0).sum()
missing_pct   = missing_orders / len(picking) * 100
print(f"Orders with pick > 20 min: {slow_picks} ({slow_pct:.1f}%)")
print(f"Orders with missing items: {missing_orders} ({missing_pct:.1f}%)")
print(f"Avg pick duration: {picking['pick_duration_minutes'].mean():.2f} min")
print(f"Max pick duration: {picking['pick_duration_minutes'].max():.1f} min\n")

# Pain Point 3 — Delivery Assignment
high_delay = (delivery['assignment_delay_minutes'] > 15).sum()
high_pct   = high_delay / len(delivery) * 100
print(f"Deliveries with assignment delay > 15 min: {high_delay} ({high_pct:.1f}%)")
print(f"Avg assignment delay: {delivery['assignment_delay_minutes'].mean():.2f} min")
print(f"Max assignment delay: {delivery['assignment_delay_minutes'].max():.1f} min\n")

# Pain Point 4 — Inventory
low_acc   = (inventory['inventory_accuracy_pct'] < 80).sum()
low_pct   = low_acc / len(inventory) * 100
neg_var   = (inventory['stock_variance'] < 0).sum()
stockouts = (inventory['stockout'] == 'Yes').sum()
print(f"Items with accuracy < 80%: {low_acc} ({low_pct:.1f}%)")
print(f"Items with negative variance (physical < system): {neg_var}")
print(f"Stockout items: {stockouts}")
print(f"Avg inventory accuracy: {inventory['inventory_accuracy_pct'].mean():.1f}%\n")

stores_low = inventory[inventory['inventory_accuracy_pct'] < 80].groupby('store_id').size()
print(f"Stores with at least one item below 80% accuracy: {len(stores_low)}\n")

# Pain Point 7 — Workforce
overloaded = (workforce['tasks_pending'] > 10).sum()
over_pct   = overloaded / len(workforce) * 100
print(f"Employees with > 10 pending tasks: {overloaded} ({over_pct:.1f}%)")
print(f"\nPending tasks by role:")
print(workforce.groupby('role')['tasks_pending'].mean().sort_values(ascending=False))
print(f"\nPending tasks by shift:")
print(workforce.groupby('shift')['tasks_pending'].mean().sort_values(ascending=False))