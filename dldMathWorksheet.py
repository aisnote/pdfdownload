# coding:utf-8
import re
import requests
import threading
import urllib
import tempfile
import shutil
import sys
import time

g_site = r'https://beestar.org/worksheets/'
g_site_grads = ['grade_01.jsp',
                'grade_02.jsp',
                'grade_03.jsp',
                'grade_04.jsp',
                'grade_05.jsp',
                'grade_06.jsp',
                'grade_07.jsp',
                'grade_08.jsp']

pdf_links = []
have_visited_links = []


def checkVisitedLinks(url):
    for item in have_visited_links:
        if cmp(item, url) == 0:
            return True
    have_visited_links.append(url)
    return False


def AppendPdfLinks(pdflink):
    for item in pdf_links:
        if cmp(item, pdflink) == 0:
            return
    pdf_links.append(pdflink)


def downloadPdf(url):
    if str(url).find(g_site) < 0:
        return

    if checkVisitedLinks(url) == True:
        return

    if url.find('.css') > 0:
        return

    if url.find('.php') > 0:
        return

    # if url.find('flashcards') < 0:
    #    return

    print(url)

    r = requests.get(url)
    data = r.text

    # use regular to find
    link_list = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", data)
    i = 0;
    for urlitem in link_list:

        # if str(urlitem).find(g_site) < 0  :
        #    continue

        if urlitem.find(r'/') > 0:
            newUrl = url + urlitem
            print(newUrl)
            downloadPdf(newUrl)

        if urlitem.find(".pdf") > 0:
            pdfUrl = url + urlitem
            AppendPdfLinks(pdfUrl)  # pdf_links.append(urlitem);
            # else:
            #    downloadPdf(urlitem)


def chunk_report(bytes_so_far, chunk_size, total_size):
    percent = float(bytes_so_far) / total_size
    percent = round(percent * 100, 2)
    sys.stdout.write("Downloaded %d of %d bytes (%0.2f%%)\r" %
                     (bytes_so_far, total_size, percent))

    if bytes_so_far >= total_size:
        sys.stdout.write('\n')


def chunk_read(response, destFile, chunk_size=8192, report_hook=None):
    #total_size = response.info().getheader('Content-Length').strip()
    total_size = response.length
    total_size = int(total_size)
    bytes_so_far = 0

    tempFile = tempfile.mktemp()
    handle = open(tempFile, 'wb')

    while 1:
        chunk = response.read(chunk_size)
        bytes_so_far += len(chunk)

        if not chunk:
            break

        if report_hook:
            report_hook(bytes_so_far, chunk_size, total_size)

        handle.write(chunk)

    handle.close()
    # done
    shutil.copyfile(tempFile, destFile)
    return bytes_so_far


def dldPdf(pdfLink, destFile):
    response = urllib.request.urlopen(pdfLink)
    chunk_read(response, destFile, report_hook=chunk_report)

    # h1 = httplib.HTTPConnection(headerlib_server);
    # if h1 <> 0:
    #    h1.request("GET", "")
    # tempFile = urllib.urlretrieve(headerlib_server);
    # files = urllib2.urlopen(headerlib_server).read().splitlines()
    # for l in files[:4]: print l
    # soup = BeautifulSoup(open(tempFile[0]))

    # tempFile[0].close()
    # print(soup.prettify())


def dldPdf_thread(pdfLink, destDir):
    thread_list = []
    for i in range(1):
        thread_list.append(threading.Thread(target=dldPdf, args=(pdfLink, destDir,)))
    for a in thread_list:
        a.start()

    for a in thread_list:
        a.join()


if __name__ == '__main__':
    """
    svnusername  = sys.argv[1]
    svnpassword = sys.argv[2]
    """

    target = g_site + g_site_grads[3]
    req = requests.get(url=target)
    data = req.text

    destDir = "/Users/liuliu/math_worksheets/"

    # use regular to find
    link_list = re.findall(r"(?<=href=\").+?(?=\.pdf\")|(?<=href=\').+?(?=\.pdf\')", data)
    i = 0;
    for urlitem in link_list:
        pdfLink = urlitem + ".pdf"
        print (pdfLink)

        pdfBaseLink = pdfLink[0:pdfLink.rfind("/")+1]

        pdfName = pdfLink[pdfLink.rfind("/") + 1: len(pdfLink)]

        urlpdfName = urllib.parse.quote(pdfName)

        pdfLink = pdfBaseLink + urlpdfName

        destFile = destDir + pdfName

        #pdfLink = urllib.parse.quote(pdfLink)
        print ("new link:" + pdfLink)

        dldPdf_thread(pdfLink, destFile)

        time.sleep(10)
        #break

    #print(req.text)


    # downloadPdf(r'http://www.kids-pages.com/folders/flashcards/')
    # downloadPdf(r'http://www.kids-pages.com/folders/alphabet/')
    # downloadPdf(g_site)
    # write pdf links to file.
    # AppendPdfLinks("c:/test/test.pdf")
    # destDir = "C:\\test\\flashcards\\"
    # output = open(r"c:\test\pdf.txt",'w')
    # for url in pdf_links:
    #     output.write(url)
    #     output.write('\n')
    #     print (url)
    #     pdfName=''
    #     index = url.rfind(r'/')
    #     nLen = len(url)
    #     pdfName = url[index+1:nLen]
    #
    #     pdfName = destDir + pdfName
    #     dldPdf_thread(url,pdfName)
    # output.close()

