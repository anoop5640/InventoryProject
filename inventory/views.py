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
    """View to add a new inventory item."""
    
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
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
