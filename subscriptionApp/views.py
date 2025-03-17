# Create your views here.
from rest_framework.views import APIView
from customClasses.CustomBaseModelViewSet import CustomBaseModelViewSet
from .models import CompanySubscriptionPlansModel, CompanySubscriptionDetailsModel
from .serializers import CompanySubscriptionDetailsModelSerializer, CompanySubscriptionPlansModelsSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from . import helpers
from rest_framework import permissions
from  helpers.payment.moyasar import Mayasar
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
        
    


# payment 
class PaymentApiView(APIView):
    permission_classes = [permissions.AllowAny]
    secrect_key = config('MOYASAR_SECRET')
    api_key = config('MOYASAR_PUBLIC')
    callback_url = config('MOYASAR_CALLBACK_URL')
    
    def post(self,request):
        data = request.data
        moyasar = Mayasar(self.api_key, self.secrect_key, self.callback_url)
        payment = moyasar.payment(data['amount'], data['description'], data['source'])
        return Response(payment)
        
        
