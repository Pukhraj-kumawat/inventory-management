from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from inventory.models import *

def home(request):
    return HttpResponse("<h1>Welcome to Inventory Management</h1>")

def index(request):
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    context = {
        'total_products': total_products,
        'total_categories': total_categories,
    }
    return render(request, 'inventory/index.html', context)

# ADD APIs
@csrf_exempt
@require_http_methods(["POST","GET"])
def category_register(request):

    try:
        name= request.POST.get('name')
        description = request.POST.get('description')
        request_errors = {}
        
        if not name:
            request_errors['name'] = "Please provide name"
        if not description:
            request_errors['description'] = "Please provide description "
        # if request_errors:
        #     return JsonResponse({'status': False, 'errors': request_errors}, status=400)
        if request_errors:
            return render(request, 'inventory/add_category.html', {'errors': request_errors})

          
        category_register_row=Category.objects.create(
            name=name,
            description=description,
        )

        category_data = {
            'category_Id' : category_register_row.id,
            'name': category_register_row.name,
            'description': category_register_row.description,
        }
        context = {
            'status': True,
            'message': 'Product Registration Successful',
            'category_data': category_data
        }

        return render(request, 'inventory/add_category.html', context)



    except Exception as e:
        return render(request, 'inventory/add_category.html', {'error': str(e)})

   
@csrf_exempt
@require_http_methods(["POST"])
def user_register(request):

    try:
        username=request.POST.get('username')
        password= request.POST.get('password')
        email = request.POST.get('email')
        request_errors = {}
        
        if not username:
            request_errors['username'] = "Please provide username"
        if not email:
            request_errors['email'] = "Please provide email "
        if not password:
            request_errors['password'] = "Please provide password "
        if request_errors:
            return JsonResponse({'status': False, 'errors': request_errors}, status=400)

          
        user_register_row=User.objects.create(
            username=username,
            email=email,
            password=password,
        )

        user_data = {
            'user_Id' : user_register_row.id,
            'username': user_register_row.username,
            'email': user_register_row.email,
        }

        return JsonResponse({
            'status': True,
            'message': 'User Registration Successful',
            'user_data': user_data
        }) 
    

    except Exception as e:
        return JsonResponse({'status': False, 'error': str(e)}, status=500)
  
@csrf_exempt
@require_http_methods(["POST","GET"])
def product_register(request):

    try:
        categories = Category.objects.all()

        if request.method == "POST":
            name= request.POST.get('name') 
            quantity_in_stock = request.POST.get('quantity_in_stock')
            # category = request.POST.get('category')
            category_id = request.POST.get('category')
            price = request.POST.get('price')
            request_errors = {}
            print("category_id",category_id)
            if not name:
                request_errors['name'] = "Please provide name"
            if not price:
                request_errors['price'] = "Please enter price "
            if not quantity_in_stock:
                request_errors['quantity_in_stock'] = "Please enter quantity in stock "
            if not category_id:
                request_errors['category'] = "Please enter category "

            # if request_errors:
            #     return JsonResponse({'status': False, 'errors': request_errors}, status=400)
            if request_errors:
                return render(request, 'inventory/add_product.html', {'errors': request_errors})
            
            category = Category.objects.filter(id=category_id).first()
            print("category",category)
            
            if not category:
                context = {
                    'errors': {'category': 'Category not found'},
                    'categories': categories
                }
                return render(request, 'inventory/add_product.html', context)
            
            product_row=Product.objects.create(
                name=name,
                category=category,
                price=price,
                quantity_in_stock=quantity_in_stock,
            )
            print("product_row",product_row)

            product_data = {
                'product_Id' : product_row.id,
                'name': product_row.name,
                'price': product_row.price,
                'quantity':product_row.quantity_in_stock,
                'category': product_row.category.name,
            }

            context = {
                'status': True,
                'message': 'Product Registration Successful',
                'product_data': product_data,
                'categories': categories
            }

            return render(request, 'inventory/add_product.html', context)
        return render(request, 'inventory/add_product.html', {'categories': categories})

        # return JsonResponse({
        #     'status': True,
        #     'message': 'Product Registration Successful',
        #     'product_data': product_data
        # }) 


    except Exception as e:
        # return JsonResponse({'status': False, 'error': str(e)}, status=500)
        return render(request, 'inventory/add_product.html', {'error': str(e)})



