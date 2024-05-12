import sys
import json
import time
# Define a function to create a complex object based on the argument
def create_complex_object(argument):
    # You can replace this with your actual object creation logic
    complex_obj = {
        'imageArrayUUID': '04a89561-c8aa-400c-ae81-37dd8a806596',
        'images': [
            {
                'id': '306362b1-26ba-45f1-8a1d-f95935769a0f_istockphoto-1933752815-170667a.webp',
                'imgUrl': 'https://19p1472-dis-images.s3.eu-north-1.amazonaws.com/306362b1-26ba-45f1-8a1d-f95935769a0f_istockphoto-1933752815-170667a.webp?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAZI2LB5JHNWBKCKBL%2F20240512%2Feu-north-1%2Fs3%2Faws4_request&X-Amz-Date=20240512T122734Z&X-Amz-Expires=3600&X-Amz-Signature=11848ea1bd25e8e15182c5975226dc8adca12e7899b16df8de3f796cc7ffb5ed&X-Amz-SignedHeaders=host&x-id=GetObject',
                'mimeType': 'image/webp'
            }
        ],
        'something':argument
    }

    time.sleep(3)
    return json.dumps(complex_obj)

if __name__ == "__main__":
    # Check if an argument is provided
    if len(sys.argv) != 2:
        print("Usage: python work.py <argument>")
        sys.exit(1)

    # Get the argument
    argument = sys.argv[1]

    # Create a complex object based on the argument and serialize it to a string
    complex_obj_str = create_complex_object(argument)

    # Print the serialized complex object
    print(complex_obj_str)
