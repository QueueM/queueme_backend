# Create your views here.
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView,CreateAPIView
from customClasses.CustomBaseModelViewSet import CustomBaseModelViewSet
from .models import CompanySubscriptionPlansModel, CompanySubscriptionDetailsModel
from .serializers import(
    CompanySubscriptionDetailsModelSerializer, 
    CompanySubscriptionPlansModelsSerializer,
    PaymentSerializer
    )
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from . import helpers
from rest_framework import permissions
from  helpers.payment.moyasar import Moyasar
from  decouple import config



class CompanySubscriptionPlanViewSet(CustomBaseModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = CompanySubscriptionPlansModel.objects.all()
    serializer_class = CompanySubscriptionPlansModelsSerializer

class CompanySubscriptionDetailsViewSet(CustomBaseModelViewSet):
    queryset = CompanySubscriptionDetailsModel.objects.all()
    serializer_class = CompanySubscriptionDetailsModelSerializer

    def create(self, request, *args, **kwargs):
        company = request.data.get('company')
        plan_id = request.data.get('plan')

        try:
            company_instance = request.user.company
            plan_instance = CompanySubscriptionPlansModel.objects.get(id=plan_id)
            subscription = helpers.create_subscription(company_instance, plan_instance)
            serializer = self.get_serializer(subscription)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["get"],
        url_path="cash-and-bank-ledger", url_name="cash-and-bank-ledger",
    )
    def test(self, request, *args, **kwargs):
        return 
        
    


# payment APi view
class PaymentCreateApiView(CreateAPIView):
    serializer_class = PaymentSerializer
    def  get_serializer_context(self):
        context =  super().get_serializer_context()
        context["request"] = self.request
        return context
    




    
    
