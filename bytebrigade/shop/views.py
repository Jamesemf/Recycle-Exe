from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
import qrcode
import qrcode.image.svg
from io import BytesIO
from .models import ShopItems

# Create your views here.
def shop_view(request):
    """
    This function will handle the shop page view. A user will be presented the shop page to which they can select
    which item they would like to buy. This will then be returned to the user by email after a successful purchase.
    """
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        item_id = request.POST.get("item_id")
        item = ShopItems.objects.get(item_id=item_id)
        item_purchased(request.user, item)
    return render(request, 'Shop/shop.html')

def item_purchased(user, item):
    """
    This procedure handles the purchase of a given item. First we must check that the user can afford this item and then
    if they can we then purchase the product and then email them a QR code
    """
    user_stats = Statistic.objects.get(user=user)
    if(user_stats.points>=item.cost):
        user_stats.points-=item.cost
        user_stats.save()
        img = qrcode.make(item.name, image_factory=factory, box_size=20)
        subject, from_email, to = 'hello', 'from@example.com', user.email
        text_content = 'This is an important message.'
        html_content = '<img>'+img+'</img>'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    else:
        # They cannot afford the product
        return redirect('shop_view')