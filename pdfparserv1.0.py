from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.converter import PDFPageAggregator


def from_pdf_to_txt(read_file, write_file, page_start=0, page_end=0):
    """

    :param read_file: str. 注意后缀名是".pdf"
    :param write_file: str. 注意后缀名填".txt"
    :param page_start: int
    :param page_end: int
    :return:
    """
    
    # 以二进制读模式打开
    origin_pdf_file = open(read_file, 'rb')
    # 用文件对象来创建一个pdf文档分析器
    parser = PDFParser(origin_pdf_file)
    # 创建一个pdf文档
    doc = PDFDocument()
    # 连接分析器与文档对象,这个语句比较有意思,相互set对方进去
    parser.set_document(doc)
    doc.set_parser(parser)
    
    # 提供初始化密码.如果pdf没有密码,就传入一个空参数
    doc.initialize()
    
    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        # 如果pdf不支持提取,则直接报错
        raise PDFTextExtractionNotAllowed
    else:
        # 创建pdf资源管理器 来管理共享资源
        srcmgr = PDFResourceManager()
        # 创建一个pdf设备对象
        device = PDFPageAggregator(srcmgr, laparams=LAParams())
        # 创建一个pdf解释器对象
        interpreter = PDFPageInterpreter(srcmgr, device)
        
        # 循环遍历列表，每次处理一个page的内容
        pages = list(doc.get_pages())
        if page_end == 0:
            page_end = len(pages)
        
        for i in range(page_start, page_end):
            interpreter.process_page(pages[i])
            
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里返回的是一个LTPage对象,里面存放着这个page解析出的各种对象
            # 一般包括LTTextBox,LTFigure,LTImage,LTTextBoxHorizontal等等
            # 想要获取文本就取它的text属性,即x.get_text()
            
            # 获取text属性
            for x in layout:
                if isinstance(x, LTTextBoxHorizontal):
                    with open(write_file, 'a', encoding='utf-8') as f:
                        results = x.get_text()
                        f.write(results + '\n')
        
        # 最后关闭原始pdf文件
        origin_pdf_file.close()


def test():
    from_pdf_to_txt('02.pdf', 'output2.txt', 0, 1)


if __name__ == '__main__':
    test()