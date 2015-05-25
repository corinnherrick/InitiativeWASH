from rapidsms.contrib.handlers import KeywordHandler
from rapidsms.contrib.handlers import PatternHandler
from models import Source
from models import Test
from models import TestResult
from models import Neighborhood

class DataHandler(KeywordHandler):
    """
    The test results should be sent in the following format: add WellID, turb ###, coli ### 
    """
    keyword = "add"
    def help(self):
        self.respond("Please enter data in the format 'add WellID, turb ###, coli ###")
        return True

    def handle(self, text):
        bad_format_response = "Please enter data in the format 'add WellID, turb ###, coli ###"
        data_list = text.split(",")
        if len(data_list) != 3:
            self.respond(bad_format_response)
            return True
        try:
            source_id = int(data_list[0])
        except ValueError:
            self.respond("%s is not a valid well ID." % (data_list[0]))
            return True
        try:
            source = Source.objects.get(id=source_id)
        except Source.DoesNotExist:
            self.respond("Water source %s does not exist." % (source_id,))
            return True

        fc_test_model = Test.objects.get(name="Fecal Coliform")
        turbidity_test_model = Test.objects.get(name="Turbidity")
        try:
            turbidity = float(data_list[1].split()[1])
            fecal_coliform = float(data_list[2].split()[1])
        except ValueError:
            self.respond(bad_format_response)
            return True
        if data_list[1].split()[0] != "turb" or data_list[2].split()[0]!="coli":
            self.respond(bad_format_response)
            return True 
        TestResult(test=fc_test_model, value=fecal_coliform, source=source).save()
        TestResult(test=turbidity_test_model, value=turbidity, source=source).save()

        self.respond("Thanks! We saved the data in our system." )
        return True

class NeighborhoodHandler(KeywordHandler):
    keyword = "near"

    def help(self):
        self.respond("Text in 'near NEIGHBORHOOD' to get the water sources near you. Text in 'near NEIGHBORHOOD, WELLID to get data about a specific water source.")
        return True

    def handle(self, text):
        response = "Thank you for using WASH Mobile.\n"
        data_list = text.split(",")
        if len(data_list) == 0:
            self.help()
            return True
        elif len(data_list) == 2:
            try:
                well_id = int(data_list[1])
                try:
                    source = Source.objects.get(id=well_id)
                    response += "Here is the grade for the well you entered.\n\n"
                    response += "Well %d, Grade: %d\n\n" % (source.id, source.water_quality())
                except Source.DoesNotExist:
                    response += "We can't find a water source with ID %s\n" % (data_list[1],)
            except ValueError:
                response += "We can't find a water source with ID %s\n" % (data_list[1],)
            
        neighborhood = Neighborhood.objects.get(name__iexact=data_list[0].strip())
        sources_nearby = sorted(Source.objects.all(), key=lambda s: s.water_quality(), reverse=True)
        sources_nearby = filter(lambda s: neighborhood.distance_to(s.lattitude, s.longitude) < neighborhood.radius_to_search,
                                sources_nearby)
        
        response += "Here are the best water sources near you:\n"
        response += "\n".join(["Well %d, Grade: %d\n" % (source.id, source.water_quality()) for source in sources_nearby[:3]])
        response += "\nThank you for using I:WASH"
        response += str(len(sources_nearby))
        
        self.respond(response)
        return True



