import matplotlib.pyplot as plt
import sys


print(sys.executable)

categories = ('A', 'B', 'C', 'D', 'E')

values = [10, 15, 7, 12, 20]

colors = ['red', 'blue', 'green', 'orange', 'purple']

bars = plt.bar(categories, values, color=colors)

# Add labels on top of each bar#
for bar in bars:
    height = bar.get_height()   # get the height of each bar
    plt.text(
       bar.get_x() + bar.get_width() / 2,   # x-position (middle of the bar)
        height,                              # y-position (top of the bar)
        str(height),                         # text (the number itself)
        ha='center', va='bottom'             # align center horizontally, bottom vertically
    )

# ✅ Add grid lines (only on Y-axis for readability)
plt.grid(axis='y', linestyle='--', alpha=1.0)
#plt.grid(axis='x', linestyle='--', alpha=1.0)

plt.xlabel('categories')
plt.ylabel('values')
plt.title('Colored Bar Graph')
plt.show()