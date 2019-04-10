from bs4 import BeautifulSoup
import urllib.request
import re
import sys
def parseHtml(content):
    soup = BeautifulSoup(content,'html.parser')
    sentencenodes = soup.select('.sentence')
    subs = []
    for sentence in sentencenodes:
        # link like "/videos/play/wwdc2018-503/?time=23"
        #link = sentence['href']
        timenode = sentence.select('span')[0]
        data_start = float(timenode['data-start'])
        data_end = float(timenode['data-end'])
        subs.append((timenode.string.strip('\n '),data_start,data_end))
    return subs

        

def downloadHtml(url):
    response = urllib.request.urlopen(url)
    data = response.read()
    text = data.decode('utf-8')
    return text
def seconds2string(seconds):
    hour = (int)(seconds / 3600.0)
    seconds = seconds - hour * 3600.0
    minute = (int )(seconds / 60)
    seconds = seconds - minute * 60.0
    return "%02d:%02d:%02d" %(hour,minute,seconds)

def getSrtName(hdcode,conent):
    pattern = '(' + hdcode + r"_hd_.*)\.mp4"
    print(pattern)
    pat = re.compile(pattern)
    matches = pat.search(content)
    text = matches.group(1)
    return text + ".srt"
def writeSubtitles(subs,newfilename):
    index = 0
    with open(newfilename,"w") as filew:
        for sub in subs:
            if sub[0] == "":
                continue
            index = index + 1
            
            filew.write("%d\n" % index)
            
            #transform to 00:00:22,524
            time_start = seconds2string(sub[1])
            time_end = seconds2string(sub[2])
            time_start = time_start + ",000"
            if (sub[1] == sub[2]):
                time_end = time_end + ",999"
            else:
                time_end = time_end + ",000"

            time_str = "%s --> %s \n" % (time_start,time_end)
            filew.write(time_str)
            filew.write(sub[0])
            filew.write('\n\n')
            
                


            
def printUsage():
    print("download.py <hdcode> [year]")
    print("et.")
    print("download.py 219")
    print("download.py 219 2018")


if __name__ == "__main__":
    year = "2018"
    hdcode = "219"
    count = len(sys.argv)
    if count == 1:
        printUsage()
        quit(0)
    if count > 1:
        hdcode = sys.argv[1]
    if count > 2:
        year = sys.argv[2]
    if count > 3:
        printUsage()
        quit(0)

    

    content = downloadHtml("https://developer.apple.com/videos/play/wwdc%s/%s/" %(year,hdcode))
    filename = getSrtName(hdcode,content)
    subs = parseHtml(content)
    writeSubtitles(subs,filename)