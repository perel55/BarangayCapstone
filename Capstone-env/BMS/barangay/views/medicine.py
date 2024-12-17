from .models import *
from django.shortcuts import redirect, render
from django.shortcuts import redirect
from django.http import JsonResponse

def addMedicine(request):
    if request.method == 'POST':
        medicine_name = request.POST.get('medicine_name')
        medicine_quantity = request.POST.get('medicine_quantity')
        medicine_description = request.POST.get('medicine_description')
        expiration_date = request.POST.get('expiration_date')
        medicine_type = request.POST.get('medicine_type')
        picture = request.FILES['picture']

        if medicine_name and medicine_description and medicine_quantity and picture:
            # Create and save the HealthService object
            new_medicine = Medicine(
                medicine_name=medicine_name,
                medicine_quantity=medicine_quantity,
                medicine_description=medicine_description,
                expiration_date=expiration_date,
                medicine_type=medicine_type,
                picture=picture,
            )
            new_medicine.save()
            return redirect('bhwMedic') 
        else:
            error_message = "All fields are required."

def bhwMedic(request):
    medicines = Medicine.objects.all()
    return render(request, 'bhw/bhwMI.html', {'medicines': medicines})    





def update_maintenance(request):
    if request.method == "POST":
        for key, value in request.POST.items():
            if key.startswith("medicine_name_"):
                # Extract the row index
                index = key.split("_")[2]
                medicine_id = value
                quantity_key = f"medicine_quantity_{index}"
                quantity = request.POST.get(quantity_key)

                if quantity and medicine_id:
                    quantity = int(quantity)
                    medicine = Medicine.objects.get(id=medicine_id)

                    if medicine.medicine_quantity >= quantity:
                        # Deduct the quantity from the Medicine table
                        medicine.medicine_quantity -= quantity
                        medicine.save()
                    else:
                        # Handle insufficient stock
                        return JsonResponse({'error': f'Not enough stock for {medicine.medicine_name}'}, status=400)

        # Redirect or render a success message
        return redirect('releasedMaintenance')  

    return JsonResponse({'error': 'Invalid request'}, status=400)
