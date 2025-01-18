from .models import *
from django.shortcuts import redirect, render, get_object_or_404
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



def manage_medicine_release(request):
    if request.method == 'POST':
        maintenance_id = request.POST.get('maintenance_id')
        medicine_id = request.POST.get('medicine_id')
        released_quantity = int(request.POST.get('released_quantity', 0))

        # Fetch the medicine instance
        medicine = get_object_or_404(Medicine, id=medicine_id, maintenance_id=maintenance_id)

        if medicine.medicine_quantity >= released_quantity:
            # Deduct the released quantity from medicine stock
            medicine.medicine_quantity -= released_quantity
            medicine.released_quantity = released_quantity  # Save released quantity
            medicine.save()
            return JsonResponse({"success": True, "message": "Medicine released successfully."})
        else:
            return JsonResponse({"success": False, "message": "Insufficient stock."})
    
    # For GET, fetch medicines and maintenance objects
    medicines = Medicine.objects.all()
    maintenances = Maintenance.objects.all()
    return render(request, 'manage_medicine.html', {'medicines': medicines, 'maintenances': maintenances})
