import psycopg2
import os

from slugify import slugify

import urllib.request

import sys
from dotenv import load_dotenv

domain = "https://img.y7349.top/"
mainBaseDir = "/home/img.y7349.top/public_html/img/c"
load_dotenv()

def save_image_chapters(chapter):
    # your image save code goes here
    # Start WP API
    chaptersId = chapter[0]
    chapters_content = chapter[2]
    comicTitle = chapter[3]
    comicTitle = str(comicTitle).replace("'","")
    # print(chaptersId,' ', comicTitle)
    comicTitle = slugify(comicTitle)
    chapterSlug = chapter[1]
    chapterSlug = str(chapterSlug).replace("'","")
    chapterSlug = slugify(chapterSlug)
    basedir = 'img/c/'+comicTitle+'/'+chapterSlug+'/'
    filename = comicTitle + '-' + chapterSlug + '-' + 'page-'

    # print("Working on image {}...".format(chapter[0]))
    if not os.path.exists(basedir):
        os.makedirs(basedir)
    # print('makedir')

    content = chapters_content.split(',')
    page = 0
    tampung = []
    for gmbr in content:
        # print(gmbr)
        page = page + 1
        fullFIle = basedir + filename + str(page) + '.jpg'
        gmbr = str(gmbr).strip()
        getSource(gmbr,fullFIle)
        fullFIle = domain + fullFIle
        tampung.append(fullFIle)
        # print(fullFIle)

    tampung = ','.join(tampung)
    # print(tampung)
    print(filename)
    # # Update In Database
    conn = psycopg2.connect(
            host=os.environ["DB_HOST"],
            port=os.environ["DB_PORT"],
            database=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASS"]
        )
    cursor = conn.cursor()
    sql_update_query = """UPDATE chapters SET content = %s WHERE id = %s"""

    try:
        cursor.execute(sql_update_query, (str(tampung), str(chaptersId)))
        conn.commit()
    except:
        cursor.execute(sql_update_query, (str(tampung), str(chaptersId)))
        conn.commit()
    print("update database")
    cursor.close()
    conn.close()
    return True

def save_image_comic_images(comic):
    # your image save code goes here
    # Start WP API
    comicId = comic[0]
    comicTitle = comic[1]
    thumbnail = comic[2]
    banner = comic[3]
    previews = comic[4]
    comicTitle = str(comicTitle).replace("'","")
    comicTitle = slugify(comicTitle)
    basedir = 'img/c/'+comicTitle+'/'

    if not os.path.exists(basedir):
        os.makedirs(basedir)
    # print('makedir')

    fullFIleThumbnail = ""
    # Thumbnail
    if thumbnail:
        fullFIleThumbnail = basedir+"thumbnail-"+comicTitle+".jpg"
        thumbnail = str(thumbnail).strip()
        getSource(thumbnail,fullFIleThumbnail)
        fullFIleThumbnail = domain + fullFIleThumbnail
        print(fullFIleThumbnail)

    fullFIleBanner = ""
    # Banner
    if banner:
        fullFIleBanner = basedir+"banner-"+comicTitle+".jpg"
        banner = str(banner).strip()
        getSource(banner,fullFIleBanner)
        fullFIleBanner = domain + fullFIleBanner
        print(fullFIleBanner)

    # Previews
    tampung = []
    if previews:
        content = previews.split(',')
        page = 0
        for gmbr in content:
            # print(gmbr)
            page = page + 1
            fullFIle = basedir+comicTitle+"-preview-"+str(page)+".jpg"
            gmbr = str(gmbr).strip()
            getSource(gmbr,fullFIle)
            fullFIle = domain + fullFIle
            tampung.append(fullFIle)
            # print(fullFIle)

    tampung = ','.join(tampung)
    # print(fullFIleThumbnail)
    # # Update In Database
    conn = psycopg2.connect(
            host=os.environ["DB_HOST"],
            port=os.environ["DB_PORT"],
            database=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASS"]
        )
    cursor = conn.cursor()
    sql_update_query = """UPDATE comics 
                            SET (thumbnail, banner, previews) = (%s,%s,%s)
                            WHERE id = %s"""
    # print("start")
    comicId = str(comicId)
    print(fullFIleThumbnail,fullFIleBanner,tampung,comicId)
    try:
        cursor.execute(sql_update_query, (fullFIleThumbnail, fullFIleBanner, tampung, comicId))
        conn.commit()
        print(1)
    except:
        cursor.execute(sql_update_query, (fullFIleThumbnail, fullFIleBanner, tampung, comicId))
        conn.commit()
        print(2)
    print("update database")
    cursor.close()
    conn.close()
    return True

def getSource(sourceFrom,savePath):
    opener=urllib.request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)
    sourceFrom = sourceFrom.replace("https","http")
    urllib.request.urlretrieve(sourceFrom, savePath)