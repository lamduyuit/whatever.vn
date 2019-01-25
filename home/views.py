from flask import Blueprint, session, render_template, url_for, send_file, flash,redirect, request,abort,send_from_directory, jsonify, make_response
from bokeh.embed import components
from werkzeug.datastructures import MultiDict
import pandas as pd
from datetime import datetime, timedelta
from collections import namedtuple
import pytz, json
from sys import path
import pprint
from flask_login import current_user, login_required


from home.forms import home_form, info_form, form_2_stages, form_3_stages, form_n_stages, form_stable
from home.models import *
from home.func import get_chart, download_financial
from home.help_valuation import get_df_input, valuate_2_stages, api_response, valuate_3_stages, valuate_n_stages, \
valuate_stable, get_attr_from_class, extract_data_from_form, create_obj, get_list_form
from settings import PROTECTED_FOLDER
from user.models import *

"""
#from flask_oauth import OAuth
from flask_oauthlib.client import OAuth

FACEBOOK_APP_ID = '642326979519735'
FACEBOOK_APP_SECRET = 'a3cf59bbd590318df949cf77aecae12e'

oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': ('email, ')}
)
"""
#import os
#os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
#Module Search Paths
#from pprint import pprint
#pprint(path)


home_app = Blueprint('home_app', __name__)

@home_app.route('/', methods=('GET', 'POST'))
def home():
    print(session)
    if session.get("facebook_token"):
        data = facebook.get('/me?fields=id,name,birthday,address,education,email,hometown').data
        print(data)
        token_to_text(session.get("facebook_token"))
    debug = True
    form = home_form()
    #print(type(form.stock_id))
    divs,script,error = None,None,None
    scripts,divs = [],[]
    if form.validate_on_submit():
        stock_id = form.stock_id.data
        if debug:
            list_chart = get_chart(str(stock_id).upper())
            if list_chart is None:
                error = "Can't not display this stock"
                return render_template("home/home.html", form = form, divs = divs,scripts = scripts,error=error)
            error=None
            for chart in list_chart:
                script,div = components(chart)
                scripts.append(script)
                divs.append(div)
        else:
            #list_chart = get_chart(str(stock_id).upper())
            try:
                list_chart = get_chart(str(stock_id).upper())
            except Exception as e:
                print(e)
                error = "Can't not display this stock"
            else:
                for chart in list_chart:
                    script,div = components(chart)
                    scripts.append(script)
                    divs.append(div)

        return render_template("home/home.html", form = form, divs = divs,scripts = scripts,error=error)

    return render_template("home/home.html", form = form, divs=divs,scripts=scripts,error=error)

@home_app.route('/download/', methods=['POST'])
def download():
    if request.method == "POST":
        form = home_form()
        if form.validate_on_submit():
            path = download_financial(str(form.stock_id.data).upper())
            if path is not None:
                #return "Path +++++++++++++++++++++++++++>>>>>>>>>>>>>>>>>>>" + path
                # return "Dang test : )))"
                return send_from_directory(PROTECTED_FOLDER,filename=str(form.stock_id.data).upper()+"-report.xlsx",attachment_filename=str(form.stock_id.data).upper()+"-report.xlsx",as_attachment=True)
            else:
                 flash("Sorry! We don't have fundamental information about this company")
                 return redirect("/")
        else:
            # return "Dang test :  )))"
            flash(form.stock_id.errors[0])
            return redirect("/")
    else:
        abort(404)

@home_app.route('/valuation/', methods=['POST', 'GET'])
def valuation():
    form = home_form()
    form_stable_ = form_stable()

    #for i, field in enumerate(form_n_stages_):
        #print(i+1, "  ", field)

    #print("data: ", form_2_stages_data, type(form_2_stages_data))


    #form_2_stages_ = form_2_stages(formdata   = MultiDict(list(form_2_stages_data.items())))

    #return render_template("home/valuation.html", form = form, error = None, first_info_form = first_info_form, form_2_stages_ = form_2_stages_)

