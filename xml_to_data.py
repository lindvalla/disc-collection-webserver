import os
import shutil
import xml.etree.ElementTree as ET

def getmedia(node):
    dvd = node.find('DVD').text == 'true'
    blue = node.find('BluRay').text == 'true'
    uhd = node.find('UltraHD').text == 'true'
    # return dvd, blue, uhd
    return f"{dvd};{blue};{uhd}"

def sanity_check_the_xml(fs):
    #print(f"{fs=}")
    data = fs.read(1000).decode('iso-8859-1')
    if data.find('DVD Profiler Collection Export') < 0:
        raise ValueError("Could not find 'DVD Profiler Collection Export' in selected file")
    # move file pointer back to the start
    fs.stream.seek(0)


def parse(fs):
    sanity_check_the_xml(fs)
    tree = ET.parse(fs)
    root = tree.getroot()
    with open('extracted.txt', 'w') as fout:
        i = 0
        for child in root:
            i+=1
            title = child.find('Title').text
            orig = child.find('OriginalTitle').text
            if orig is None:
                orig=''
            cn = child.find('CollectionNumber').text
            if cn is None:
                # print(title, 'has no collection number')
                num = -1
            else:
                num = int(cn)
            media = getmedia(child.find('MediaTypes'))
            if num != -1 and title.startswith('24: Season'):
                print(i, num, media, title, orig)
            # if i == 5:
            #     break
            if num != -1:
                fout.write(f"{num};{media};{title};{orig}\n")

# Takes a flask FileStorage object in
def backup_then_parse(fs):
    os.makedirs('backups', exist_ok=True)
    if os.path.exists('extracted.txt'):
        shutil.move('extracted.txt', 'backups/extracted.txt.old')
    with open('extracted.txt', 'w') as f:
        pass
    parse(fs)
    for i in reversed(range(5)):
        src = f"backups/data.txt.old{i}"
        dst = f"backups/data.txt.old{i+1}"
        if os.path.exists(src):
            shutil.move(src, dst)
    shutil.copy("data.txt", "backups/data.txt.old0")
    shutil.move("extracted.txt", "data.txt")

