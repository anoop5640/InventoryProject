from django.shortcuts import render, get_object_or_404, redirect
from .models import InventoryItem
from .forms import InventoryItemForm
from django.db.models import F, Sum
from django.http import HttpResponse
from django.conf import settings
import boto3

import os
# View for listing inventory items
def inventory_list(request):
    items = InventoryItem.objects.all()
    low_stock_items = items.filter(quantity__lte=F('reorder_level'))
    return render(request, 'inventory/list.html', {
        'items': items,
        'low_stock_items': low_stock_items
    })

# View for adding a new inventory item
def add_inventory_item(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, request.FILES)
        if form.is_valid():
            new_item = form.save()

            # Upload the image to S3
            if 'image' in request.FILES:
                image_file = request.FILES['image']
                s3_client = boto3.client('s3')

                try:
                    s3_client.upload_fileobj(
                        image_file,
                        settings.AWS_STORAGE_BUCKET_NAME,
                        f'inventory_images/{image_file.name}',
                        ExtraArgs={'ACL': 'public-read'}  # Make the file public
                    )
                    new_item.image.name = f'inventory_images/{image_file.name}'
                    new_item.save()
                except Exception as e:
                    print(f"Error uploading image to S3: {e}")

            return redirect('inventory_list')  # Replace with your appropriate redirect
    else:
        form = InventoryItemForm()

    return render(request, 'inventory/add_edit_item.html', {'form': form})

# View for editing an existing inventory item
def edit_inventory_item(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            if 'image' in request.FILES:
                if item.image:
                    # Delete the old image from S3
                    s3_client = boto3.client('s3')
                    s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=item.image.name)
            form.save()
            return redirect('inventory_list')
    else:
        form = InventoryItemForm(instance=item)
    return render(request, 'inventory/add_edit_item.html', {'form': form})

# View for deleting an inventory item
def delete_inventory_item(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == 'POST':
        if item.image:
            # Delete the image from S3
            s3_client = boto3.client('s3')
            s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=item.image.name)
        item.delete()
        return redirect('inventory_list')
    return render(request, 'inventory/confirm_delete.html', {'item': item})

def dashboard(request):
    low_stock_items = InventoryItem.objects.filter(quantity__lte=F('reorder_level'))
    total_items = InventoryItem.objects.count()
    total_value = InventoryItem.objects.aggregate(total_value=Sum(F('quantity') * F('price')))['total_value'] or 0

    return render(request, 'inventory/dashboard.html', {
        'low_stock_items': low_stock_items,
        'total_items': total_items,
        'total_value': total_value,
    })
