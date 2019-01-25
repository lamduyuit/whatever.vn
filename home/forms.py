# coding: utf-8
from flask_wtf import FlaskForm
from wtforms import validators, StringField, FloatField, SubmitField, IntegerField, RadioField
from wtforms.validators import ValidationError

class home_form(FlaskForm):
	stock_id = StringField('',[
		validators.DataRequired(message="Ban phai nhap ma CP"),
        validators.length(min=3, max=3)
		])

class info_form(FlaskForm):
	"""docstring for vaidation_form"""
	Stock_id_hidden = StringField('Stock_id_hidden',[
        validators.length(min=3, max=3)
		])

	Initial_ROE = FloatField("Initial_ROE",[
		validators.DataRequired(message="Ban phai nhap Initial_ROE"),
        validators.NumberRange(min=0, max=200)
		])

	Initial_NI = FloatField("Initial_NI",[
		validators.DataRequired(message="Ban phai nhap Initial_NI"),
        validators.NumberRange(min=0, max=50000)
		])

	Initial_Chi_tieu_von_dau_tu = FloatField("Initial_Chi_tieu_von_dau_tu",[
		validators.DataRequired(message="Ban phai nhap Initial_Chi_tieu_von_dau_tu"),
        validators.NumberRange(min=0, max=50000)
		])

	Initial_KH = FloatField("Initial_KH",[
		validators.DataRequired(message="Ban phai nhap Initial_KH"),
        validators.NumberRange(min=0, max=20000)
		])

	Initial_Thay_doi_von_luu_dong = FloatField("Initial_Thay_doi_von_luu_dong",[
		validators.DataRequired(message="Ban phai nhap Initial_Thay_doi_von_luu_dong"),
        validators.NumberRange(min=0, max=50000)
		])

	Initial_No_phat_hanh_thuan = FloatField("Initial_No_phat_hanh_thuan",[
		validators.DataRequired(message="Ban phai nhap Initial_No_phat_hanh_thuan"),
        validators.NumberRange(min=-10000, max=50000)
		])

	Initial_ROC = FloatField("Initial_ROC",[
		validators.DataRequired(message="Ban phai nhap Initial_ROC"),
        validators.NumberRange(min=0, max=200)
		])

	Initial_EBIT_HDKD_AT = FloatField("Initial_EBIT_HDKD_AT",[
		validators.DataRequired(message="Ban phai nhap Initial_EBIT_HDKD_AT"),
        validators.NumberRange(min=0, max=50000)
		])

	Stable_g = FloatField("Stable_g",[
		validators.DataRequired(message="Ban phai nhap Stable_g"),
        validators.NumberRange(min=0, max=200)
		])

	Stable_ROE = FloatField("Stable_ROE",[
		validators.DataRequired(message="Ban phai nhap Stable_ROE"),
        validators.NumberRange(min=0, max=200)
		])

	Stable_ROC = FloatField("Stable_ROC",[
		validators.DataRequired(message="Ban phai nhap Stable_ROC"),
        validators.NumberRange(min=0, max=200)
		])

	Tax = FloatField("Tax",[
		validators.DataRequired(message="Ban phai nhap Tax"),
        validators.NumberRange(min=5, max=30)
		])

	Lai_suat_vay = FloatField("Lai_suat_vay",[
		validators.DataRequired(message="Ban phai nhap Lai_suat_vay"),
        validators.NumberRange(min=4, max=20)
		])

	Beta = FloatField("Beta",[
		validators.DataRequired(message="Ban phai nhap Beta"),
        validators.NumberRange(min=0, max=2)
		])

	Lai_suat_phi_rui_ro = FloatField("Lai_suat_phi_rui_ro",[
		validators.DataRequired(message="Ban phai nhap Lai_suat_phi_rui_ro"),
        validators.NumberRange(min=0, max=12)
		])

	Phan_bu_rui_ro = FloatField("Phan_bu_rui_ro",[
		validators.DataRequired(message="Ban phai nhap Phan_bu_rui_ro"),
        validators.NumberRange(min=0, max=20)
		])

	Tong_no_vay = FloatField("Tong_no_vay",[
		validators.DataRequired(message="Ban phai nhap Tong_no_vay"),
        validators.NumberRange(min=0, max=50000)
		])

	Shares_Outstand = FloatField("Shares_Outstand",[
		validators.DataRequired(message="Ban phai nhap Shares_Outstand"),
        validators.NumberRange(min=1000, max=4000000000)
		])
	Cash_Investment = FloatField("Cash_Investment",[
		validators.DataRequired(message="Ban phai nhap Cash_Investment"),
        validators.NumberRange(min=0, max=50000)
		])


