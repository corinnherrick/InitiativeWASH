# gateway/handlers.py
from rapidsms.contrib.handlers import KeywordHandler
from rapidsms.contrib.handlers import PatternHandler
from .models import Neighborhood
from .models import Source
from .models import Test
from .models import TestResult
from django.db.models import F

#Weighting Factors
#Faecal Coliform
# FC = 0.16 According to Water Quality Index
#Turbidity
# T = 0.08 According to Water Quality Index
#RANGES OF WATER QUALITY
#90-100 EXCELLENT
#70-90 GOOD
#50-70 MEDIUM
#25-50 BAD
#0-25 VERY BAD
#IF FC and T are only accounted for, then FC is weighted at 0.666666 and T is weighted at 0.333333
FC = 0.666666
T = 0.333333
#What will be given to us will be the Q values for both that we will input into our equation
#equation = FC * Q_FC + T * Q_T
#Using the range above we can determine the Water Quality

class EquationHandler(PatternHandler):
    pattern = r'^(\d+) FC (\d+) T (\d+)$'

    def help(self):
        """Respond with the valid commands.  Example response:
        ``Valid commands: 01234 FC 34 T 67
        """
        self.respond("Please enter proper Q-Value in the form: <Well-ID> FC <Q-VALUE> T <Q-VALUE> where the Q-VALUE ranges from 1-100. \n For example, 01234 FC 34 T 67 is a valid response.")

    def handle(self, a,b,c):
        a = int(a) #WELLID
        Q_FC = float(b) #Q VALUE FOR FAECAL COLIFORM
        Q_T = float(c) # Q VALUE FOR TURBIDITY
        equation = FC * Q_FC + T * Q_T

        self.respond( "WQI : %d" % (equation)) # GIVES OUT WATER QUALITY OF WATER