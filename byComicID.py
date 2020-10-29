import psycopg2
import os
import numpy as np

import concurrent.futures
import sys

from saveToLocal import save_image_chapters
from dotenv import load_dotenv
load_dotenv()
'''
Script Untuk Menjalankan SAVE IMAGE berdasarkan comic IDnya

python byComicID.py ? ( ? = masukkan IDnya)
'''

comicId = str(sys.argv[1])

conn = psycopg2.connect(
            host=os.environ["DB_HOST"],
            port=os.environ["DB_PORT"],
            database=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASS"]
        )
cursor = conn.cursor()
query = """ SELECT chapters.id, chapters.chapter_title, chapters.content, comics.title 
                FROM chapters INNER JOIN comics ON chapters.comic_id = comics.id 
                WHERE chapters.content IS NOT NULL 
                    AND chapters.content NOT LIKE '%img.y7349.top%' 
                    AND chapters.content not like '' and comics.id = """ + comicId
print(query)


# Execute Query
cursor.execute(query)
# Get total chapters count from query
result_data = cursor.fetchall()
cursor.close()
conn.close()

total_data = len(result_data)
print(total_data)
chapters = np.array(result_data)
# max_workers specifies the number of threads. If None then use 5x your CPU count
with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
    # Images we'll save. Depending on how you generate your images you might not
    # want to materialize a list like this to avoid running out of memory.
    image_args = chapters
    # Submit futures to the executor pool.
    # Map each future back to the arguments used to create that future. That way
    # if one fails we know which image it was that failed.
    future_to_args = {executor.submit(save_image_chapters, image_arg): image_arg for image_arg in image_args}

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
            # print("Image {} saved successfully.".format(image_arg))