class Tree:
    def __init__(self, essence, arrondissement, longitude, latitude, **kwargs):
        self.essence = essence
        self.arrondissement = arrondissement
        self.longitude = longitude
        self.latitude = latitude
        self.other_info = kwargs
