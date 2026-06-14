
def extract(fname):
    all = {}
    with open(fname, 'r') as f:
       for line in f:
           cn = int(line.split(';')[0])
           if cn not in all:
               all[cn] = list()
           all[cn].append(line.strip())
    return all

def print_duplicates(lst, header):
    print(header)
    for cn in sorted(lst):
        if len(lst[cn])>1:
           print(f"   {cn=}")
           for v in lst[cn]:
               print(f"      {v}")

def compare(fname_xml, fname_txt):
    x = extract(fname_xml)
    t = extract(fname_txt)

    print_duplicates(x, "From XML - Duplicates")
    print_duplicates(t, "From TXT - Duplicates")


if __name__=='__main__':
    from_xml = 'data.txt'
    from_txt = 'extracted_from_txt.txt'
    compare(from_xml, from_txt)
