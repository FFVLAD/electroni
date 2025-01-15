# mainapp/utils.py

def is_teacher(user):
    return user.groups.filter(name='Teachers').exists()
