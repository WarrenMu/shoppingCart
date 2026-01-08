# shoppingCartshopping-cart/
```
├── backend/
│   ├── manage.py
│   ├── core/
│   │   ├── settings.py
│   │   ├── urls.py
│   ├── authapp/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── permissions.py
│   ├── shop/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── services.py   👈 algorithms live here
│   │   ├── urls.py
│   └── .env
│
├── frontend/
│   ├── pages/
│   │   ├── index.js
│   │   ├── cart.js
│   │   ├── login.js
│   ├── lib/api.js
│   ├── context/CartContext.js
│   └── .env.local
│
├── .gitignore


shop/
├── models.py
├── services.py     # business logic + algorithms
├── views.py        # thin HTTP layer
├── urls.py


accounts/
├── models.py
├── services.py     # business logic + algorithms
├── views.py        # thin HTTP layer
├── urls.py
```