#############################################################################################################################################################

    if form.validate_on_submit():
        stock_id = form.stock_id.data
        html_df_input, No_vay, Cash_Investment, Shares = get_df_input(str(stock_id.upper()))
        if html_df_input:
            if current_user.is_authenticated:
                stock_save = Save_valuation.objects.filter(stock_id=stock_id, from_user = current_user.id).first()
                #Truong hop dang nhap va co du lieu co phieu da luu
                if stock_save:
                    form_data = stock_save.form_data
                    form_data = MultiDict(list(form_data.items()))
                    first_info_form, form_2_stages_, form_3_stages_, form_n_stages_ = get_list_form(form_data)
                #Truong hop dang nhap nhung khong co ma co phieu nao luu
                else:
                    first_info_form, form_2_stages_, form_3_stages_, form_n_stages_ = get_list_form(No_vay = No_vay, Cash_Investment = Cash_Investment, Shares = Shares)
            #Truong hop khong dang nhap
            else:
                #print("khong dang nhap")
                first_info_form, form_2_stages_, form_3_stages_, form_n_stages_ = get_list_form(No_vay = No_vay, Cash_Investment = Cash_Investment, Shares = Shares)
            return render_template("home/valuation.html", form = form, error = None, dfs_input = html_df_input,\
                                    first_info_form = first_info_form, form_2_stages_ = form_2_stages_, form_3_stages_ = form_3_stages_,
                                    form_n_stages_ = form_n_stages_, form_stable_ = form_stable_)
        #Truong hop khong co stock_id
        else:
            first_info_form, form_2_stages_, form_3_stages_, form_n_stages_ = get_list_form(stock_id = False)
            error = "Không có dữ liệu !"
            return render_template("home/valuation.html", form = form, error = error,\
                                     first_info_form = first_info_form, form_2_stages_ = form_2_stages_, form_3_stages_ = form_3_stages_,
                                     form_n_stages_ = form_n_stages_, form_stable_ = form_stable_)
    else:
        first_info_form, form_2_stages_, form_3_stages_, form_n_stages_ = get_list_form(stock_id = False)
        if form.stock_id.errors != ():
            form.stock_id.errors = ["Bạn cần nhập mã CP !"]
        return render_template("home/valuation.html", form = form, error = None,\
                                 first_info_form = first_info_form, form_2_stages_ = form_2_stages_, form_3_stages_ = form_3_stages_,
                                 form_n_stages_ = form_n_stages_, form_stable_ = form_stable_)

