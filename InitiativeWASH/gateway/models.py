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

    # test result -> wqi curves
    fecal_coliform_curve = {0.0: 99.0, 2.0: 44.0, 3.0: 22.0, 4.0: 10.0, 5.0: 4.0}
    turbidity_curve = {0.0: 99.0, 3.0: 90.0, 8.0: 80.0, 13.0: 70.0, 15.0: 67.0, 
                       20.0: 61.0, 30.0: 53.0, 40.0: 45.0, 50.0: 39.0, 60.0: 33.0, 
                       70.0: 29.0, 80.0: 25.0, 90.0: 22.0, 100.0: 17.0}
    def compute_wqi(self, curve_dict, test_result):
        # Get the closest test result value for which we have a wqi
        vals_below = filter(lambda k: k<=test_result, curve_dict.keys())
        vals_above = filter(lambda k: k<=test_result, curve_dict.keys())
        if len(vals_below) == 0:
            return 100
        if len(vals_above) == 0:
            return 0
        nearest_val_below = min(vals_below, key=lambda k: abs(k-test_result))
        nearest_val_above = min(vals_above, key=lambda k: abs(k-test_result))
        wqi_below = curve_dict[nearest_val_below]
        wqi_above = curve_dict[nearest_val_above]
        if nearest_val_below == nearest_val_above:
            return wqi_below
        else:
            slope = (wqi_above - wqi_below)/(nearest_val_above - nearest_val_below)
            return wqi_below + slope*(test_result - nearest_val_below)

    def water_quality(self):
        """Returns the water quality score depending on the test results"""
        fc_result = TestResult.objects.filter(test__name="Fecal Coliform", source=self).order_by("-timestamp")[0]
        turbidity_result = TestResult.objects.filter(test__name="Turbidity", source=self).order_by("-timestamp")[0]

        # log the fc_result value
        fc_value = 100
        if fc_result.value >= 1.0:
            fc_value = math.log(fc_result.value)/math.log(10)
        fc_wqi = self.compute_wqi(Source.fecal_coliform_curve, fc_value)
        turb_wqi = self.compute_wqi(Source.turbidity_curve, turbidity_result.value)
        return fc_wqi*fc_result.test.weight + turb_wqi*turbidity_result.test.weight
        

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

