import os

from requests.api import head
import httputils
import datetime
import zipfile
import os.path

class BaseSpider:
    def __init__(self):
        super().__init__()
        self.host = ''
        self.base_url = ''
        self.output_dir = ''

    def load(self, url, path):
        self.output_dir = path
        url_segments = url.split('/')
        self.host = url_segments[2]
        self.base_url = url_segments[0]+'//'+url_segments[2]

        
        os.makedirs(os.path.dirname(self.output_dir), exist_ok=True)
        # os.makedirs(self.output_dir+'/META-INF', exist_ok=True)
        # os.makedirs(self.output_dir+'/images/', exist_ok=True)
        # os.makedirs(self.output_dir+'/chapters/', exist_ok=True)

        self.zfile = zipfile.ZipFile(path, 'w')

        self.zfile.writestr('mimetype', 'application/epub+zip', compress_type=zipfile.ZIP_STORED)
        # with open(self.output_dir+'/mimetype', 'w') as f:
        #     f.write('application/epub+zip')
        self.zfile.writestr('META-INF/container.xml', '''
<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
   <rootfiles>
      <rootfile full-path="content.opf" media-type="application/oebps-package+xml"/>
   </rootfiles>
</container>''', compress_type=zipfile.ZIP_STORED)
#         with open(self.output_dir+'/META-INF/container.xml', 'w') as f:
#             f.write('''
# <?xml version="1.0"?>
# <container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
#    <rootfiles>
#       <rootfile full-path="content.opf" media-type="application/oebps-package+xml"/>
#    </rootfiles>
# </container>''')

    def persist_chapter(self, title, contents, filename):
        template = '''
        <HTML>
        <HEAD>
        </HEAD>
        <BODY>
        '''
        tail = '''
        </BODY>
        </HTML>
        '''
        # file = open(self.output_dir+'/chapters/' +
        # filename, 'w', encoding="utf8")

        buffer = ''
        # file.write(template)
        # file.write('<H1>%s</H1>' % title)
        # file.write('<DIV id="content">')

        buffer += (template)
        buffer += ('<H1>%s</H1>' % title)
        buffer += ('<DIV id="content">')

        for line in contents:
            if line[0] == 'txt':
                # file.write('<P>%s</P>' % line[1])
                buffer += ('<P>%s</P>' % line[1])
            elif line[0] == 'img':
                img_content = httputils.image(line[1])
                self.zfile.writestr(
                    'images/'+line[1].split('/')[-1], img_content, compress_type=zipfile.ZIP_STORED)
                # with open(self.output_dir+'/images/' + line[1].split('/')[-1], 'wb') as f:
                #     f.write(img_content)
                # file.write('<P><IMG SRC="%s"/></P>' %
                #            ('../images/' + line[1].split('/')[-1]))
                buffer += ('<P><IMG SRC="%s"/></P>' %
                           ('../images/' + line[1].split('/')[-1]))
        buffer += ('</DIV>')
        buffer += (tail)

        # file = open(self.output_dir+'/chapters/' +
        # filename, 'w', encoding="utf8")

        self.zfile.writestr('chapters/'+filename, buffer,
                            compress_type=zipfile.ZIP_STORED)
        # file.write('</DIV>')
        # file.write(tail)
        # file.close()

    def generate_opf(self, author, book_title, chapters):
        #         with open(self.output_dir+'content.opf', 'w', encoding="utf8") as f:
        #             f.write('''<?xml version='1.0' encoding='utf-8'?>
        # <package xmlns="http://www.idpf.org/2007/opf" unique-identifier="uuid_id" version="2.0">
        #   <metadata xmlns:calibre="http://calibre.kovidgoyal.net/2009/metadata" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:opf="http://www.idpf.org/2007/opf" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        #     <dc:creator>%s</dc:creator>
        #     <dc:language>zh</dc:language>
        #     <dc:title>%s</dc:title>
        #     <dc:identifier id="uuid_id" opf:scheme="uuid">c0edc2b6-488d-4d50-a57f-01757285a222</dc:identifier>
        #     <meta name="cover" content="cover"/>
        #   </metadata>
        #   ''' % (author, book_title))
        #             f.write('<manifest>')
        #             f.write(
        #                 '<item href="cover_image.jpg" id="cover" media-type="image/jpeg"/>\n')

        #             for i, chap in enumerate(chapters):
        #                 f.write(
        #                     '<item href="chapters/%s" id="html%d" media-type="application/xhtml+xml"/>\n' % (chap[1], i))

        #             f.write(
        #                 '<item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml"/>')
        #             f.write('''
        #     </manifest>
        #     <spine toc="ncx">
        #   ''')
        #             for i, chap in enumerate(chapters):
        #                 f.write(
        #                     '<itemref idref="html%d"/>\n' % i)
        #             f.write('</spine>')
        #             f.write('</package>')
        buffer = ''
        buffer += ('''<?xml version='1.0' encoding='utf-8'?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="uuid_id" version="2.0">
    <metadata xmlns:calibre="http://calibre.kovidgoyal.net/2009/metadata" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:opf="http://www.idpf.org/2007/opf" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <dc:creator>%s</dc:creator>
        <dc:language>zh</dc:language>
        <dc:title>%s</dc:title>
        <dc:identifier id="uuid_id" opf:scheme="uuid">c0edc2b6-488d-4d50-a57f-01757285a222</dc:identifier>
        <meta name="cover" content="cover"/>
    </metadata>
''' % (author, book_title)) 
        buffer += '''
    <manifest>
        <item href="cover_image.jpg" id="cover" media-type="image/jpeg"/>
        <item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml"/>
'''

        for i, chap in enumerate(chapters):
            buffer += (
                '       <item href="chapters/%s" id="html%d" media-type="application/xhtml+xml"/>\n' % (chap[1], i))
        buffer += '''
    </manifest>
    <spine toc="ncx">
'''
        for i, chap in enumerate(chapters):
            buffer += (
                '           <itemref idref="html%d"/>\n' % i)
        buffer += ('        </spine>')
        buffer += ('</package>')

        self.zfile.writestr('content.opf', buffer,
                            compress_type=zipfile.ZIP_STORED)

    def generate_ncx(self, book_title, chapters): 
        buffer = ''
        buffer += '''<?xml version='1.0' encoding='utf-8'?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="zh-CN">
    <head>
        <meta content="NOVEL_SPDIER_PY" name="generator"/>
    </head>
'''
        buffer += ('''
    <docTitle>
        <text>%s</text>
    </docTitle>
''' % book_title)

        buffer += '''
    <navMap>
'''
        chapter_template = '''
        <navPoint id="id_%d" playOrder="%d">
            <navLabel>
                <text>%s</text>
            </navLabel>
            <content src="chapters/%s"/>
        </navPoint>
'''
        for i, chap in enumerate(chapters):
            buffer += (chapter_template % (i, i, chap[0], chap[1]))
        buffer += ('</navMap>')
        buffer += ('</ncx>')
        self.zfile.writestr('toc.ncx', buffer, compress_type=zipfile.ZIP_STORED)
