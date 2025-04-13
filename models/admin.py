from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, flash
from forms import UserForm

class AdminModelView(ModelView):
    form = UserForm
    
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        flash('Brak dostępu do panelu administracyjnego.', 'danger')
        return redirect(url_for('login'))


#def add_menu_links(admin):
#    if current_user.is_authenticated:
#        admin.add_link(MenuLink(name="Logout", url="/logout"))
#    else:
#        admin.add_link(MenuLink(name="Login", url="/login"))
#    admin.add_link(MenuLink(name="Powrót do strony głównej", url="/"))