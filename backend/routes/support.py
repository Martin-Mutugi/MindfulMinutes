from flask import Blueprint, render_template

support_bp = Blueprint('support', __name__, url_prefix='/support')

@support_bp.route('/help')
def help():
    return render_template('support/help.html')

@support_bp.route('/faq')
def faq():
    return render_template('support/faq.html')
@support_bp.route('/contact')
def contact():
    return render_template('support/contact.html')


