
import folium

class AssetMap:
    file_ext = "*.json"
    def __init__(self):
        self.map = folium.Map(
            location=[37.6485, -118.9721],
            # tiles="Stamen Toner",
            tiles="Stamen Terrain",
            zoom_start=6
        )

    def vega_img(self):
        import base64
        from folium import IFrame
        encoded = base64.b64encode(open("img/a.png", 'rb').read()).decode()        
        html = '<img src="data:image/png;base64,{}">'.format
        resolution, width, height = 1, 450, 250
        iframe = IFrame(html(encoded), width=(width*resolution)+20, height=(height*resolution)+20)
        popup = folium.Popup(iframe, max_width=2650)
        
        icon = folium.Icon(color="red", icon="ok")
        return popup, icon

    def add_collection(self, collection):
        pass

    def proc_event(self, *args, **kwds):
        import quakeio
        import quakeio.vega
        record = quakeio.read("events/58658_007_20210426_10.09.54.P.zip")
        plot = folium.Vega(quakeio.vega.record2vega(record["abutment_1"]["tran"]),
                width=450, height=250
        )

        folium.Marker(
            location=[40.5031, -124.1009],
            #popup="Painter Street Overpass",
            popup=self.vega_test(),
            radius=1000,
            color="crimson",
            fill=False,
        ).add_to(self.map)
        
        folium.Marker(
            location=[37.6907, -122.0993],
            popup="Hayward Hwy 580/238 Interchange",
            radius=1000,
            color="crimson",
            fill=False,
        ).add_to(self.map)

        pop, ico = self.vega_img()
        folium.Marker(
            location=[32.7735, -115.4481],
            #popup="Meloland Overpass",
            color="crimson",
            radius=1000,
            fill=False,
            popup=pop, icon=ico
            #popup=folium.Popup(max_width=450).add_child(plot)
            #color="#3186cc",
            #fill=True,
            #fill_color="#3186cc",
        ).add_to(self.map)
 
        #return {"content": m.get_root().render()}
        #return {"content": m._repr_html_()}
        return {"content": self.map._repr_html_()}