@home_app.route('/_stages/', methods=['POST'])
def _stages():
    #Dieu chinh lai gia tri cong ty, them o tien va cac khoan dau tu tai chinh ngan han
    first_info_form = info_form()
    form_2_stages_ = form_2_stages()
    form_3_stages_ = form_3_stages()
    form_n_stages_ = form_n_stages()
    form_stable_ = form_stable()

    form_n_stages_errors = {"stages_1" : [], "stages_1_no_errors": [],"stages_1_errors": [], "stages_1_messages": [],\
    "stages_2" : [], "stages_2_no_errors": [] , "stages_2_errors": [], "stages_2_messages": [],\
    "stages_3" : [], "stages_3_no_errors": [] , "stages_3_errors": [], "stages_3_messages": [],\
    "stages_n" : [], "stages_n_no_errors": [] , "stages_n_errors": [], "stages_n_messages": [],\
    "stages_stable" : [], "stages_stable_no_errors": [] , "stages_stable_errors": [], "stages_stable_messages": [],\
    "html_df_input": []}
    for i, field in enumerate(first_info_form):
        if i > 0:
            form_n_stages_errors["stages_1"].append("#" + field.name)
    form_n_stages_errors["stages_1_no_errors"] = form_n_stages_errors["stages_1"].copy()

    if form_2_stages_.type_valuation.validate(form_2_stages_):
        print("==vao==form_2_stages_===>")
        for i, field in enumerate(form_2_stages_):
            if i == 22:
                form_n_stages_errors["stages_2"].append("#" + field.name + "_2_stages")
            if i > 22:
                form_n_stages_errors["stages_2"].append("." + field.name + "_2_stages")
        form_n_stages_errors["stages_2_no_errors"] = form_n_stages_errors["stages_2"].copy()

        if form_2_stages_.validate_on_submit():
            print("====form_2_stages_===========> ok ")
            #print("form_2_stages_.data: ", form_2_stages_.data)
            print(form_2_stages_.data)
            FCFE_value, FCFF_value, html_df_input = valuate_2_stages(form_2_stages_.data)
            form_n_stages_errors["FCFE_value"] = FCFE_value
            form_n_stages_errors["FCFF_value"] = FCFF_value
            form_n_stages_errors["html_df_input"] = html_df_input

            #print("FCFE_value: ", FCFE_value, " || ", "FCFF_value: ", FCFF_value)
            #print(type(form_2_stages_.data))
            #response = make_response(jsonify(form_n_stages_errors))
            #form_2_stages_.type_valuation.data = 0
            #response.set_cookie("data", json.dumps(form_2_stages_.data), max_age=timedelta(days=30))
            #return response
            return jsonify(form_n_stages_errors)
        else:
            #print(form_2_stages_.errors)
            #print(form_n_stages_errors)
            print(form_2_stages_.data)
            api_response(first_info_form, form_2_stages_, form_n_stages_errors, 2)

            for i, error in form_n_stages_errors.items():
                print(i, " || ", error)
                print("=======================================================================================================")
                """
                .custom-control-input.is-invalid~.custom-control-label  red
                .custom-control-input:valid~.custom-control-label    green
                """
            return jsonify(form_n_stages_errors)
    elif form_3_stages_.type_valuation.validate(form_3_stages_):
        print("===vao==form_3_stages_===========>")
        for i, field in enumerate(form_3_stages_):
            #print(i, " || ", field)
            if i == 22 or i ==23 or i >= 32:
                form_n_stages_errors["stages_3"].append("#" + field.name + "_3_stages")
            if i >= 24 and i <32:
                form_n_stages_errors["stages_3"].append("." + field.name + "_3_stages")
        #print("form_n_stages_errors: ", form_n_stages_errors["stages_3"])
        form_n_stages_errors["stages_3_no_errors"] = form_n_stages_errors["stages_3"].copy()

        if form_3_stages_.validate_on_submit():
            print("====form_3_stages_===========> ok")
            print(form_3_stages_.data)
            FCFE_value, FCFF_value, html_df_input = valuate_3_stages(form_3_stages_.data)
            form_n_stages_errors["FCFE_value"] = FCFE_value
            form_n_stages_errors["FCFF_value"] = FCFF_value
            form_n_stages_errors["html_df_input"] = html_df_input

            return jsonify(form_n_stages_errors)
        else:
            for i, error in form_3_stages_.errors.items():
                print(i, " || ", error)
            api_response(first_info_form, form_3_stages_, form_n_stages_errors, 3)
            return jsonify(form_n_stages_errors)

    elif form_n_stages_.type_valuation.validate(form_n_stages_):
        print("===vao==form_n_stages_===========>")
        for i, field in enumerate(form_n_stages_):
            #print(i, " || ", field)
            if i >= 22 and i <= 24:
                form_n_stages_errors["stages_n"].append("#" + field.name + "_n_stages")
            if i > 24:
                form_n_stages_errors["stages_n"].append("." + field.name + "_n_stages")
        form_n_stages_errors["stages_n_no_errors"] = form_n_stages_errors["stages_n"].copy()
        """
        for i, error in form_n_stages_errors.items():
            print(i, " || ", error)
            print("=======================================================================================================")
        """

        if form_n_stages_.validate_on_submit():
            print("====form_n_stages_===========> ok")
            #print(form_n_stages_.data)
            FCFE_value, FCFF_value, html_df_input = valuate_n_stages(form_n_stages_.data)
            form_n_stages_errors["FCFE_value"] = FCFE_value
            form_n_stages_errors["FCFF_value"] = FCFF_value
            form_n_stages_errors["html_df_input"] = html_df_input

            return jsonify(form_n_stages_errors)
        else:
            for i, error in form_n_stages_.errors.items():
                print(i, " || ", error)
            api_response(first_info_form, form_n_stages_, form_n_stages_errors, "n")
            return jsonify(form_n_stages_errors)

    elif form_stable_.type_valuation.validate(form_stable_):
        print("===vao==form_stable_===========>")
        if form_stable_.validate_on_submit():
            print("====form_stable_===========> ok")
            #print(form_n_stages_.data)
            FCFE_value, FCFF_value = valuate_stable(form_stable_.data)
            form_n_stages_errors["FCFE_value"] = FCFE_value
            form_n_stages_errors["FCFF_value"] = FCFF_value

            return jsonify(form_n_stages_errors)
        else:
            for i, error in form_stable_.errors.items():
                print(i, " || ", error)
            api_response(first_info_form, form_stable_, form_n_stages_errors, "stable")
            return jsonify(form_n_stages_errors)
    else:
        print(form_n_stages_.data)
        print("error ", form_n_stages_.type_valuation.errors)

