from django.db import models

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
    def water_quality(self):
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

