from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Book Categories
CATEGORY_CHOICES = (
    ('Fiction', 'Fiction'),
    ('Non-fiction', 'Non-fiction'),
    ('Science', 'Science'),
    ('History', 'History'),
)

# Book Model
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='book_images/')
    available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title

# Cart Model
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

# Order Model
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book, through='OrderItem')
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.TextField()
    payment_method = models.CharField(max_length=50, default='Cash on Delivery')
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

# Order Item (Intermediate Model)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.book.title}"
