import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from PIL import Image
import time
import os
import sys
from reportlab.pdfgen import canvas

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Capture screenshots from a webpage and create a PDF.")
    parser.add_argument("--url", required=True, help="URL of the webpage to capture")
    parser.add_argument("--pages", type=int, required=True, help="Number of pages to capture")
    parser.add_argument("--email", help="Email for login (optional)")
    parser.add_argument("--password", help="Password for login (optional)")
    parser.add_argument("--output", default="output_screenshots.pdf", help="Output PDF file name")
    return parser.parse_args()

def login(driver, email, password):
    """Attempt to log in to the webpage if credentials are provided."""
    if not email or not password:
        print("No credentials provided, skipping login.")
        return
    try:
        email_field = driver.find_element(By.ID, "login-email")
        email_field.send_keys(email)
        email_field.send_keys(Keys.RETURN)
        time.sleep(2)
        password_field = driver.find_element(By.ID, "password-login")
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        time.sleep(5)  # Wait for login to complete
        print("Login successful.")
    except NoSuchElementException:
        print("Login fields not found, assuming already logged in or not required.")

def capture_screenshots(driver, url, total_pages, output_folder):
    """Capture screenshots by scrolling through the webpage."""
    try:
        driver.get(url)
        time.sleep(5)  # Wait for page to load
        login(driver, args.email, args.password)  # Attempt login if credentials provided

        # Get page height for dynamic scrolling
        page_height = driver.execute_script("return document.body.scrollHeight")
        viewport_height = driver.execute_script("return window.innerHeight")

        for page in range(total_pages):
            # Scroll to the next page position
            scroll_position = viewport_height * page
            driver.execute_script(f"window.scrollTo(0, {scroll_position});")
            time.sleep(1)  # Wait for content to load

            # Save screenshot
            screenshot_path = os.path.join(output_folder, f"page_{page + 1}.png")
            driver.save_screenshot(screenshot_path)
            print(f"Captured page {page + 1}/{total_pages}")
    except WebDriverException as e:
        print(f"Error during screenshot capture: {e}")
        sys.exit(1)

def create_pdf_from_images(output_folder, output_pdf):
    """Combine screenshots into a PDF file."""
    try:
        c = canvas.Canvas(output_pdf)
        image_files = [f for f in os.listdir(output_folder) if f.endswith(".png")]

        for image_file in sorted(image_files):
            image_path = os.path.join(output_folder, image_file)
            img = Image.open(image_path)
            width, height = img.size
            c.setPageSize((width, height))
            c.drawImage(image_path, 0, 0, width, height)
            c.showPage()

        c.save()
        print(f"PDF created at {output_pdf}")
    except Exception as e:
        print(f"Error creating PDF: {e}")
        sys.exit(1)

def main():
    """Main function to execute the screenshot-to-PDF process."""
    args = parse_arguments()

    # Create output folder if it doesn't exist
    output_folder = "screenshots"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Initialize Chrome browser
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")  # Open in full-screen mode
        driver = webdriver.Chrome(options=options)  # Requires ChromeDriver in PATH
    except WebDriverException as e:
        print(f"Failed to initialize ChromeDriver: {e}")
        sys.exit(1)

    # Capture screenshots and create PDF
    try:
        capture_screenshots(driver, args.url, args.pages, output_folder)
        driver.quit()
        create_pdf_from_images(output_folder, args.output)
    except Exception as e:
        print(f"Unexpected error: {e}")
        driver.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()