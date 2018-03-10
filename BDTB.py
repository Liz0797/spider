import urllib2
import urllib
import re
class BDTB:
    def __init__(self, baseUrl, seeLZ, floorTag):
        self.baseUrl = baseUrl
        self.seeLZ = '?see_lz='+str(seeLZ)
        self.tool = Tool()
        self.file = None
        self.floor = 1
        self.floorTag = floorTag

    def getPage(self, pageNum):
        try:
            url = self.baseUrl + self.seeLZ + '&pn=' + str(pageNum)
            #print url
            request =  urllib2.Request(url)
            response = urllib2.urlopen(request)
            #print response.read()
            return response.read().decode('utf-8')
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print e.reason
                return None
    
    def getTitle(self):
        #print page_html.read()
        page = self.getPage(1)
        #print 'this is page',page
        pattern = re.compile('<h3.*?>(.*?)</h3>',re.S)
        result = re.search(pattern,page)
        if result:
            #print 'This is group0',result.group(0)
            print 'Title',result.group(1)
            return result.group(1).strip()
        else:
            print 'error'
            return None
    def getPageNum(self):
        page = self.getPage(1)
        pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>')
        result = re.search(pattern,page)
        if result:
            print 'PageNum',result.group(1).strip()
            #print 'group2',result.group(2)
            return result.group(1).strip()
        else:
            return None

    def getContent(self, pageHtml):
        pattern = re.compile('<div id="post_content.*?>(.*?)</div>',re.S)
        items = re.findall(pattern, pageHtml)
        #floor = 1
        #print self.tool.replace(items[1])
        contents = []
        for item in items:
            #print floor,'---------------------------'
            #print self.tool.replace(item)
            #floor += 1
            content = '\n' + self.tool.replace(item) + '\n'
            contents.append(content.encode('utf-8'))
        return contents
     
    def setFileTitle(self, title):
        if title is not None:
            self.file = open(title + '.txt', 'w+')
        else:
            self.file = open('BDTB_Spider.txt', 'w+')
  
    def writeData(self, contents):
        for item in contents:
            if self.floorTag == '1':
                floorLine = '\n' + str(self.floor) + u'---------------------    \n'
                self.file.write(floorLine)
            self.file.write(item)
            self.floor += 1
    def start(self):
        indexPage = self.getPage(1)
        pageNum = self.getPageNum()
        title = self.getTitle()
        self.setFileTitle(title)
        if pageNum == None:
            print 'error pageNum'
            return
        try:
            print 'total',str(pageNum),'page'
            for i in range(1, int(pageNum)+1):
                print 'Write',str(i),'page'
                page = self.getPage(i)
                contents = self.getContent(page)
                #print contents
                self.writeData(contents)
        except IOError,e:
            print 'Error Reason',e
        finally:
            print 'write over'
class Tool:
    removeImg = re.compile('<img.*?>| {7}|')
    removeAddr = re.compile('<a.*?>|</a>')
    repalceLine = re.compile('<tr>|<div>|</div>|</p>')
    replaceTD = re.compile('<td>')
    replacePara = re.compile('<p.*?>')
    replaceBR = re.compile('<br><br>|<br>')
    removeExtraTag = re.compile('<.*?>')
    def replace(self, x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.repalceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        return x.strip()
baseUrl = 'http://tieba.baidu.com/p/3138733512'
bdtb = BDTB(baseUrl,1,'1')
bdtb.getPageNum()
bdtb.start()