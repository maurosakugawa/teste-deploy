# THIRD PARTY IMPORTS
from flask import redirect, abort
from flask.helpers import flash, url_for
from flask.globals import g, session

# LOCAL IMPORTS
from app import app, db
from helpers import (
    commit_on_finish,
    form_validated_or_page_with_errors,
)
from forms.account import SignupForm, SigninForm, UpdateAccountForm
from models.customers import Customers
from models.isolated.customer_personal_info import CustomerPersonalInfo
from views.utils import (FormMethodView, MethodViewWrapper,
    RequiredLoggedoutViewMixin, RequiredLoginViewMixin,
)


class AccountEdit(FormMethodView, RequiredLoginViewMixin):
    """Tela para visualizar dados do Customer"""

    FORM = UpdateAccountForm

    @form_validated_or_page_with_errors
    @commit_on_finish
    def post(self, form=None):
        customer = Customers.from_form(form)
        yield customer
        return self.get(template=AccountView.TEMPLATE)


class AccountView(MethodViewWrapper, RequiredLoginViewMixin):
    """Tela para visualizar dados do Customer"""

    def get(self):
        form = UpdateAccountForm(obj=g.user)
        del form.password
        del form.username
        return super().get(form=form)


class AccountDelete(MethodViewWrapper, RequiredLoginViewMixin):
    """Rota para anonimizar Customer"""

    def get(self):
        if g.user is None:
            flash('Customer not found', category='error')
            abort(404)

        user_personal_info = CustomerPersonalInfo.from_customer(g.user)
        g.user.anonymized().save()
        user_personal_info.save()
        self.store_key_id(user_personal_info.customerid)

        flash("We're sorry to see you go :(")
        return redirect(url_for(Signout.ROUTE))
    
    def store_key_id(self, customerid):
        """Store id;key on an isolated environment"""
        # TODO: Change how to manage the keys
        # something like KMS from Amazon
        with open('isolated_db_keys.txt', 'a') as f:
            f.write('%s;%s\n' % (customerid, session['cryptkey'].decode()))
    

class Signin(FormMethodView, RequiredLoggedoutViewMixin):
    """Rota de login"""

    FORM = SigninForm
    
    @form_validated_or_page_with_errors
    def post(self, form=None):

        customer = Customers.query.filter(
            Customers.email==form.email.data).one_or_none()
        
        if customer and customer.is_active:
            if customer.password == form.password.data:
                session['customerid'] = customer.customerid
                return redirect(url_for(AccountView.ROUTE))
        
        flash("Email or Password doesn't match")
        return self.get(form=form)


class Signup(FormMethodView, RequiredLoggedoutViewMixin):
    """Rota para registrar usuario"""

    FORM = SignupForm

    @form_validated_or_page_with_errors
    @commit_on_finish
    def post(self, form=None):
        customer = Customers.from_form(form)
        
        yield customer

        flash('Thank You For Signing Up!')
        return redirect(url_for(Signin.ROUTE))


class Signout(MethodViewWrapper):
    """Rota para deslogar usuario"""

    def dispatch_request(self):
        session.clear()
        return redirect(url_for(Signin.ROUTE))
