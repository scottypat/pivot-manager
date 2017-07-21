import web
import model

## Url mappings

urls = (
    "/", "Index",
    "/moisture", "Moisture"
)


### Templates
render = web.template.render('templates', base='basetemp')


class Index:

    def GET(self):   
        
        return render.index()
               
class Moisture:

    def GET(self):
        
        delta = web.input(weekDelta=None)
        if delta.weekDelta == None:
            weekOffset = 4
        else:
            weekOffset = int(delta.weekDelta)
                           
        moistureData = model.getMoistureData(weekOffset)        
        moistureData = model.orgMoistureData(moistureData)        
        return render.moisture(moistureData)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()