class form_2_stages (info_form):

	type_valuation = IntegerField("type_valuation",[
		validators.DataRequired(),
        validators.NumberRange(min=2, max=2)
		])

	first_n_year = IntegerField("First_stages_n_year",[
		validators.DataRequired(),
        validators.NumberRange(min=3, max=12)
		])

	change_expected_growth_rate_NI = RadioField("Change_growth_NI",[
		validators.DataRequired(message="Ban phai chon"),
		], choices=[("1", "True"), ("0", "False")])

	change_expected_growth_rate_EBIT_AT = RadioField("Change_growth_EBIT_AT",[
		validators.DataRequired(message="Ban phai chon"),
		], choices=[("1", "True"), ("0", "False")])

	change_ROE = RadioField("Change_ROE",[
		validators.DataRequired(message="Ban phai chon"),
		], choices=[("1", "True"), ("0", "False")])

	change_ROC = RadioField("Change_ROC",[
		validators.DataRequired(message="Ban phai chon"),
		], choices=[("1", "True"), ("0", "False")])

	change_Ke = RadioField("Change_Ke",[
		validators.DataRequired(message="Ban phai chon"),
		], choices=[("1", "True"), ("0", "False")])

	change_WACC = RadioField("Change_WACC",[
		validators.DataRequired(message="Ban phai chon"),
		], choices=[("1", "True"), ("0", "False")])

class form_3_stages (info_form):
	type_valuation = IntegerField("type_valuation",[
		validators.DataRequired(),
        validators.NumberRange(min=3, max=3)
		])

	first_stages_n_year = IntegerField("First_stages_n_year",[
		validators.DataRequired(),
        validators.NumberRange(min=3, max=8)
		])
	second_stages_n_year = IntegerField("Second_stages_n_year",[
		validators.DataRequired(),
        validators.NumberRange(min=3, max=8)
		])

	first_stages_change_expected_growth_rate_NI = RadioField("First_stages_change_g_NI",[
		validators.DataRequired(message="Ban phai chon"),
		], choices=[("1", "True"), ("0", "False")])

	first_stages_change_expected_growth_rate_EBIT_AT = RadioField("First_stages_change_g_EBIT_AT",[
		validators.DataRequired(message="Ban phai chon"),
		], choices=[("1", "True"), ("0", "False")])

	first_stages_change_ROE = RadioField("First_stages_change_ROE",[
		validators.DataRequired(message="Ban phai chon"),
		], choices=[("1", "True"), ("0", "False")])

	first_stages_change_ROC = RadioField("First_stages_change_ROC",[
		validators.DataRequired(message="Ban phai chon"),
		], choices=[("1", "True"), ("0", "False")])

	second_stages_change_expected_growth_rate_NI = RadioField("Second_stages_change_g_NI",[
		validators.DataRequired(message="Ban phai chon"),
		], choices=[("1", "True"), ("0", "False")])

	second_stages_change_expected_growth_rate_EBIT_AT = RadioField("Second_stages_change_g_EBIT_AT",[
		validators.DataRequired(message="Ban phai chon"),
		], choices=[("1", "True"), ("0", "False")])

	second_stages_change_ROE = RadioField("Second_stages_change_ROE",[
		validators.DataRequired(message="Ban phai chon"),
		], choices=[("1", "True"), ("0", "False")])

	second_stages_change_ROC = RadioField("Second_stages_change_ROC",[
		validators.DataRequired(message="Ban phai chon"),
		], choices=[("1", "True"), ("0", "False")])

	second_stages_g_NI = FloatField("Second_stages_g_NI",[
		validators.DataRequired(message="Ban phai nhap Second_stages_g_NI"),
        validators.NumberRange(min=0, max=200)
		])

	second_stages_ROE = FloatField("Second_stages_ROE",[
		validators.DataRequired(message="Ban phai nhap Second_stages_ROE"),
        validators.NumberRange(min=0, max=200)
		])

	second_stages_g_EBIT_AT = FloatField("Second_stages_g_EBIT_AT",[
		validators.DataRequired(message="Ban phai nhap Second_stages_g_EBIT_AT"),
        validators.NumberRange(min=0, max=200)
		])

	second_stages_ROC = FloatField("Second_stages_ROC",[
		validators.DataRequired(message="Ban phai nhap Second_stages_ROC"),
        validators.NumberRange(min=0, max=200)
		])

class form_n_stages (info_form):
	type_valuation = IntegerField("type_valuation",[
		validators.DataRequired(),
        validators.NumberRange(min=4, max=4)
		])

	fix_n_year = IntegerField("Fix_n_year",[
		validators.DataRequired(),
        validators.NumberRange(min=5, max=30)
		])

	Initial_g_NI = FloatField("Initial_g_NI",[
		validators.DataRequired(message="Ban phai nhap Initial_g_NI"),
        validators.NumberRange(min=0, max=200)
		])

	Initial_g_EBIT_AT = FloatField("Initial_g_EBIT_AT",[
		validators.DataRequired(message="Ban phai nhap Initial_g_EBIT_AT"),
        validators.NumberRange(min=0, max=200)
		])

	change_expected_growth_rate_NI_n = RadioField("Change_g_NI",[
		validators.DataRequired(message="Ban phai chon"),
		], choices=[("1", "True"), ("0", "False")])

	change_expected_growth_rate_EBIT_n = RadioField("Change_g_EBIT_AT",[
		validators.DataRequired(message="Ban phai chon"),
		], choices=[("1", "True"), ("0", "False")])

	change_Ke_n = RadioField("Change_Ke",[
		validators.DataRequired(message="Ban phai chon"),
		], choices=[("1", "True"), ("0", "False")])

	change_WACC_n = RadioField("Change_WACC",[
		validators.DataRequired(message="Ban phai chon"),
		], choices=[("1", "True"), ("0", "False")])
class form_stable (info_form):
	type_valuation = IntegerField("type_valuation",[
		validators.DataRequired(),
        validators.NumberRange(min=5, max=5)
		])




	

		