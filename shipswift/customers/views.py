from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Customer

def register_customer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            password = data.get('password', '')
            username = data.get('username', '')
            full_name = data.get('fullName', '')
            address = data.get('Address', '')
            gender = data.get('Gender', False)  
            marital_status = data.get('maritalStatus', '')

            if Customer.objects.filter(username=username).exists():
                return JsonResponse({'message': 'Username already taken'}, status=400)

            new_customer = Customer.objects.create(
                password=password,
                username=username,
                fullName=full_name,
                Address=address,
                Gender=gender,
                maritalStatus=marital_status
            )

            customer_id = new_customer.id

            return JsonResponse({'message': 'Customer registered successfully', 'customer_id': customer_id})
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON format in the request body'}, status=400)
        except Exception as e:
            return JsonResponse({'message': f'Error registering customer: {str(e)}'}, status=500)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)

def delete_customer(request, customer_id):
    if request.method == 'DELETE':
        customer = get_object_or_404(Customer, pk=customer_id)
        customer.delete()

        return JsonResponse({'message': 'Customer deleted successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)

def update_customer(request, customer_id):
    if not Customer.objects.filter(username=username).exists():
        return JsonResponse({'message': 'Customer not found'}, status=404)
    else:
        customer = Customer.objects.get(username=username)

        data = json.loads(request.body.decode('utf-8'))
        password = data.get('password', '')
        username = data.get('username', '')
        full_name = data.get('fullName', '')
        address = data.get('Address', '')
        gender = data.get('Gender', False)  
        marital_status = data.get('maritalStatus', '')

        customer.password = password
        customer.username = username
        customer.fullName = full_name
        customer.address = address
        customer.gender = gender
        customer.maritalStatus = marital_status
        
        



def get_customer(request, customer_id):
    if request.method == 'GET':
        customer = get_object_or_404(Customer, pk=customer_id)

        return JsonResponse({'id': customer.id, 'full_name': customer.full_name})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)


def get_all_customers(request):
    if request.method == 'GET':
        customers = Customer.objects.all()

        customer_list = [{'id': customer.id, 'username': customer.username, 'full_name': customer.full_name} for customer in customers]

        return JsonResponse({"customers": customer_list})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)


