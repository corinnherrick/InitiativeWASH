from rapidsms.contrib.handlers import KeywordHandler
from rapidsms.contrib.handlers import PatternHandler
from models import Source
from models import Test
from models import TestResult
from models import Neighborhood

class DataHandler(PatternHandler):
    pattern = r'^(\d+) FC (\d+) T (\d+)$'
    """
    The test results should be sent in the following format: <Source-ID> FC <FC-VALUE> T <T-VALUE> where 
    Source-ID is the ID number of the water source, T-VALUE is the turbidity test value and FC-VALUE is 
    the fecal coliform test value.
    """

    def handle(self, source_id, fecal_coliform, turbidity):
        try:
            source = Source.objects.get(id=source_id)
        except Source.DoesNotExist:
            self.respond("Water source %s does not exist." % (source_id,))
            return True

        fc_test_model = Test.objects.get(name="Fecal Coliform")
        turbidity_test_model = Test.objects.get(name="Turbidity")
        TestResult(test=fc_test_model, value=fecal_coliform, source=source).save()
        TestResult(test=turbidity_test_model, value=turbidity, source=source).save()

        self.respond("Thanks! We saved the data in our system." )
        return True

class NeighborhoodHandler(KeywordHandler):
    keyword = "near"

    def help(self):
        self.respond("Text in 'near NEIGHBORHOOD' to get the water sources near you.")
        return True

    def handle(self, text):
        neighborhood = Neighborhood.objects.get(name__iexact=text.strip())
        sources_nearby = sorted(Source.objects.all(), key=lambda s: s.water_quality(), reverse=True)
        sources_nearby = filter(lambda s: neighborhood.distance_to(s.lattitude, s.longitude) < neighborhood.radius_to_search,
                                sources_nearby)
        
        response = "Here is a list of wells near you:\n"
        response += "\n".join(["Well %d, Grade: %d\n" % (source.id, source.water_quality()) for source in sources_nearby[:3]])
        response += "\nThank you for using I:WASH"
        response += str(len(sources_nearby))
        
        self.respond(response)
        return True



