import os
import requests
class utils:
    def __init__(self):
        self.secretkey=os.environ.get('SECRET_KEY')
    def get_latlong(self, address):
        """
        calculates the latlong given an address
        :param add:
        :return:
        """
        try:
            r = requests.get(
                "https://www.mapquestapi.com/geocoding/v1/address?key=7cAySSYeXfuO70UE1AypAPALnRnNglJ6&inFormat=kvp&outFormat=json&location= " + address + "&thumbMaps=false")
            data = r.json()
            results = data['results'][0]
            locations = results['locations']
            latlng = locations[0].get('latLng')
            return latlng
        except Exception as identifier:
           return {"lat": -24.90629, "lng": 152.19168}

        
       
