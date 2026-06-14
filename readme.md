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

* Checkboxes for bluray, dvd, 4K, Johan, Me
* Check if the data matches the actually ripped movie database
* Add Johan data
* Sort by clicking column head
* Nicer UI


## DVDProfiler -> data

### New way

As of 2026-06-14 there is an upload button that will accept the exported profile data (.xml).

### Old way

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
    parse(r'g:\My Drive\SynkaPrivat\dvd_backup_992_exported_Collection.xml')
```

## Future

The following files are part of an attempt to check the ``content.txt`` (i.e. the file of actual ripped movies)
with the ``data.txt`` that we create from the exported collection in DVD Profiler. The work has just started
and with ``txt_to_data.py`` creating ``extracted_from_txt.txt`` it is clear that neither side is complete.
The xml-based data e.g. has 'Tillbaka till framtiden' trilogy (id 131) as a collection without a english title.
The txt-based data has 'Back to the Future' + II + III, all without an id.

* ``extracted_from_txt.txt``
* ``list_compare.py``
* ``txt_to_data.py``
* ``backups/content.txt``
