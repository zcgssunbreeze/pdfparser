from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.layout import LAParams
from pdfminer.converter import XMLConverter


def parse_pdf_to_txt(pdf_handle, write_file):
    pagenos = set()
    maxpages = 0
    codec = 'utf-8'
    caching = True
    laparams = LAParams()
    #laparams.all_texts = True
    laparams.detect_vertical = True

    # 创建pdf资源管理器 来管理共享资源
    rsrcmgr = PDFResourceManager(caching = caching)

    print("ready to open out file ........")
    with open(write_file, "wt", encoding = codec, errors = 'ignore') as outfp:
        device = XMLConverter(rsrcmgr, outfp, laparams = laparams)
        print("ready to converte pdf to xml ........")
        process_pdf(rsrcmgr, device, pdf_handle, pagenos, maxpages=maxpages, password='', caching=caching, check_extractable=True)
        device.close()

if __name__ == '__main__':
    with open('01.pdf', 'rb') as pdfhandle:
        parse_pdf_to_txt(pdfhandle, '01.xml')