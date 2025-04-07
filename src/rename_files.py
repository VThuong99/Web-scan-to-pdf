import os

# Path to the folder containing screenshots
folder_path = "screenshots"

# Iterate through all files in the folder
for filename in os.listdir(folder_path):
    # Check if the file starts with "page_" and ends with ".png"
    if filename.startswith("page_") and filename.endswith(".png"):
        # Extract the page number from the filename (remove "page_" and ".png")
        number = filename[len("page_"):-len(".png")]
        
        # Convert to 3-digit format (e.g., 1 -> 001)
        new_number = f"{int(number):03d}"
        
        # Create new filename
        new_filename = f"page_{new_number}.png"
        
        # Define old and new file paths
        old_file = os.path.join(folder_path, filename)
        new_file = os.path.join(folder_path, new_filename)
        
        # Rename the file
        os.rename(old_file, new_file)
        print(f"Renamed: {filename} -> {new_filename}")

print("File renaming completed!")