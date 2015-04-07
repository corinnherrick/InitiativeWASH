from rapidsms.contrib.handlers import KeywordHandler
from rapidsms.contrib.handlers import PatternHandler
from models import Source
from models import Test
from models import TestResult

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



