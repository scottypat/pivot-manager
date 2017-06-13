import web

## Url mappings

urls = (
    '/(.*)', 'Index',
    '/weather', 'Weather',
    '/moisture', 'Moisture'
)


### Templates
render = web.template.render('templates', base='basetemp')


class Index:

    def GET(self):   
        
        return render()

        

app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()