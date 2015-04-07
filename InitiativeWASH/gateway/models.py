from django.db import models
import math

class Neighborhood(models.Model):
    """ Corresponds to a neighborhood that the system will recognize.
        - name -- the human-readable name of the neighborhood
        - radius_to_search -- how far to search for wells in meters
        - lattitude -- the lattitude of the neighborhood
        - longitude -- the longitude of the neighborhood
    """ 
    name = models.CharField(max_length=80)
    radius_to_search = models.IntegerField()
    lattitude = models.FloatField()
    longitude = models.FloatField()
    def distance_to(self, lattitude, longitude):
        """Get the distance from this neighborhood to a lat lon point (eg a water source).
           Uses the haversine formula.
        """
        lat1 = math.radians(self.lattitude)
        lat2 = math.radians(lattitude)
        lon1 = math.radians(self.longitude)
        lon2 = math.radians(longitude)
        delta_lattitude = lat2 - lat1
        delta_longitude = lon2 - lon1
        a = (math.sin(delta_lattitude/2.0))**2 + math.cos(lat1)*math.cos(lat2)*(math.sin(delta_longitude))**2 
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0-a))
        earth_radius = 6371000.0
        return earth_radius * c

    def __str__(self):
        return self.name

class Source(models.Model):
    """ Corresponds to a source of water.
        - water_quality -- a function that takes test results that haven't expired and
                           returns a water quality score
        - lattitude -- the lattitude of the water source
        - longitude -- the longitude of the water source
        - id -- the id of the source written on the well. Must be unique (serves as the db private key)
        - type -- the type of the source (well, private, tap, private well)
    """
    lattitude = models.FloatField()
    longitude = models.FloatField()
    id = models.IntegerField(primary_key=True)
    WELL = 'W'
    PRIVATE = 'P'
    TAP = 'T'
    PRIVATE_WELL = 'PW'
    TYPE_CHOICES = (
        (WELL, 'Well'),
        (PRIVATE, 'Private'),
        (TAP, 'Tap'),
        (PRIVATE_WELL, 'Private Well'),
    )
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)

    ##### GENERAL FUNCTIONS FOR BOTH TURBIDITY AND FECAL##########
    def xtoy(x,x0,x1,y0,y1):
        m=(y1-y0)/(x1-x0)
        return (y0+m*(x-x0))

    def dattowqi(dat,length,xarray,yarray):
        found = False
        i = 0
        while ((i < length) and (not found)):
            if ((xarray[i] <= dat) and (dat <= xarray[i+1]) and (not found)):
                found = True
            i += 1

        if found:
            i -= 1
            return (xtoy(dat,xarray[i],xarray[i+1],yarray[i],yarray[i+1]))

        return 100
    #################################################################

    # FUNCTION FOR FECAL COLIFORM
    def calcfcwqi(input):
        inval = float(input)
        xarray = [0.0, 2.0, 3.0, 4.0,5.0]
        yarray = [99.0,44.0,22.0,10.0,4.0]
        cnt = 5
        if (inval < 1):
            outval = "Out of Range"
        else:

            if (inval > 100000):
                outval = 2
            else:
                outval=round(dattowqi((math.log(inval)/math.log(10)),cnt,xarray,yarray))
        return outval

    #FUNCTION FOR TURBIDITY
    def calcturbwqi(input):
        inval = float(input)
        xarray = [0.0, 3.0, 8.0,13.0,15.0,20.0,30.0,40.0,50.0,60.0,70.0,80.0,90.0,100.0]
        yarray = [99.0,90.0,80.0,70.0,67.0,61.0,53.0,45.0,39.0,33.0,29.0,25.0,22.0, 17.0]
        cnt = 14
        if (inval < 0):
            outval = "Out of range"
        else:
            if (100 < inval):
                outval = 5
            else:
                outval = round(dattowqi(inval,cnt,xarray,yarray))
        return outval

    def water_quality():
        """Returns the water quality score depending on the test results"""

        pass
    def __str__(self):
        return self.type + str(self.id)

class Test(models.Model):
    """ Corresponds to a test that community members can perform on a water source.
        - name -- the name of the test
        - weight -- the weight of the test in the water quality score
    """
    name = models.CharField(max_length=80)
    weight = models.FloatField()
    def __str__(self):
        return self.name

class TestResult(models.Model):
    """ Corresponds to a single test run on a water source.
        - test -- the test that was run
        - value -- the test result value
        - source -- the water source where the test was taken
        - timestamp -- when the test was taken (same as date received)
    """
    test = models.ForeignKey('Test')
    value = models.FloatField()
    source = models.ForeignKey('Source')
    timestamp = models.DateField(auto_now_add=True)
    def __str__(self):
        return str(self.test) + " for " + str(self.source)

