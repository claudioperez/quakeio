
from brace2.plugins import BaseEvent
import folium


class AssetMap(BaseEvent):
    file_ext = "*.json"

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

    def vega_test(self):
        import json
        import requests
        url = (
            "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data"
        )
        vis1 = json.loads(requests.get(f"{url}/vis1.json").text)
        vis2 = json.loads(requests.get(f"{url}/vis2.json").text)
        vis3 = json.loads(requests.get(f"{url}/vis3.json").text)

        #m = folium.Map(location=[46.3014, -123.7390], zoom_start=7, tiles="Stamen Terrain")

        #folium.Marker(
        #    location=[47.3489, -124.708],
        #    popup=folium.Popup(max_width=450).add_child(
        #        folium.Vega(vis1, width=450, height=250)
        #    ),
        #).add_to(m)

        #folium.Marker(
        #    location=[44.639, -124.5339],
        popup=folium.Popup(max_width=450).add_child(
                folium.Vega(vis2, width=450, height=250))
        #    ),
        #).add_to(m)

        #folium.Marker(
        #    location=[46.216, -124.1280],
        #    popup=folium.Popup(max_width=450).add_child(
        #        folium.Vega(vis3, width=450, height=250)
        #    ),
        #).add_to(m)
        return popup

    def proc_event(self,*args, **kwds):
        import quakeio
        import quakeio.vega
        record = quakeio.read("events/58658_007_20210426_10.09.54.P.zip")
        plot = folium.Vega(quakeio.vega.record2vega(record["abutment_1"]["tran"]),
                width=450, height=250
        )


        m = folium.Map(
            #location=[45.5236, -122.6750],
            #location=[37.8715, -122.2730],
            location=[37.6485, -118.9721],
            # tiles="Stamen Toner",
            tiles="Stamen Terrain",
            zoom_start=6
        )

        folium.Marker(
            location=[40.5031, -124.1009],
            #popup="Painter Street Overpass",
            popup=self.vega_test(),
            radius=1000,
            color="crimson",
            fill=False,
        ).add_to(m)
        
        folium.Marker(
            location=[37.6907, -122.0993],
            popup="Hayward Hwy 580/238 Interchange",
            radius=1000,
            color="crimson",
            fill=False,
        ).add_to(m)

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
        ).add_to(m)

        
        #return {"content": m.get_root().render()}
        return {"content": m._repr_html_()}