@csrf_exempt
@require_http_methods(["POST"])
def delete_product_view(request):
    try:
        product_id = request.POST.get('product_id')
        request_errors = {}
        
        if not product_id:
            request_errors['product_id'] = "Product ID is required"
        
        if request_errors:
            return JsonResponse({'status': False, 'errors': request_errors}, status=400)

        try:
            product = Product.objects.get(id=product_id)
           
            product.delete()
            return JsonResponse({'status': True, 'message': 'Product removed successfully'})
        except Product.DoesNotExist:
            return JsonResponse({'status': False, 'error': 'Product does not exist for this ID'}, status=400)

    except Exception as e:
        return JsonResponse({'status': False, 'error': str(e)}, status=500)
    
@csrf_exempt
@require_http_methods(["POST"])
def delete_category_view(request):
    try:
        category_id = request.POST.get('category_id')
        request_errors = {}
        
        if not category_id:
            request_errors['category_id'] = "Category ID is required"
        
        if request_errors:
            return JsonResponse({'status': False, 'errors': request_errors}, status=400)

        try:
            category = Category.objects.get(id=category_id)
            category.delete()
            return JsonResponse({'status': True, 'message': 'Category removed successfully'})
        except Product.DoesNotExist:
            return JsonResponse({'status': False, 'error': 'Category does not exist for this ID'}, status=400)

    except Exception as e:
        return JsonResponse({'status': False, 'error': str(e)}, status=500)
 

@csrf_exempt
@require_http_methods(["POST"])
def view_product(request):
    try:
        product_id = request.POST.get('product_id')
        request_errors = {}
        
        if not product_id:
            request_errors['product_id'] = "Product ID is required"
        
        if request_errors:
            return JsonResponse({'status': False, 'errors': request_errors}, status=400)
        
        try:
            product = Product.objects.get(id=product_id)
            product_data = {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'quantity_in_stock': product.quantity_in_stock, 
                'category':product.category.name,
            }
            
            return JsonResponse({'status': True, 'product': product_data})
        
        except Product.DoesNotExist:
            return JsonResponse({'status': False, 'error': 'Product not found'}, status=404)

    except Exception as e:
        return JsonResponse({'status': False, 'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def view_category(request):
    try:
        category_id = request.POST.get('category_id')
        request_errors = {}
        
        if not category_id:
            request_errors['category_id'] = "Category ID is required"
        
        if request_errors:
            return JsonResponse({'status': False, 'errors': request_errors}, status=400)
        
        try:
            category = Category.objects.get(id=category_id)
            category_data = {
                'id': category.id,
                'name': category.name,
                'price': category.description,
            }
            
            return JsonResponse({'status': True, 'category': category_data})
        
        except Category.DoesNotExist:
            return JsonResponse({'status': False, 'error': 'Category not found'}, status=404)

    except Exception as e:
        return JsonResponse({'status': False, 'error': str(e)}, status=500)




# list APIs
@require_http_methods(["GET"])
def list_products_view(request):
    try:
        products = Product.objects.values('id', 'name', 'price', 'quantity_in_stock','category__name')
      
        context = {
        'products': products
        }

        return render(request, 'inventory/list_products.html', context)


    
    except Exception as e:
        return render(request, 'inventory/list_products.html', {'error': str(e)})
    

def list_category_view(request):
    try:
        categories = Category.objects.values('id', 'name', 'description')
      
        # category_list = list(categories)
        context = {
        'categories': categories
        }

        return render(request, 'inventory/list_categories.html', context)

        # return JsonResponse({
        #     'status': True,
        #     'categories': category_list
        # }, status=200)

    except Exception as e:
        return render(request, 'inventory/list_categories.html', {'error': str(e)})
  
  