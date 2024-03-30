import time
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

# Function to reverse the RGB values of a pixel
def reverse_pixel(pixel):
    return tuple(255 - value for value in pixel)

# Function to process a portion of the image
def process_chunk(image, start_x, end_x):

    for x in range(start_x, end_x):
        for y in range(image.height):
            pixel = image.getpixel((x, y))
            reversed_pixel = reverse_pixel(pixel)
            image.putpixel((x, y), reversed_pixel)

# Single-threaded approach
def single_threaded_reverse(image_path):
    start_time = time.time()
    # Open image
    img = Image.open(image_path)
    # Process image
    for x in range(img.width):
        for y in range(img.height):
            pixel = img.getpixel((x, y))
            reversed_pixel = reverse_pixel(pixel)
            img.putpixel((x, y), reversed_pixel)
    # Save the modified image
    img.save("reversed_single_threaded.jpg")
    end_time = time.time()
    # Measure time taken
    print("Single-threaded time:", end_time - start_time)

# Multi-threaded approach
def multi_threaded_reverse(image_path):
    start_time = time.time()
    img = Image.open(image_path)
    num_threads = 4  # Number of threads/processes
    chunk_size = img.width // num_threads
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for i in range(num_threads):
            start_x = i * chunk_size
            end_x = (i + 1) * chunk_size if i < num_threads - 1 else img.width
            futures.append(executor.submit(process_chunk, img.copy(), start_x, end_x))
        for future in futures:
            future.result()
    img.save("reversed_multi_threaded.jpg")
    end_time = time.time()
    print("Multi-threaded time:", end_time - start_time)

# Main function
def main():
    image_path = r"C:\Users\aseel\Downloads\BackendCourse\week6\lecture15\img1.jpg"
    single_threaded_reverse(image_path)
    multi_threaded_reverse(image_path)

if __name__ == "__main__":
    main()
