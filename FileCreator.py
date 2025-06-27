import os

# Loop from 0 to 78 (79 files total)
for i in range(80):
    # Format number with leading zero if needed (e.g., 00.png, 01.png, ..., 78.png)
    filename = f"{i:02}.png"
    
    # Create an empty file
    with open(filename, 'wb') as f:
        pass  # Leave it empty (or write bytes if needed)

print("79 empty .png files created.")
