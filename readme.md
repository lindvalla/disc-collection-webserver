# Movie search program

Can reach it over nordvpn meshnet as

http://anders.xa.lindvall-olympic.nord:5000/

or on home network as

http://raspi-proj-dev.dreadlands:5000/


## Start after Pi reboot:

``screen -S movies``

Rename tab to webserver Ctrl-a Ctrl-A

```bash
cd projects/movie_filter
. .venv/bin/activate
python app.py
```

Create a second tab, Ctrl-a -Ctrl-c

```bash
cd projects/movie_filter
```


## Todo

* checkboxes for bluray, dvd, 4K, Johan, Me

* Check if the data matches the actually ripped movie database

* Add Johan data


## DVDProfiler -> data

The tool to extract movie list from dvd profiler exported data is:

```python
import xml.etree.ElementTree as ET

def getmedia(node):
    dvd = node.find('DVD').text == 'true'
    blue = node.find('BluRay').text == 'true'
    uhd = node.find('UltraHD').text == 'true'
    # return dvd, blue, uhd
    return f"{dvd};{blue};{uhd}"

def parse(fname):
    tree = ET.parse(fname)
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

if __name__=='__main__':
    parse(r'g:\My Drive\SynkaPrivat\dvd_backup_980_exported_Collection.xml')
```
