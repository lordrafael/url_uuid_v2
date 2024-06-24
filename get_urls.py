import time
import pandas as pd
import requests
import argparse

def read_uuids_from_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        if 'uuid' not in df.columns:
            raise ValueError("CSV file must contain a 'uuid' column")
        return df['uuid'].tolist()
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []

def fetch_urls(base_url, uuids, db):
    results = []
    for uuid in uuids:
        try:
            start_time = time.time()
            response = requests.get(f"{base_url}/{uuid}", params={"db": db})
            elapsed_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                result[elapsed_time] = elapsed_time
                results.append(result)
            else:
                print(f"Failed to fetch URL for UUID {uuid}: {response.status_code} {response.text}")
                results.append({
                    "uuid": uuid,
                    "url": None,
                    "elapsed_time": elapsed_time,
                    "error": response.text
                })
        except Exception as e:
            print(f"Error fetching URL for UUID {uuid}: {e}")
            results.append({
                "uuid": uuid,
                "url": None,
                "elapsed_time": None,
                "error": str(e)
            })
    return results


def main(file_path, base_url, db):
    uuids = read_uuids_from_csv(file_path)
    if not uuids:
        print("No UUIDs to process.")
        return

    results = fetch_urls(base_url, uuids, db)
    
    #df_results = pd.DataFrame(results)
    for result in results:
        print(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read UUIDs from a CSV file and fetch URLs from a FastAPI endpoint.")
    parser.add_argument("file_path", help="Path to the CSV file containing UUIDs")
    parser.add_argument("base_url", help="Base URL of the FastAPI endpoint")
    parser.add_argument("db", help="Database to use ('mysql', 'redis', or 'cache')")
    
    
    args = parser.parse_args()
    main(args.file_path, args.base_url, args.db)
