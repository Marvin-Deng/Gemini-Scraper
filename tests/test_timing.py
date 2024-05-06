import requests
import json
import time


def send_post_request():
    print("Starting time test.")
    url = "http://127.0.0.1:8000/crawl/"
    headers = {"Content-Type": "application/json"}
    data = {
        "url": "https://en.wikipedia.org/wiki/Apple_Inc.",
        "topics": [
            "Early days of the company",
            "List of products",
            "Important people in the company",
        ],
        "max_depth": 2,
    }
    output_filename = "response.json"
    start_time = time.time()
    response = requests.post(url, headers=headers, json=data)
    end_time = time.time()
    duration = end_time - start_time
    print(f"Total time: {duration:.3f} seconds")

    if response.status_code == 200:
        with open(output_filename, "w") as file:
            json.dump(response.json(), file, indent=4)
        print(f"Response JSON has been written to {output_filename}")
    else:
        print(f"Failed to get a valid response: {response.status_code}")


if __name__ == "__main__":
    send_post_request()
