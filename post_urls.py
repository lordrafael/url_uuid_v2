import requests
import pandas as pd


def post_url(url):
    endpoint = "http://127.0.0.1:8000/process_url/" 
    response = requests.post(endpoint, data={"url": url})
    if response.status_code == 200:
        response_json = response.json()
        print(f"Successfully processed URL: {url}, UUID: {response_json['uuid']}")
        return response_json
    else:
        print(f"Failed to process URL: {url}, Status Code: {response.status_code}, Error: {response.json()}")
        return None


def read_urls_from_csv(file_path):
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise ValueError("Can't read file : {e}")
    
    if 'url' not in df.columns:
        raise ValueError("CSV file must contain a 'url' column")
    
    return df['url'].tolist()

def read_url_from_txt(file_path):
    try:
        with open(file_path, 'r') as file:
            urls = [line.strip() for line in file.readline() if line.strip()]
        return urls
    except Exception as e;
    raise ValueError (f"Error reading the text file")

def post_urls_sequentially(urls):
    
    for url in urls:
        response_json = post_url(url)
        if response_json:
           print("URLs storeddddddddddddd")
    
if __name__ == "__main__":

    file_path = "/home/rafael/Downloads/urls.csv"
    urls = read_urls_from_csv(file_path)
    post_urls_sequentially(urls)


