import basic
import requests
from lxml import etree
import time

crawler = basic.crawlerComponent()
database = basic.dataBase()


'''
book = [['fly into thee air','https:/asaswd/asasd']]
database.add_book(book)
book = [['fly into thee air2','https:/asaswd/asashd','asjasjaksx']]
database.add_book(book)
database.head()
'''


indexLink = []
# initialize the  url
for i in range(2045,2304):
    indexLink.append('http://edu.15kankan.com/class/' + str(i))



def add_one_page_book(indexPageLink):
    resourcePageUrl = []

    page = etree.HTML(requests.get('http://edu.15kankan.com/class/2301',proxies=crawler.get_an_ip(),headers=crawler.get_crawel_header()).content)
    totalPage = int(page.xpath('//*[@id="main-container"]/div/div/div/div[2]/div[2]/span[1]/b/text()')[0])
    totalPage = int((totalPage - totalPage%18)/18 + 1)
    print(totalPage)

    for i in range(1,totalPage):
        individualPageUrl = indexPageLink+'?pg=' + str(i)

        resource = etree.HTML(requests.get(individualPageUrl,proxies=crawler.get_an_ip(),headers=crawler.get_crawel_header()).content)
        # //*[@id="resource-list"]/li[6]/label/a
        # //*[@id="resource-list"]/li[1]/label/a
        for i in range(1,18):
            url = resource.xpath('//*[@id="resource-list"]/li['+str(i)+']/label/a/@href')

            if url == []:
                break

            print(url)

            resourcePageUrl.append('http://edu.15kankan.com/' + url[0])

            time.sleep(0.001)


    print('Already Catched: ' + str(len(resourcePageUrl)) + 'Resources Index\n')
    print('begin to catch the resources url')


    for packetUrl in resourcePageUrl:

        page = etree.HTML(requests.get(packetUrl, proxies=crawler.get_an_ip(),headers=crawler.get_crawel_header()).content)

        '''
        # introduction is static in each page even if it has numerous resources
        introduction = page.xpath('//*[@id="resource_content"]/p[7]/span/text()')

        if introduction == []:
            introduction = ''

        else:
            introduction = introduction[0]

        '''

        liCount = 0

        while True:
            liCount += 1

            url = page.xpath('//*[@id="resource-list"]/li['+str(liCount)+']/label/a/@href')
            title = page.xpath('//*[@id="resource-list"]/li['+str(liCount)+']/label/a/text()')

            if url == [] or title == []:
                break

            item = [title[0],url[0],'','']

            #print('Add book: ' + str(item))
            try:
                database.add_book([item])
            except Exception as e:
                print('Add Error: ' + str(e))
                continue

        time.sleep(0.01)

#add_one_page_book('http://edu.15kankan.com/class/2301')


if __name__ == "__main__":
    catchNumber = input('How many page you want to catch: ')

    input('Enter to Began...')

    for i in indexLink[:catchNumber]:
        add_one_page_book(i)