@home_app.route('/save_valuation/', methods=['POST'])
def save_valuation():
    if not current_user.is_authenticated:
        return jsonify({"message":"Ban phai dang nhap moi luu duoc"})
    print("vao server: ============> ")
    data = request.get_json(cache=False)
    if data:
        #Lay attribute cua tung form, khong ke thua
        #pprint.pprint(data["form_3_stages"])

        attr_cls_info_form = get_attr_from_class(info_form)
        attr_cls_form_2_stages = get_attr_from_class(form_2_stages)
        attr_cls_form_3_stages = get_attr_from_class(form_3_stages)
        attr_cls_form_n_stages = get_attr_from_class(form_n_stages)
        #Lay du lieu cua tung form gui len khong ke thua
        data_info_form =  extract_data_from_form(attr_cls_info_form, data["form_input"])
        data_form_2_stages =  extract_data_from_form(attr_cls_form_2_stages, data["form_2_stages"])
        data_form_3_stages =  extract_data_from_form(attr_cls_form_3_stages, data["form_3_stages"])
        data_form_n_stages =  extract_data_from_form(attr_cls_form_n_stages, data["form_n_stages"])

        data_form = dict(dict(data_info_form, **data_form_2_stages), **dict(data_form_3_stages, **data_form_n_stages))
        data_form_keys = data_form.keys()
        data_form_multidict = MultiDict(list(data_form.items()))

        list_form = [info_form(data_form_multidict), form_2_stages(data_form_multidict), form_3_stages(data_form_multidict), form_n_stages(data_form_multidict)]
        for form in list_form:
            if not form.validate():
                for field, error in form.errors.items():
                    if field in data_form_keys:
                        #print("error: ", field)
                        data_form.pop(field)
        #for i, val in data_form.items():
            #print(i, "  || ", val)
        if "Stock_id_hidden" not in data_form.keys():
            return jsonify({"message":"Ban phai nhap chinh xac ma co phieu de luu"})
        stock_id = data_form["Stock_id_hidden"].upper()
        stock = report_yearly.objects.filter(stock_id=stock_id).count()
        if stock == 0:
            return jsonify({"message":"Khong co ma co phieu trong he thong"})
        stock_save = Save_valuation.objects.filter(stock_id=stock_id, from_user = current_user.id).first()
        #stock_save = Save_valuation.objects(stock_id=stock_id, from_user = current_user.id)
        #print(stock_save._query)
        #print(current_user.id)

        if stock_save is None:
            print("created")
            save_stock = Save_valuation(stock_id = stock_id,
                                        form_data = data_form,
                                        from_user = current_user.id)
            save_stock.save()
            return jsonify({"message":" Luu du lieu thanh cong"})
        else:
            print("update")
            stock_save.form_data = data_form
            stock_save.save()
            return jsonify({"message":" Update du lieu thanh cong"})

    return jsonify({"message":" Du lieu gui len khong hop le"})



"""
@facebook.tokengetter
def get_facebook_token():
    return session.get('facebook_token')

def pop_login_session():
    session.pop('logged_in', None)
    session.pop('facebook_token', None)

@home_app.route("/facebook_authorized")
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('home_app.home')
    print(request.args.get('next'))
    if resp is None or 'access_token' not in resp:
        return redirect(next_url)

    session['logged_in'] = True
    session['facebook_token'] = (resp['access_token'], '')

    return redirect(next_url)

@home_app.route('/facebook_login/', methods=['POST', 'GET'])
def facebook_login():
    return facebook.authorize(callback=url_for('home_app.facebook_authorized',
        next=request.args.get('next'), _external=True))

@home_app.route("/logout/")
def logout():
    pop_login_session()
    return redirect(url_for('home_app.home'))

def token_to_text(token):
    with open("token.txt", mode="w") as f_in:
        f_in.writelines(token)
"""
"""

"""




