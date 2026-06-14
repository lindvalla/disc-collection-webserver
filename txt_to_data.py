from pathlib import Path
import os

def getmedia(path, line):
    dvd = False
    blue = False
    uhd = False
    if path.find('/superseded/')>0:
       #print(f"Superseeded: {path}")
       fs = int(line.split()[4])
       #print(f"   {fs=}")
       if fs > 40_000_000_000:
          uhd = True
          #print("   4K")
       elif fs > 8_000_000_000:
          blue = True
          #print("   bluray")
       else:
          dvd = True
          #print("   dvd")
    else:
        dvd = path.find('/dvd_') > 0
        blue = path.find('/bluray_') > 0
        uhd = path.find('/4K') > 0
    # return dvd, blue, uhd
    return f"{dvd};{blue};{uhd}"

def save(data, fout):
    num = data["cn"]
    title = data["title"]
    media = data["media"]
    orig = ""
    fout.write(f"{num};{media};{title};{orig}\n")

def parse(fname_in):
    with open(fname_in, 'r') as fin, open('extracted_from_txt.txt', 'w') as fout:
        last_path = None
        data = dict()
        for line in fin:
            if line.find('---------------')>=0:
                break
            if line.find('/bluray_series/')>0 or line.find('dvd_series')>0:
                # skip for now
                continue
            if line.find('/demos_trinnov/')>0:
                continue
            if line.rstrip().endswith('johan.txt'):
                continue
            #print(f"Processing {line.strip()}")
            path = line[line.find('/'):].strip()
            #print(f"   {path=}")
            if "path" in data:
                if data["path"] != Path(path).parent:
                    # found a new title without finding the dvdprofiler-data
                    data["cn"] = -1
                    save(data, fout)
                    data = dict()

            if line.find('dvdprofiler_')>0:
                assert("cn" not in data)
                data["cn"] = int(line[line.find('dvdprofiler'):].split('_')[1])
                #print(f"   {data['cn']=}")
            else:
                assert("media" not in data)
                data["title"] = Path(path).stem
                data["media"] = getmedia(path, line)
                #print(f"   {data['title']=}")
                #print(f"   {data['media']=}")
            data["path"] = Path(path).parent
            if "cn" in data and "media" in data:
                save(data, fout)
                data = dict()

'''
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
'''

if __name__=='__main__':
    parse('backups/content.txt')
