# gateway/handlers.py
from rapidsms.contrib.handlers import KeywordHandler
from rapidsms.contrib.handlers import PatternHandler
from .models import Neighborhood
from .models import Source
from .models import Test
from .models import TestResult
from django.db.models import F
from celery import task

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
# @task()

################
#CALCULATES THE FECAL COLIFORM
# function calcfcwqi()
#    {
#       var intext=document.fcform.fc;
#       var outtext=document.fcform.fcwqi;
#       var xarray=new Array( 0.0, 2.0, 3.0, 4.0,5.0);
#       var yarray=new Array(99.0,44.0,22.0,10.0,4.0);
#       var inval,outval;
#       var cnt=5;
#
#       if (intext.value=="")
#       {
#          inval=intext.value;
#          outval="Blank";
#       }
#       else
#       {
#          inval=parseFloat(intext.value);
#          if (inval<1)
#          {
#              outval="Out of range";
#          }
#          else
#          {
#             if (inval>100000)
#             {
#                outval="2";
#             }
#             else
#             {
#                outval=Math.round(dattowqi(Math.log(inval)/Math.LN10,cnt,xarray,yarray));
#             }
#          }
#       }
#       intext.value=inval;
#       outtext.value=outval;
#    }

##################
##################
#CALCULATES THE TURBIDITY
# function calcturbwqi()
#    {
#       var intext=document.turbform.turb;
#       var outtext=document.turbform.turbwqi;
#       var xarray=new Array( 0.0, 3.0, 8.0,13.0,15.0,20.0,30.0,40.0,50.0,60.0,70.0,80.0,90.0,100.0);
#       var yarray=new Array(99.0,90.0,80.0,70.0,67.0,61.0,53.0,45.0,39.0,33.0,29.0,25.0,22.0, 17.0);
#       var inval,outval;
#       var cnt=14;
#
#       if (intext.value=="")
#       {
#          inval=intext.value;
#          outval="Blank";
#       }
#       else
#       {
#          inval=parseFloat(intext.value);
#          if (inval<0)
#          {
#              outval="Out of range";
#          }
#          else
#          {
#             if (100<inval)
#             {
#                outval="5";
#             }
#             else
#             {
#                 outval=Math.round(dattowqi(inval,cnt,xarray,yarray));
#             }
#          }
#       }
#       intext.value=inval;
#       outtext.value=outval;
#    }

##################
###### GENERAL FUNCTIONS FOR BOTH TURBIDITY AND FECAL COLIFORM
# function xtoy(x,x0,x1,y0,y1)
#    {
#       var m=(y1-y0)/(x1-x0);
#
#       return(y0+m*(x-x0));
#    }
#
#    function dattowqi(dat,len,xarray,yarray)
#    {
#       var i,found=false;
#
#       for (i=0;i<len && !found;i++)
#       {
#          if (xarray[i]<=dat && dat<=xarray[i+1] && !found)
#          {
#              found=true;
#          }
#       }
#       if (found)
#       {
#           i--;
#           return(xtoy(dat,xarray[i],xarray[i+1],yarray[i],yarray[i+1]));
#       }
#       return(100);
#    }

##################

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



###NEIGHBORHOOD NAME

#
# class NeighborhoodHandler(PatternHandler):
#     pattern = r'^(\d+) FC (\d+) T (\d+)$'
#
#     def help(self):
#         """Respond with the valid commands.  Example response:
#         ``Valid commands: 01234 FC 34 T 67
#         """
#         self.respond("Please enter proper Q-Value in the form: <Well-ID> FC <Q-VALUE> T <Q-VALUE> where the Q-VALUE ranges from 1-100. \n For example, 01234 FC 34 T 67 is a valid response.")
#
#     def handle(self, a,b,c):
#         a = int(a) #WELLID
#         Q_FC = float(b) #Q VALUE FOR FAECAL COLIFORM
#         Q_T = float(c) # Q VALUE FOR TURBIDITY
#         equation = FC * Q_FC + T * Q_T
#
#         self.respond( "WQI : %d" % (equation)) # GIVES OUT WATER QUALITY OF WATER

###########EXAMPLE WITH USING TASKS###########
# @task()
# def add(x,y):
#     return x+y
#
# #IF A NEW FILE IS MADE
# from myapp.tasks import add
# add.delay(2,2)
#
# ##ANOTHER EXAMPLE
# import myapp.tasks.add
# myapp.tasks.add(2,2)
#################################################