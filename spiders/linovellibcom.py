import httputils
import basespider
import asyncio

from bs4 import BeautifulSoup

# url is a category url, like https://www.linovelib.com/novel/2796/catalog
class LinovellibCom(basespider.BaseSpider):
    def __init__(self):
        super().__init__()

    def load(self, url, path):
        super().load(url, path)
        self.process_book(url)

    def process_book(self, url):
        loop = asyncio.get_event_loop()

        print('loading page %s' % (url))
        html = loop.run_until_complete(httputils.get(url))

        soup = BeautifulSoup(html, 'html.parser')

        book_meta = soup.find(class_='book-meta')
        id = url.split('/')[-2]
        title = book_meta.find('h1').text
        author = book_meta.find('p').find_all('span')[0].find('a').text
        update_date = book_meta.find('p').find_all('span')[1].text

        print('Novel Name: %s Author: %s' % (title, author))
        all_chapters = soup.find_all('li', class_='col-4')

        print('find %d chapters, starting to process' % len(all_chapters))
        # loop.run_until_complete(self.process_chapter(
        #     self.base_url + all_chapters[0].find('a')['href']))

        tasks = []
        for i, chapter in enumerate(all_chapters):
            chapter_url = self.base_url + chapter.find('a')['href']
            chapter_name = chapter.find('a').text
            tasks.append(asyncio.ensure_future(
                self.process_chapter(i, chapter_name, chapter_url)))

        result, b = loop.run_until_complete(asyncio.wait(tasks))

        chapters_metas = list(filter(lambda x: x != None, [x.result() for x in result]))
        chapters_metas = sorted(chapters_metas, key=lambda x: x[0])
        chapters_metas = [(x[1], x[2]) for x in chapters_metas]

        super().generate_ncx(title, chapters_metas)
        super().generate_opf(author, title, chapters_metas)

    async def process_chapter(self, index, chapter_name, chapter_url, persist=True):
        if not chapter_url.endswith('.html'):
            print('chapter %s has no available url' % chapter_name)
            return

        print('processing chapter: %s[%s]' % (chapter_name, chapter_url))
        chapter_content = await httputils.get(chapter_url)
        page = BeautifulSoup(chapter_content, 'html.parser')
        id = chapter_url.split('/')[-1].split('.')[0]
        html_file_name = 'chapter_' + id + '.html'
        title = page.find('h1').text.strip(' ')
        a_tag = page.find('a')
        chapter_title = a_tag.text.strip(' ')
        chapter_url = self.base_url + a_tag['href']

        contents = []

        div_tag = page.find('div', id='TextContent')
        p_tags = div_tag.find_all()

        for p in p_tags:
            if p.name == 'div':
                if p.get('class')[0] == 'divimage':
                    contents.append(('img', p.find('img')['src']))
                pass
            elif p.name == 'p':
                if p.get('style') != None:
                    next_chapter_url = page.find(
                        'p', class_='mlfy_page').find_all('a')[-1]['href']
                    content = await self.process_chapter(index, chapter_name, self.base_url+next_chapter_url, False)
                    contents.extend(content)
                elif p.text != '':
                    contents.append(('txt', p.text))

        if persist:
            basespider.BaseSpider.persist_chapter(
                self, title, contents, html_file_name)
            print('finish chapter: %s[%s]' % (chapter_name, chapter_url))
        else:
            return contents

        return index, title, html_file_name


if __name__ == '__main__':
    a = LinovellibCom()
    # a.load('https://www.linovelib.com/novel/73/catalog', './小书痴.epub')
    a.load('https://www.linovelib.com/novel/2796/catalog', './平均值.epub')
