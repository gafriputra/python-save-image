import psycopg2
import os
import numpy as np

import concurrent.futures
import sys

from saveToLocal import save_image_comic
from dotenv import load_dotenv
load_dotenv()
'''
Script Untuk Menjalankan SAVE IMAGE thumbnail

python comicsThumbnail.py
'''
conn = psycopg2.connect(
            host=os.environ["DB_HOST"],
            port=os.environ["DB_PORT"],
            database=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASS"]
        )
cursor = conn.cursor()
query = """ SELECT id, title, thumbnail 
            FROM comics 
            WHERE deleted_at is null 
            AND thumbnail not like '%img.y7349.top%' """
print(query)
# Execute Query
cursor.execute(query)
# Get total comic count from query
result_data = cursor.fetchall()
cursor.close()
conn.close()

total_data = len(result_data)
print(total_data)
comic = np.array(result_data)
# max_workers specifies the number of threads. If None then use 5x your CPU count
with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
    # Images we'll save. Depending on how you generate your images you might not
    # want to materialize a list like this to avoid running out of memory.
    image_args = comic
    # Submit futures to the executor pool.
    # Map each future back to the arguments used to create that future. That way
    # if one fails we know which image it was that failed.
    future_to_args = {executor.submit(save_image_comic, image_arg): image_arg for image_arg in image_args}

     # Images are being saved in worker threads. They will complete in any order.
    for future in concurrent.futures.as_completed(future_to_args):
        image_arg = future_to_args[future]
        try:
            result = future.result()
        except Exception as exc:
            pass
            # print("Saving image {} generated an exception: {}".format(image_arg, exc))
        else:
            pass
            # print("Image {} saved successfully.".format(image_arg))z