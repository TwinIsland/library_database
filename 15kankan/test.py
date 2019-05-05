import basic


tools = basic.tools()
crawler = basic.crawlerComponent()
token = ''


test = 'https://u19481746.pipipan.com/fs/19481746-372048608'

result = tools.solveCtLink(test,crawler)

if result != 'error':
    link = tools.shortLink(result,token,crawler)
else:
    link = 'error'

print(link)
