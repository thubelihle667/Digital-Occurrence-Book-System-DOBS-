from django.contrib.auth import get_user_model

User = get_user_model()

def create_test_user(
    email="user@example.com",
    role="officer",
    password="pass1234",
    username='bob',
    #**extra_fields
):
    return User.objects.create_user(
        email=email,
        role=role,
        password=password,
        username=username
        #**extra_fields
    )


def create_test_admin(
    email="admin@example.com",
    role="admin",
    password="adminpass",
    #**extra_fields
):
    return User.objects.create_superuser(
        email=email,
        role=role,
        password=password,
        #**extra_fields
    )
