from django.shortcuts import render, redirect
import qrcode
import qrcode.image.svg
from io import BytesIO
from .models import ShopItems
from account.models import Statistic
from django.core.mail import EmailMultiAlternatives


def shop_view(request):
    """
    Web backend for’../shop/’ (name ‘shop’)

    This function will handle the shop page view. A user will be presented the shop page to which they can select
    which item they would like to buy. This will then be returned to the user by email after a successful purchase.

    Return: 'shop.html' with shop items dictionary.
    """
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        item_id = request.POST.get("shop_item")
        item = ShopItems.objects.get(item_id=item_id)
        item_purchased(request.user, item)

    data = ShopItems.objects.all()
    data_dict = {'shop_items': data}
    return render(request, 'shop.html', data_dict)


def item_purchased(user, item):
    """
    This procedure handles the purchase of a given item. First we must check that the user can afford this item and then
    if they can we then purchase the product and then email them a QR code

    Parameters:
        user: user model of specific user.
        item: item that been choosed by user.
    return:
        redirect back to shop page after purchase done.
    """
    user_stats = Statistic.objects.get(user=user)
    if(item.stock == 0):
        return redirect('shop')
    if(user_stats.points>=item.cost):
        item.stock -= 1
        item.save()
        user_stats.points -= item.cost
        user_stats.save()

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(item.name)
        qr.make(fit=True)

        img = qr.make_image(fill_color='black', back_color='white')
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        qr_image_data = buffer.getvalue()

        email = EmailMultiAlternatives(
            subject='Shop Purchase',
            body='Attached is your purchase QRcode. Please show this to a member of staff',
            from_email='bytebrigade@outlook.com',
            to=[user.email],
        )
        # Attach the QR code image as an inline attachment
        email.attach('qrcode.png', qr_image_data, 'image/png')
        email.send()
    # They cannot afford the product
    return redirect('shop')



