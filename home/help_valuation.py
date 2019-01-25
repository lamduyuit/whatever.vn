from home.models import *
from datetime import datetime
import pandas as pd
from collections import namedtuple
from home.forms import info_form, form_2_stages, form_3_stages, form_n_stages
from pprint import pprint
#from random import random

def get_list_form(form_data = None, stock_id = True, No_vay = None, Cash_Investment = None, Shares = None):
    if form_data:
        first_info_form = info_form(formdata  = form_data)
        form_2_stages_ = form_2_stages(formdata  = form_data)
        form_3_stages_ = form_3_stages(formdata  = form_data)
        form_n_stages_ = form_n_stages(formdata  = form_data)
        return first_info_form, form_2_stages_, form_3_stages_, form_n_stages_
    elif stock_id:
        first_info_form = info_form()
        info_form_data =  first_info_form.data
        info_form_data["Tong_no_vay"] = No_vay
        info_form_data["Cash_Investment"] = Cash_Investment
        info_form_data["Shares_Outstand"] = round(Shares/1000000, 2)
        info_form_data = create_obj(info_form_data)
        first_info_form = info_form(obj = info_form_data)
        #pprint(first_info_form.data)

        form_2_stages_ = form_2_stages()
        form_3_stages_ = form_3_stages()
        form_n_stages_ = form_n_stages()
        return first_info_form, form_2_stages_, form_3_stages_, form_n_stages_
    elif stock_id is False:
        first_info_form = info_form()
        form_2_stages_ = form_2_stages()
        form_3_stages_ = form_3_stages()
        form_n_stages_ = form_n_stages()
        return first_info_form, form_2_stages_, form_3_stages_, form_n_stages_


def create_obj(dict_obj):
	MyStruct = namedtuple("MyStruct", " ".join(dict_obj.keys()))
	s = MyStruct(**dict_obj)
	return s


def get_attr_from_class(cls_name):
	func_list_attr = []
	for attr in cls_name.__dict__.keys():
		if not attr.startswith("__") and not attr.startswith("_"):
			func_list_attr.append(attr)
	return func_list_attr
def extract_data_from_form(cls_attr, data_form):
	keys = list(data_form.keys()).copy()
	for key in keys:
		if key not in cls_attr:
			data_form.pop(key)
	if "type_valuation" in keys:
		data_form.pop("type_valuation")
	return data_form

def api_response(first_form, second_form, form_errors, stages):
    for field_name, messages_error in second_form.errors.items():
        if(first_form.__contains__(field_name)):
            form_errors["stages_1_errors"].append("#" + field_name)
            form_errors["stages_1_no_errors"].pop(form_errors["stages_1_no_errors"].index("#" + field_name))
            form_errors["stages_1_messages"].append(messages_error[0])
        else:
            if("change" not in field_name):
                form_errors["stages_" + str(stages) + "_errors"].append("#" + field_name + "_" + str(stages) + "_stages")
                form_errors["stages_" + str(stages) + "_no_errors"].pop(form_errors["stages_" + str(stages) + "_no_errors"].index("#" + field_name + "_" + str(stages) + "_stages"))
                form_errors["stages_" + str(stages) + "_messages"].append(messages_error[0])
            else:
                form_errors["stages_" + str(stages) + "_errors"].append("." + field_name + "_" + str(stages) + "_stages")
                form_errors["stages_" + str(stages) + "_no_errors"].pop(form_errors["stages_" + str(stages) + "_no_errors"].index("." + field_name + "_" + str(stages) + "_stages"))
                form_errors["stages_" + str(stages) + "_messages"].append(messages_error[0])


def color_negative_red(value):
	    """ Colors elements in a dateframe green if positive and red if negative. Does not color NaN values.
	      """
	    if value < 0:
	        color = 'red'
	        font_w = "bold"
	        back_c = "#f8f9fa"
	    elif value > 0:
	        color = 'green'
	        font_w = "bold"
	        back_c = "#f8f9fa"
	    else:
	        color = 'black'
	        font_w = "normal"
	        back_c = "white"
	    return 'color: {0}; font-weight: {1}; background-color: {2}'.format(color, font_w, back_c)
	    #return 'color: %s; background-color: #FFA500' % color
def color_index(value):
    return "font-weight:bold"

# Set CSS properties for th elements in dataframe
th_props = [
  ('text-align', 'center'),
  ('font-weight', 'bold'),
  ]

# Set CSS properties for td elements in dataframe
td_props = [
    ('text-align', 'center'),
  ]

# Set table styles
styles = [
  dict(selector="th", props=th_props),
  dict(selector="td", props=td_props)
  ]
#Lấy dữ liệu để định giá trong Database
def get_df_input(stock_id):
	#stock_id = "HPG"
	year_now = 2018
	n_year = year_now - 6

	#Ham loc lai data theo quy
	def change_type_df_q(df,year):
	    df = pd.DataFrame(df.data)
	    df.set_index("STT",inplace=True)
        # df.set_index("index",inplace=True)
	    df.index = df.index.astype("int")
	    df["Year"] = df["Year"].astype("int")
	    #print(df.columns[1:6])
	    for col in df.columns[2:6]:
	        df[col] = df[col].astype("float")
	    return df[df["Year"]>=year]

	#Ham loc lai data theo nam
	def change_type_df_y(df,year):
	    df = pd.DataFrame(df.data)
	    df.set_index("STT",inplace=True)
        # df.set_index("index",inplace=True)
	    df.index = df.index.astype("int")
	    df.sort_index(inplace= True)
	    attr = df["Attribute"]

	    df.drop("Attribute",inplace=True,axis=1)
	    df.insert(0,"Attribute",attr)
	    data = df[df.columns[1:][-(int(df.columns[-1])-year+1):]]
	    df = df[df.columns[0]].to_frame().join(data)
	    df.index = df.index.astype("int")
	    for col in df.columns[1:]:
	        df[col] = df[col].astype("float")
	    return df

	#Lay data quy chi gom kqkd va cdkt
	data_quy = report_quaterly.objects.filter(stock_id=stock_id)
	if data_quy.count() == 0:
		return None, None, None
	list_reports_name = []
	for i in data_quy:
	    if i.report_name == "KQKD":
	        list_reports_name.append(i.report_name)
	        kqkd_quy = change_type_df_q(i,n_year)
	    if i.report_name == "CDKT":
	        list_reports_name.append(i.report_name)
	        cdkt_quy = change_type_df_q(i,n_year)
	if "KQKD" not in list_reports_name or "CDKT" not in list_reports_name:
		return None, None, None

	#Lay data theo nam
	data_nam  = report_yearly.objects.filter(stock_id=stock_id)
	if data_nam.count() == 0:
		return None, None, None

	list_reports = []
	shares = 0
	for y_data in data_nam:
	    list_reports.append(y_data.report_name)
	    #print(y_data.report_name)
	    if y_data.report_name == "CDKT":
	        shares = (y_data.shares)
	        # print("shares: =============> ", shares)
	        cdkt_nam = change_type_df_y(y_data,n_year)
	        cdkt_nam.iloc[:, 1:] = cdkt_nam.iloc[:, 1:]/1000
	    if y_data.report_name == "KQKD":
	        kqkd_nam = change_type_df_y(y_data,n_year)
	        kqkd_nam.iloc[:, 1:] = kqkd_nam.iloc[:, 1:]/1000
	    if y_data.report_name == "LCTT":
	        Lctt_nam = change_type_df_y(y_data,n_year)
	        Lctt_nam.iloc[:, 1:] = Lctt_nam.iloc[:, 1:]/1000
	    if y_data.report_name == "CSTC":
	        cstc_nam = change_type_df_y(y_data,n_year)

	Chi_tieu_tscd_huu_hinh = cdkt_nam.iloc[38,1:] - cdkt_nam.iloc[38,1:].shift(1)
	Chi_tieu_tscd_thue_tc = cdkt_nam.iloc[41,1:] - cdkt_nam.iloc[41,1:].shift(1)
	Chi_tieu_tscd_vo_hinh = cdkt_nam.iloc[44,1:] - cdkt_nam.iloc[44,1:].shift(1)
	Chi_tai_san_do_dang_dai_han = cdkt_nam.iloc[49,1:] - cdkt_nam.iloc[49,1:].shift(1)
	Chi_tieu_von_dau_tu = Chi_tieu_tscd_huu_hinh + Chi_tieu_tscd_thue_tc + Chi_tieu_tscd_vo_hinh + Chi_tai_san_do_dang_dai_han

	Khau_hao_luy_ke = cdkt_nam.iloc[[39, 42, 45], 1:]
	Khau_hao = (Khau_hao_luy_ke.sum() - Khau_hao_luy_ke.sum().shift())*-1

	NOWC_thuan = cdkt_nam.iloc[1, 1:] - cdkt_nam.iloc[[2,5], 1:].sum() - (cdkt_nam.iloc[68, 1:] - cdkt_nam.iloc[78, 1:])
	Thay_doi_von_luu_dong = NOWC_thuan - NOWC_thuan.shift()

	Ty_le_NOWC_vs_DT = NOWC_thuan/kqkd_nam.iloc[2, 1:]

	Tong_no_vay = cdkt_nam.iloc[78, 1:] + cdkt_nam.iloc[91, 1:]
	#print("Tong_no_vay: ", Tong_no_vay)

	No_phat_hanh_thuan = Tong_no_vay - Tong_no_vay.shift()

	# Lợi nhuận sau điều chỉnh = EBT - Tax - Tax được hoãn lại bình quân
	NI_dieu_chinh_tax = kqkd_nam.iloc[16, 1:] - kqkd_nam.iloc[17, 1:] - kqkd_nam.iloc[18, 1:].drop(str(year_now)).mean()

	#Ty le dong thue duoc dieu chinh
	Thue_suat_dieu_chinh = (kqkd_nam.iloc[16, 1:] - NI_dieu_chinh_tax)/kqkd_nam.iloc[16, 1:]

	# Tỷ lệ đóng thuế thực
	Thue_suat_thuc = (kqkd_nam.iloc[16, 1:] - kqkd_nam.iloc[19, 1:])/kqkd_nam.iloc[16, 1:]

	# Điều chỉnh Net income, loại trừ thu nhập khác, thu nhập tài chính
	EBT_HDKT = kqkd_nam.iloc[16, 1:] - kqkd_nam.iloc[14, 1:] - (kqkd_nam.iloc[5, 1:] - kqkd_nam.iloc[6, 1:] + kqkd_nam.iloc[7, 1:])
	NI_HDKT = EBT_HDKT*(1- Thue_suat_thuc)

	#Tính EBIT và EBIT*(1-T) riêng HĐKD
	EBIT_HDKD = (EBT_HDKT + kqkd_nam.iloc[7, 1:])
	EBIT_HDKD_AT = EBIT_HDKD * (1- Thue_suat_thuc)

	#Tính ROE từ HĐKD
	BV_VCSH_dieu_chinh = cdkt_nam.iloc[98, 1:] - cdkt_nam.iloc[2, 1:] - cdkt_nam.iloc[5, 1:]
	#print("Cash and Investment: ", cdkt_nam.iloc[2, 1:], cdkt_nam.iloc[5, 1:])
	BV_VCSH_TB = (BV_VCSH_dieu_chinh + BV_VCSH_dieu_chinh.shift())/2
	ROE_HDKD = NI_HDKT/BV_VCSH_TB

	#Tính tổng nguồn vốn đầu tư = BV VCSH + Nợ vay chịu lãi
	BV_VCSH_NV_dieu_chinh = BV_VCSH_dieu_chinh + Tong_no_vay
	BV_VCSH_NV_TB = (BV_VCSH_NV_dieu_chinh + BV_VCSH_NV_dieu_chinh.shift())/2
	# Tính ROC từ HDKD:
	ROC_HDKD = EBIT_HDKD_AT/BV_VCSH_NV_TB

	FCFE = NI_HDKT - (Chi_tieu_von_dau_tu - Khau_hao) - Thay_doi_von_luu_dong + No_phat_hanh_thuan

	Table_FCFE = pd.concat([NI_HDKT.to_frame().T, EBIT_HDKD_AT.to_frame().T, BV_VCSH_TB.to_frame().T, BV_VCSH_NV_TB.to_frame().T, Chi_tieu_von_dau_tu.to_frame().T,
	                        Khau_hao.to_frame().T, Thay_doi_von_luu_dong.to_frame().T, No_phat_hanh_thuan.to_frame().T,
	                        Ty_le_NOWC_vs_DT.to_frame().T, kqkd_nam.iloc[2, 1:].to_frame().T,
	                        NOWC_thuan.to_frame().T, ROE_HDKD.to_frame().T, ROC_HDKD.to_frame().T])

	Table_FCFE.index = ["NI_HDKT", "EBIT_HDKD_AT", "BV_VCSH_TB", "BV_VCSH_NV_TB", "Chi_tieu_von_dau_tu", "Khau_hao", "Thay_doi_von_luu_dong", "No_phat_hanh_thuan",
	                    "Ty_le_NOWC_vs_DT", "Doanh_thu_thuan", "NOWC_thuan", "ROE_HDKD", "ROC_HDKD"]
	Table_FCFE = Table_FCFE.T

	Table_FCFE["Tai_dau_tu"] = Table_FCFE["Chi_tieu_von_dau_tu"] - Table_FCFE["Khau_hao"] + Table_FCFE["Thay_doi_von_luu_dong"]
	Table_FCFE["Ty_le_no_tren_tai_dau_tu"] = Table_FCFE["No_phat_hanh_thuan"]/Table_FCFE["Tai_dau_tu"]
	Table_FCFE["FCFE"] = Table_FCFE["NI_HDKT"] - Table_FCFE["Tai_dau_tu"] + Table_FCFE["No_phat_hanh_thuan"]
	Table_FCFE["FCFF"] = Table_FCFE["EBIT_HDKD_AT"] - Table_FCFE["Tai_dau_tu"]
	Table_FCFE["Tai_dau_tu_VCP"] = (Table_FCFE["Tai_dau_tu"] - Table_FCFE["No_phat_hanh_thuan"])
	Table_FCFE["Ty_le_Tai_dau_tu_VCP"] = 1 - (Table_FCFE["FCFE"]/Table_FCFE["NI_HDKT"])
	Table_FCFE["Ty_le_Tai_dau_tu"] = 1 - (Table_FCFE["FCFF"]/Table_FCFE["EBIT_HDKD_AT"])
	Table_FCFE.dropna(inplace=True)

	def Table_FCFE_TB(Table_FCFE_def = None, n_current_year = None, drop_trailing = True):
	    #n_current_year: số năm gần nhất, vd: n_current_year = 5 thì 5 năm gần nhất bao gồm trailling(nếu có) và 4 năm gần nhất
	    #không có trailling
	    if drop_trailing == True and kqkd_quy[kqkd_quy["Year"] == year_now].shape[0] > 0:
	        Table_FCFE_def.drop(str(year_now), inplace=True)
	        n_current_year = n_current_year - 1
	    #print(Table_FCFE_def)
	    #print((len(Table_FCFE_def.index) - n_current_year))
	    Table_FCFE_def = Table_FCFE_def.iloc[(len(Table_FCFE_def.index) - n_current_year):].copy()
	    #print("===========================================================================================")
	    #print(Table_FCFE_def)

	    Table_FCFE_def.loc["Trung_binh"] = Table_FCFE_def.mean()
	    Table_FCFE_def.loc["Tong"] = Table_FCFE_def.iloc[:-1].sum()

	    # Tính bình quân các tham số theo tổng
	    #Tinh ROE và ROC bao gồm cả ROE trailing dựa trên 4 quý gần nhất
	    ROE_BQ_T = Table_FCFE_def.loc["Tong", "NI_HDKT"]/Table_FCFE_def.loc["Tong", "BV_VCSH_TB"]
	    ROC_BQ_T = Table_FCFE_def.loc["Tong", "EBIT_HDKD_AT"]/Table_FCFE_def.loc["Tong", "BV_VCSH_NV_TB"]
	    #Tính tỷ lệ nợ phát hành thuần bình quân/tái đầu tư để tính phần tài trợ của nợ trong Vốn tái đầu tư
	    No_phat_hanh_thuan_BQ_T = Table_FCFE_def.loc["Tong", "No_phat_hanh_thuan"]/Table_FCFE_def.loc["Tong", "Tai_dau_tu"]
	    #Tính tỷ lệ tái đầu tư vốn cổ phần và tỷ lệ tái đầu tư/EBIT_HDKD_AT để tính tốc độ tăng trưởng
	    Tai_dau_tu_VCP = Table_FCFE_def.loc["Tong", "Tai_dau_tu_VCP"]/Table_FCFE_def.loc["Tong", "NI_HDKT"]
	    Tai_dau_tu = Table_FCFE_def.loc["Tong", "Tai_dau_tu"]/Table_FCFE_def.loc["Tong", "EBIT_HDKD_AT"]
	    #Tính bình quân tỷ trọng NOWC thuần/ doanh thu thuần
	    Ty_le_NOWC_vs_DT = Table_FCFE_def.loc["Tong", "NOWC_thuan"]/Table_FCFE_def.loc["Tong", "Doanh_thu_thuan"]
	    #Tính thay đổi NOWC điều chỉnh dựa trên bình quân tỷ trọng NOWC thuần/ doanh thu thuần

	    Table_FCFE_def.loc["Trung_binh_DC"] = [0  for i in range(len(Table_FCFE_def.columns))]
	    Table_FCFE_def.loc["Trung_binh_DC",
	                          ["ROE_HDKD", "ROC_HDKD", "Ty_le_no_tren_tai_dau_tu",
	                           "Ty_le_Tai_dau_tu_VCP", "Ty_le_Tai_dau_tu", "Ty_le_NOWC_vs_DT"]] = [ROE_BQ_T,
	                                                                                         ROC_BQ_T,No_phat_hanh_thuan_BQ_T,
	                                                                                         Tai_dau_tu_VCP, Tai_dau_tu,
	                                                                                         Ty_le_NOWC_vs_DT]
	    return Table_FCFE_def

	def Final_Table_FCFE(n_current_year = None):
	    if kqkd_quy[kqkd_quy["Year"] == year_now].shape[0] > 0:
	        tmp_1 = Table_FCFE_TB(Table_FCFE.copy(), n_current_year, False)
	        tmp_2 = Table_FCFE_TB(Table_FCFE.copy(), n_current_year, True)
	        tmp_2 = tmp_2.iloc[-3:]
	        tmp_2.index = ["TB_drop_trailing_" + str(n_current_year-1), "Tong_drop_trailing_" + str(n_current_year-1),
	                       "TB_DC_drop_trailing_" + str(n_current_year-1)]
	        return pd.concat([tmp_1, tmp_2])
	    else:
	        return Table_FCFE_TB(Table_FCFE.copy(), n_current_year, True)

	df_input = Final_Table_FCFE(5)


	#Cần chú ý đến trường hợp slice Index khi có thêm traillig =================================================>
	tmp_slice = None
	if len(df_input.index) <= 8:
	    df_input.drop(df_input.index[-2], inplace=True)
	    n_row_df_input = len(df_input.index)
	    tmp_slice = [(n_row_df_input-1), (n_row_df_input-2)]
	else:
	    df_input.drop(df_input.index[[-2, -5]], inplace=True)
	    n_row_df_input = len(df_input.index)
	    tmp_slice = [t for t in range(n_row_df_input-4, n_row_df_input)]

	df_input.reset_index(inplace=True)
	#df_input.set_index("index", inplace=True)
	#print(df_input)
	#df_input.replace(0, "-", inplace=True)
	styler = df_input.style.format("{:>8,.0f}", subset = ["NI_HDKT", "EBIT_HDKD_AT", "BV_VCSH_TB",\
	                                             "BV_VCSH_NV_TB", "Chi_tieu_von_dau_tu", "Khau_hao",\
	                                             "Thay_doi_von_luu_dong", "No_phat_hanh_thuan", "Doanh_thu_thuan",\
	                                             "NOWC_thuan", "Tai_dau_tu", "FCFE", "FCFF", "Tai_dau_tu_VCP"])\
	                .format("{:>.2%}", subset = ["Ty_le_NOWC_vs_DT", "ROE_HDKD", "ROC_HDKD", "Ty_le_no_tren_tai_dau_tu",\
	                                             "Ty_le_Tai_dau_tu_VCP", "Ty_le_Tai_dau_tu"])\
	                .set_table_styles(styles)\
	                .applymap(color_negative_red, subset=pd.IndexSlice[tmp_slice, \
	                                                                   ["NI_HDKT", "EBIT_HDKD_AT", "Chi_tieu_von_dau_tu", \
	                                                                   "Khau_hao", "Thay_doi_von_luu_dong", "No_phat_hanh_thuan", \
	                                                                   "Ty_le_NOWC_vs_DT", "ROE_HDKD", "ROC_HDKD", \
	                                                                   "Ty_le_no_tren_tai_dau_tu", "Ty_le_Tai_dau_tu_VCP", \
	                                                                   "Ty_le_Tai_dau_tu"]])\
	                .applymap(color_index, subset = ["index"]).hide_index()\
	                .set_table_attributes('class= "table table-hover table-responsive-md"')
	first_range = list(df_input.columns[1:8])
	second_range = list(df_input.columns[8:14])
	third_range = list(df_input.columns[14:])

	html_df_input = []




	first_html_df_input = "".join(styler.hide_columns(second_range + third_range).render().split("\n"))
	html_df_input.append(first_html_df_input)
	#print(first_html_df_input)
	#print("=============================================================================================")
	second_html_df_input = "".join(styler.hide_columns(first_range + third_range).render().split("\n"))
	html_df_input.append(second_html_df_input)
	#print(second_html_df_input)
	#print("=============================================================================================")
	third_html_df_input = "".join(styler.hide_columns(first_range + second_range).render().split("\n"))
	html_df_input.append(third_html_df_input)
	#print("".join(html_df_input))
	"""
	print(html_df_input[0])
	print("=============================================================================================")
	print(html_df_input[1])
	print("=============================================================================================")
	print(html_df_input[2])
	"""
	cdkt_nam.iloc[2, 1:] - cdkt_nam.iloc[5, 1:]
	No_vay = 0
	if Tong_no_vay.iloc[-1] > 0:
		No_vay = round(Tong_no_vay.iloc[-1], 2)
		Cash_Investment = round((cdkt_nam.iloc[2, 1:].iloc[-1] + cdkt_nam.iloc[5, 1:].iloc[-1]), 2)
	else:
		No_vay = round(Tong_no_vay.iloc[-2], 2)
		Cash_Investment = round((cdkt_nam.iloc[2, 1:].iloc[-2] + cdkt_nam.iloc[5, 1:].iloc[-2]), 2)
	return html_df_input, No_vay, Cash_Investment, shares


def valuate_2_stages(data):
	Initial_ROE = data["Initial_ROE"]/100
	Initial_NI = data["Initial_NI"]
	Initial_Chi_tieu_von_dau_tu = data["Initial_Chi_tieu_von_dau_tu"]
	Initial_KH = data["Initial_KH"]
	Initial_Thay_doi_von_luu_dong = data["Initial_Thay_doi_von_luu_dong"]
	Initial_No_phat_hanh_thuan = data["Initial_No_phat_hanh_thuan"]

	Initial_Tai_dau_tu = (Initial_Chi_tieu_von_dau_tu - Initial_KH) + Initial_Thay_doi_von_luu_dong
	Initial_FCFE = Initial_NI - Initial_Tai_dau_tu + Initial_No_phat_hanh_thuan
	Initial_Ty_le_Tai_dau_tu_VCP = 1 - Initial_FCFE/Initial_NI
	Initial_Ty_le_no_tren_tai_dau_tu = Initial_No_phat_hanh_thuan/Initial_Tai_dau_tu
	first_g = Initial_ROE * Initial_Ty_le_Tai_dau_tu_VCP

	Initial_ROC = data["Initial_ROC"]/100
	Initial_EBIT_HDKD_AT = data["Initial_EBIT_HDKD_AT"]
	Initial_FCFF = Initial_EBIT_HDKD_AT - Initial_Tai_dau_tu
	Initial_Ty_le_Tai_dau_tu = Initial_Tai_dau_tu/Initial_EBIT_HDKD_AT
	first_g_FCFF = Initial_ROC * Initial_Ty_le_Tai_dau_tu

	Stable_g = data["Stable_g"]/100
	Stable_ROE = data["Stable_ROE"]/100
	Stable_ROC = data["Stable_ROC"]/100
	Stable_Ty_le_Tai_dau_tu_VCP = Stable_g/Stable_ROE
	Stable_Ty_le_Tai_dau_tu = Stable_g/Stable_ROC

	Tax = data["Tax"]/100
	Initial_Ty_le_no_vay = Initial_Ty_le_no_tren_tai_dau_tu
	Initial_Ty_le_VCP = 1 - Initial_Ty_le_no_vay
	Lai_suat_vay = data["Lai_suat_vay"]/100
	Beta = data["Beta"]
	Lai_suat_phi_rui_ro = data["Lai_suat_phi_rui_ro"]/100
	Phan_bu_rui_ro = data["Phan_bu_rui_ro"]/100
	Initial_Chi_phi_von_co_phan = Lai_suat_phi_rui_ro + Beta*Phan_bu_rui_ro
	#print(Initial_Chi_phi_von_co_phan)
	Initial_WACC = Lai_suat_vay * (1-Tax) * Initial_Ty_le_no_vay + Initial_Chi_phi_von_co_phan * Initial_Ty_le_VCP


	Stable_Ty_le_no_vay = Initial_Ty_le_no_vay
	Stable_Ty_le_VCP = 1 - Stable_Ty_le_no_vay

	Stable_Chi_phi_von_co_phan = Lai_suat_phi_rui_ro + 1*Phan_bu_rui_ro
	Stable_WACC = Lai_suat_vay * (1-Tax) * Stable_Ty_le_no_vay + Stable_Chi_phi_von_co_phan * Stable_Ty_le_VCP


	first_stages_n_year = data["first_n_year"]
	Shares_Outstand = data["Shares_Outstand"]*1000000
	Tong_no_vay = data["Tong_no_vay"]
	Cash_Investment = data["Cash_Investment"]

	df_FCFE = pd.DataFrame(columns=[i+1 for i in range(first_stages_n_year)])
	df_FCFE["Terminal Year"] = None

	change_expected_growth_rate_NI = True if data["change_expected_growth_rate_NI"] == "1" else False
	change_expected_growth_rate_EBIT = True if data["change_expected_growth_rate_EBIT_AT"] == "1" else False
	change_ROE = True if data["change_ROE"] == "1" else False
	change_ROC = True if data["change_ROC"] == "1" else False
	change_Ke = True if data["change_Ke"] == "1" else False
	change_WACC = True if data["change_WACC"] == "1" else False

	for cols_df_FCFE in df_FCFE.columns[:-1]:
	    #print(type(cols_df_FCFE))
	    #print(cols_df_FCFE)
	    df_FCFE.loc["ROE_HDKD", cols_df_FCFE] = Initial_ROE
	    df_FCFE.loc["ROC_HDKD", cols_df_FCFE] = Initial_ROC
	    df_FCFE.loc["EQ_Reinvestment rate", cols_df_FCFE] = Initial_Ty_le_Tai_dau_tu_VCP
	    df_FCFE.loc["Reinvestment rate", cols_df_FCFE] = Initial_Ty_le_Tai_dau_tu
	    df_FCFE.loc["Expected growth rate NI", cols_df_FCFE] = first_g
	    df_FCFE.loc["Expected growth rate EBIT_AT", cols_df_FCFE] = first_g_FCFF

	    if cols_df_FCFE == 1:
	        df_FCFE.loc["Ke", cols_df_FCFE] = Initial_Chi_phi_von_co_phan
	        df_FCFE.loc["WACC", cols_df_FCFE] = Initial_WACC
	        df_FCFE.loc["Net Income", cols_df_FCFE] = Initial_NI*(1+df_FCFE.loc["Expected growth rate NI", cols_df_FCFE])
	        df_FCFE.loc["EBIT_HDKD_AT", cols_df_FCFE] = Initial_EBIT_HDKD_AT*(1+df_FCFE.loc["Expected growth rate EBIT_AT", cols_df_FCFE])
	    else:
	        #Tính tốc độ thay đổi của tốc độ tăng trưởng nếu đặt ra giả thiết này
	        if change_expected_growth_rate_NI:
	            tmp_g_NI = ((Stable_g/first_g)**(1/first_stages_n_year))-1
	            df_FCFE.loc["Expected growth rate NI", cols_df_FCFE] = df_FCFE.loc["Expected growth rate NI", (cols_df_FCFE-1)] * (1 + tmp_g_NI)
	        if change_expected_growth_rate_EBIT:
	            tmp_g_EBIT = ((Stable_g/first_g_FCFF)**(1/first_stages_n_year))-1
	            df_FCFE.loc["Expected growth rate EBIT_AT", cols_df_FCFE] = df_FCFE.loc["Expected growth rate EBIT_AT", (cols_df_FCFE-1)] * (1 + tmp_g_EBIT)

	        if change_ROC:
	            tmp_ROC = ((Stable_ROC/Initial_ROC)**(1/first_stages_n_year))-1
	            df_FCFE.loc["ROC_HDKD", cols_df_FCFE] = df_FCFE.loc["ROC_HDKD", (cols_df_FCFE-1)] * (1+tmp_ROC)
	        if change_ROE:
	            tmp_ROE = ((Stable_ROE/Initial_ROE)**(1/first_stages_n_year))-1
	            #print(tmp_ROE)
	            #print(df_FCFE.loc["ROE_HDKD", cols_df_FCFE])
	            df_FCFE.loc["ROE_HDKD", cols_df_FCFE] = df_FCFE.loc["ROE_HDKD", (cols_df_FCFE-1)] * (1+tmp_ROE)
	            #print(cols_df_FCFE, df_FCFE.loc["ROE_HDKD", (cols_df_FCFE-1)] * (1+tmp_ROE))

	        tmp_EBIT_HDKD_AT = df_FCFE.loc["EBIT_HDKD_AT", cols_df_FCFE-1]
	        df_FCFE.loc["EBIT_HDKD_AT", cols_df_FCFE] = tmp_EBIT_HDKD_AT*(1+df_FCFE.loc["Expected growth rate EBIT_AT", cols_df_FCFE])

	        tmp_NI = df_FCFE.loc["Net Income", cols_df_FCFE-1]
	        df_FCFE.loc["Net Income", cols_df_FCFE] = tmp_NI*(1+df_FCFE.loc["Expected growth rate NI", cols_df_FCFE])

	        if change_WACC:
	            tmp_WACC = ((Stable_WACC/Initial_WACC)**(1/first_stages_n_year))-1
	            df_FCFE.loc["WACC", cols_df_FCFE] = df_FCFE.loc["WACC", (cols_df_FCFE-1)] * (1 + tmp_WACC)
	        else:
	            df_FCFE.loc["WACC", cols_df_FCFE] = df_FCFE.loc["WACC", (cols_df_FCFE-1)]

	        if change_Ke:
	            tmp_Ke = ((Stable_Chi_phi_von_co_phan/Initial_Chi_phi_von_co_phan)**(1/first_stages_n_year))-1
	            df_FCFE.loc["Ke", cols_df_FCFE] = df_FCFE.loc["Ke", (cols_df_FCFE-1)] * (1 + tmp_Ke)
	        else:
	            df_FCFE.loc["Ke", cols_df_FCFE] = df_FCFE.loc["Ke", (cols_df_FCFE-1)]

	df_FCFE.loc["ROE_HDKD","Terminal Year"] = Stable_ROE
	df_FCFE.loc["ROC_HDKD","Terminal Year"] = Stable_ROC
	df_FCFE.loc["EQ_Reinvestment rate","Terminal Year"] = Stable_Ty_le_Tai_dau_tu_VCP
	df_FCFE.loc["Reinvestment rate","Terminal Year"] = Stable_Ty_le_Tai_dau_tu
	df_FCFE.loc["Expected growth rate NI","Terminal Year"] = Stable_g
	df_FCFE.loc["Expected growth rate EBIT_AT","Terminal Year"] = Stable_g

	#if change_expected_growth_rate or change_ROE:
	df_FCFE.loc["EQ_Reinvestment rate"] = df_FCFE.loc["Expected growth rate NI"]/df_FCFE.loc["ROE_HDKD"]
	df_FCFE.loc["Reinvestment rate"] = df_FCFE.loc["Expected growth rate EBIT_AT"]/df_FCFE.loc["ROC_HDKD"]

	df_FCFE.loc["Net Income","Terminal Year"] = df_FCFE.loc["Net Income", cols_df_FCFE] * (1 + df_FCFE.loc["Expected growth rate NI", "Terminal Year"])
	df_FCFE.loc["EBIT_HDKD_AT","Terminal Year"] = df_FCFE.loc["EBIT_HDKD_AT", cols_df_FCFE] * (1 + df_FCFE.loc["Expected growth rate EBIT_AT", "Terminal Year"])

	df_FCFE.loc["EQ_Reinvestment"] = df_FCFE.loc["Net Income"] * df_FCFE.loc["EQ_Reinvestment rate"]
	df_FCFE.loc["Reinvestment"] = df_FCFE.loc["EBIT_HDKD_AT"] * df_FCFE.loc["Reinvestment rate"]

	df_FCFE.loc["FCFE"] = df_FCFE.loc["Net Income"] * (1 - df_FCFE.loc["EQ_Reinvestment rate"])
	df_FCFE.loc["FCFF"] = df_FCFE.loc["EBIT_HDKD_AT"] * (1 - df_FCFE.loc["Reinvestment rate"])

	df_FCFE.loc["Ke","Terminal Year"] = Stable_Chi_phi_von_co_phan
	df_FCFE.loc["WACC","Terminal Year"] = Stable_WACC

	df_FCFE.loc["Terminal Value of Equity", cols_df_FCFE] = df_FCFE.loc["FCFE", "Terminal Year"]/(df_FCFE.loc["Ke", "Terminal Year"] - df_FCFE.loc["Expected growth rate NI", "Terminal Year"])
	df_FCFE.loc["Terminal Value of Firms", cols_df_FCFE] = df_FCFE.loc["FCFF", "Terminal Year"]/(df_FCFE.loc["WACC", "Terminal Year"] - df_FCFE.loc["Expected growth rate EBIT_AT", "Terminal Year"])

	tmp_Ke = (1 + df_FCFE.loc["Ke"][:-1])**df_FCFE.columns[:-1]
	tmp_WACC = (1 + df_FCFE.loc["WACC"][:-1])**df_FCFE.columns[:-1]

	df_FCFE.fillna(0, inplace=True)
	df_FCFE.loc["Present Value FCFE", :-1] = (df_FCFE.loc["FCFE"][:-1] + df_FCFE.loc["Terminal Value of Equity"][:-1])/(tmp_Ke)
	df_FCFE.loc["Present Value FCFF", :-1] = (df_FCFE.loc["FCFF"][:-1] + df_FCFE.loc["Terminal Value of Firms"][:-1])/(tmp_WACC)

	FCFE_value = (df_FCFE.loc["Present Value FCFE"][:-1].sum() + Cash_Investment)/Shares_Outstand
	FCFF_value = (df_FCFE.loc["Present Value FCFF"][:-1].sum() + Cash_Investment - Tong_no_vay)/Shares_Outstand


	df_2_stages = df_FCFE
	df_2_stages.fillna(0, inplace=True)
	df_2_stages.reset_index(inplace=True)
	#n_row_df_2_stages_input = len(df_2_stages.columns)

	df_2_stages_styler = df_2_stages.style.format("{:>.2%}", subset = pd.IndexSlice[0:7, list(df_2_stages.columns)[1:]])\
	                                        .format("{:>8,.0f}", subset = pd.IndexSlice[8:, list(df_2_stages.columns)[1:]])\
	                                        .set_table_styles(styles)\
	                                        .applymap(color_index, subset = ["index"]).hide_index()\
	                                        .set_table_attributes('class= "table table-hover"')
	html_df_input = []

	mid_cols_df_2 = int(len(df_2_stages.columns)/2) + 1

	df_2_stages_first_range = list(df_2_stages.columns[1:mid_cols_df_2])
	df_2_stages_second_range = list(df_2_stages.columns[mid_cols_df_2:])

	#styler_df_2_export = df_2_stages_styler.export()

	first_html_df_2_stages = "".join(df_2_stages_styler.hide_columns(df_2_stages_second_range).render().split("\n"))
	html_df_input.append(first_html_df_2_stages)
	second_html_df_2_stages = "".join(df_2_stages_styler.hide_columns(df_2_stages_first_range).render().split("\n"))
	html_df_input.append(second_html_df_2_stages)

	return FCFE_value, FCFF_value, html_df_input

def valuate_3_stages(data):
	Initial_ROE = data["Initial_ROE"]/100
	Initial_NI = data["Initial_NI"]
	Initial_Chi_tieu_von_dau_tu = data["Initial_Chi_tieu_von_dau_tu"]
	Initial_KH = data["Initial_KH"]
	Initial_Thay_doi_von_luu_dong = data["Initial_Thay_doi_von_luu_dong"]
	Initial_No_phat_hanh_thuan = data["Initial_No_phat_hanh_thuan"]

	Initial_Tai_dau_tu = (Initial_Chi_tieu_von_dau_tu - Initial_KH) + Initial_Thay_doi_von_luu_dong
	Initial_FCFE = Initial_NI - Initial_Tai_dau_tu + Initial_No_phat_hanh_thuan
	Initial_Ty_le_Tai_dau_tu_VCP = 1 - Initial_FCFE/Initial_NI
	Initial_Ty_le_no_tren_tai_dau_tu = Initial_No_phat_hanh_thuan/Initial_Tai_dau_tu
	first_g = Initial_ROE * Initial_Ty_le_Tai_dau_tu_VCP

	Initial_ROC = data["Initial_ROC"]/100
	Initial_EBIT_HDKD_AT = data["Initial_EBIT_HDKD_AT"]
	Initial_FCFF = Initial_EBIT_HDKD_AT - Initial_Tai_dau_tu
	Initial_Ty_le_Tai_dau_tu = Initial_Tai_dau_tu/Initial_EBIT_HDKD_AT
	first_g_FCFF = Initial_ROC * Initial_Ty_le_Tai_dau_tu

	Stable_g = data["Stable_g"]/100
	Stable_ROE = data["Stable_ROE"]/100
	Stable_ROC = data["Stable_ROC"]/100
	Stable_Ty_le_Tai_dau_tu_VCP = Stable_g/Stable_ROE
	Stable_Ty_le_Tai_dau_tu = Stable_g/Stable_ROC

	Tax = data["Tax"]/100
	Initial_Ty_le_no_vay = Initial_Ty_le_no_tren_tai_dau_tu
	Initial_Ty_le_VCP = 1 - Initial_Ty_le_no_vay
	Lai_suat_vay = data["Lai_suat_vay"]/100
	Beta = data["Beta"]
	Lai_suat_phi_rui_ro = data["Lai_suat_phi_rui_ro"]/100
	Phan_bu_rui_ro = data["Phan_bu_rui_ro"]/100
	Initial_Chi_phi_von_co_phan = Lai_suat_phi_rui_ro + Beta*Phan_bu_rui_ro
	#print(Initial_Chi_phi_von_co_phan)
	Initial_WACC = Lai_suat_vay * (1-Tax) * Initial_Ty_le_no_vay + Initial_Chi_phi_von_co_phan * Initial_Ty_le_VCP


	Stable_Ty_le_no_vay = Initial_Ty_le_no_vay
	Stable_Ty_le_VCP = 1 - Stable_Ty_le_no_vay

	Stable_Chi_phi_von_co_phan = Lai_suat_phi_rui_ro + 1*Phan_bu_rui_ro
	Stable_WACC = Lai_suat_vay * (1-Tax) * Stable_Ty_le_no_vay + Stable_Chi_phi_von_co_phan * Stable_Ty_le_VCP
	########################################################################################################################################33
	change_Ke = True
	change_WACC = True

	Shares_Outstand = data["Shares_Outstand"]*1000000
	Tong_no_vay = data["Tong_no_vay"]
	Cash_Investment = data["Cash_Investment"]

	first_stages_n_year =data["first_stages_n_year"]
	second_stages_n_year = data["second_stages_n_year"]

	first_stages_change_expected_growth_rate_NI = True if data["first_stages_change_expected_growth_rate_NI"] == "1" else False
	first_stages_change_expected_growth_rate_EBIT_AT = True if data["first_stages_change_expected_growth_rate_EBIT_AT"] == "1" else False
	first_stages_change_ROE = True if data["first_stages_change_ROE"] == "1" else False
	first_stages_change_ROC = True if data["first_stages_change_ROC"] == "1" else False

	second_stages_change_expected_growth_rate_NI = True if data["second_stages_change_expected_growth_rate_NI"] == "1" else False
	second_stages_change_expected_growth_rate_EBIT_AT = True if data["second_stages_change_expected_growth_rate_EBIT_AT"] == "1" else False
	second_stages_change_ROE = True if data["second_stages_change_ROE"] == "1" else False
	second_stages_change_ROC = True if data["second_stages_change_ROC"] == "1" else False
	#second_stages_change_Ke = True

	second_stages_g_NI = data["second_stages_g_NI"]/100
	second_stages_ROE = data["second_stages_ROE"]/100
	second_stages_g_EBIT_AT = data["second_stages_g_EBIT_AT"]/100
	second_stages_ROC = data["second_stages_ROC"]/100

	df_FCFE = pd.DataFrame(columns=[i+1 for i in range(first_stages_n_year + second_stages_n_year)])
	df_FCFE["Terminal Year"] = None

	for cols_df_FCFE in df_FCFE.columns[:-1]:
	    #print("cols_df_FCFE: ", cols_df_FCFE)
	    df_FCFE.loc["ROE_HDKD", cols_df_FCFE] = Initial_ROE
	    df_FCFE.loc["ROC_HDKD", cols_df_FCFE] = Initial_ROC
	    df_FCFE.loc["EQ_Reinvestment rate", cols_df_FCFE] = Initial_Ty_le_Tai_dau_tu_VCP
	    df_FCFE.loc["Reinvestment rate", cols_df_FCFE] = Initial_Ty_le_Tai_dau_tu
	    df_FCFE.loc["Expected growth rate NI", cols_df_FCFE] = first_g
	    df_FCFE.loc["Expected growth rate EBIT_AT", cols_df_FCFE] = first_g_FCFF

	    if cols_df_FCFE == 1:
	        df_FCFE.loc["Ke", cols_df_FCFE] = Initial_Chi_phi_von_co_phan
	        df_FCFE.loc["WACC", cols_df_FCFE] = Initial_WACC
	        df_FCFE.loc["Net Income", cols_df_FCFE] = Initial_NI*(1+df_FCFE.loc["Expected growth rate NI", cols_df_FCFE])
	        df_FCFE.loc["EBIT_HDKD_AT", cols_df_FCFE] = Initial_EBIT_HDKD_AT*(1+df_FCFE.loc["Expected growth rate EBIT_AT", cols_df_FCFE])
	    else:
	        #Tính tốc độ thay đổi của tốc độ tăng trưởng nếu đặt ra giả thiết này
	        if (cols_df_FCFE <= first_stages_n_year):
	            if first_stages_change_expected_growth_rate_NI:
	                tmp_g_NI = ((second_stages_g_NI/first_g)**(1/first_stages_n_year))-1
	                #print("first_tmp_g_NI =========================> : ",tmp_g_NI)
	                df_FCFE.loc["Expected growth rate NI", cols_df_FCFE] = df_FCFE.loc["Expected growth rate NI", (cols_df_FCFE-1)] * (1 + tmp_g_NI)
	            if first_stages_change_expected_growth_rate_EBIT_AT:
	                tmp_g_EBIT = ((second_stages_g_EBIT_AT/first_g_FCFF)**(1/first_stages_n_year))-1
	                df_FCFE.loc["Expected growth rate EBIT_AT", cols_df_FCFE] = df_FCFE.loc["Expected growth rate EBIT_AT", (cols_df_FCFE-1)] * (1 + tmp_g_EBIT)

	            if first_stages_change_ROE:
	                tmp_ROE = ((second_stages_ROE/Initial_ROE)**(1/first_stages_n_year))-1
	                #print("first_tmp_ROE =========================> : ",tmp_ROE)
	                #print(df_FCFE.loc["ROE_HDKD", cols_df_FCFE])
	                df_FCFE.loc["ROE_HDKD", cols_df_FCFE] = df_FCFE.loc["ROE_HDKD", (cols_df_FCFE-1)] * (1+tmp_ROE)
	                #print(cols_df_FCFE,"  ", df_FCFE.loc["ROE_HDKD", cols_df_FCFE])
	                #print(cols_df_FCFE, df_FCFE.loc["ROE_HDKD", (cols_df_FCFE-1)] * (1+tmp_ROE))
	            if first_stages_change_ROC:
	                tmp_ROC = ((second_stages_ROC/Initial_ROC)**(1/first_stages_n_year))-1
	                df_FCFE.loc["ROC_HDKD", cols_df_FCFE] = df_FCFE.loc["ROC_HDKD", (cols_df_FCFE-1)] * (1+tmp_ROC)

	        if (cols_df_FCFE == (first_stages_n_year + 1)):
	            df_FCFE.loc["Expected growth rate NI", cols_df_FCFE] = second_stages_g_NI
	            df_FCFE.loc["ROE_HDKD", cols_df_FCFE] = second_stages_ROE
	            #print("second_stages_ROE: ", second_stages_ROE, "  " , cols_df_FCFE)
	            tmp_g_NI = ((Stable_g/second_stages_g_NI)**(1/second_stages_n_year))-1
	            #print("second_tmp_g_NI =========================> : ",tmp_g_NI)
	            tmp_ROE = ((Stable_ROE/second_stages_ROE)**(1/second_stages_n_year))-1
	            #print("second_tmp_ROE =========================> : ",tmp_ROE)

	            df_FCFE.loc["Expected growth rate EBIT_AT", cols_df_FCFE] = second_stages_g_EBIT_AT
	            df_FCFE.loc["ROC_HDKD", cols_df_FCFE] = second_stages_ROC
	            tmp_g_EBIT = ((Stable_g/second_stages_g_EBIT_AT)**(1/second_stages_n_year))-1
	            tmp_ROC = ((Stable_ROC/second_stages_ROC)**(1/second_stages_n_year))-1


	        if (cols_df_FCFE > (first_stages_n_year + 1)):
	            if second_stages_change_expected_growth_rate_NI:
	                df_FCFE.loc["Expected growth rate NI", cols_df_FCFE] = df_FCFE.loc["Expected growth rate NI", (cols_df_FCFE-1)] * (1 + tmp_g_NI)
	            else:
	                df_FCFE.loc["Expected growth rate NI", cols_df_FCFE] = df_FCFE.loc["Expected growth rate NI", (cols_df_FCFE-1)]

	            if second_stages_change_expected_growth_rate_EBIT_AT:
	                df_FCFE.loc["Expected growth rate EBIT_AT", cols_df_FCFE] = df_FCFE.loc["Expected growth rate EBIT_AT", (cols_df_FCFE-1)] * (1 + tmp_g_EBIT)
	            else:
	                df_FCFE.loc["Expected growth rate EBIT_AT", cols_df_FCFE] = df_FCFE.loc["Expected growth rate EBIT_AT", (cols_df_FCFE-1)]

	            if second_stages_change_ROE:
	                df_FCFE.loc["ROE_HDKD", cols_df_FCFE] = df_FCFE.loc["ROE_HDKD", (cols_df_FCFE-1)] * (1+tmp_ROE)
	            else:
	                df_FCFE.loc["ROE_HDKD", cols_df_FCFE] = df_FCFE.loc["ROE_HDKD", (cols_df_FCFE-1)]

	            if second_stages_change_ROC:
	                df_FCFE.loc["ROC_HDKD", cols_df_FCFE] = df_FCFE.loc["ROC_HDKD", (cols_df_FCFE-1)] * (1+tmp_ROC)
	            else:
	                df_FCFE.loc["ROC_HDKD", cols_df_FCFE] = df_FCFE.loc["ROC_HDKD", (cols_df_FCFE-1)]

	        tmp_EBIT_HDKD_AT = df_FCFE.loc["EBIT_HDKD_AT", cols_df_FCFE-1]
	        df_FCFE.loc["EBIT_HDKD_AT", cols_df_FCFE] = tmp_EBIT_HDKD_AT*(1+df_FCFE.loc["Expected growth rate EBIT_AT", cols_df_FCFE])

	        tmp_NI = df_FCFE.loc["Net Income", cols_df_FCFE-1]
	        df_FCFE.loc["Net Income", cols_df_FCFE] = tmp_NI*(1+df_FCFE.loc["Expected growth rate NI", cols_df_FCFE])

	        if change_Ke:
	            tmp_Ke = ((Stable_Chi_phi_von_co_phan/Initial_Chi_phi_von_co_phan)**(1/(first_stages_n_year+second_stages_n_year)))-1
	            df_FCFE.loc["Ke", cols_df_FCFE] = df_FCFE.loc["Ke", (cols_df_FCFE-1)] * (1 + tmp_Ke)
	        else:
	            df_FCFE.loc["Ke", cols_df_FCFE] = df_FCFE.loc["Ke", (cols_df_FCFE-1)]

	        if change_WACC:
	            tmp_WACC= ((Stable_WACC/Initial_WACC)**(1/(first_stages_n_year+second_stages_n_year)))-1
	            df_FCFE.loc["WACC", cols_df_FCFE] = df_FCFE.loc["WACC", (cols_df_FCFE-1)] * (1 + tmp_WACC)
	        else:
	            df_FCFE.loc["WACC", cols_df_FCFE] = df_FCFE.loc["WACC", (cols_df_FCFE-1)]

	df_FCFE.loc["ROE_HDKD","Terminal Year"] = Stable_ROE
	df_FCFE.loc["ROC_HDKD","Terminal Year"] = Stable_ROC

	df_FCFE.loc["EQ_Reinvestment rate","Terminal Year"] = Stable_Ty_le_Tai_dau_tu_VCP
	df_FCFE.loc["Reinvestment rate","Terminal Year"] = Stable_Ty_le_Tai_dau_tu

	df_FCFE.loc["Expected growth rate NI","Terminal Year"] = Stable_g
	df_FCFE.loc["Expected growth rate EBIT_AT","Terminal Year"] = Stable_g

	#if change_expected_growth_rate or change_ROE:
	df_FCFE.loc["EQ_Reinvestment rate"] = df_FCFE.loc["Expected growth rate NI"]/df_FCFE.loc["ROE_HDKD"]
	df_FCFE.loc["Reinvestment rate"] = df_FCFE.loc["Expected growth rate EBIT_AT"]/df_FCFE.loc["ROC_HDKD"]

	df_FCFE.loc["Net Income","Terminal Year"] = df_FCFE.loc["Net Income", cols_df_FCFE] * (1 + df_FCFE.loc["Expected growth rate NI", "Terminal Year"])
	df_FCFE.loc["EBIT_HDKD_AT","Terminal Year"] = df_FCFE.loc["EBIT_HDKD_AT", cols_df_FCFE] * (1 + df_FCFE.loc["Expected growth rate EBIT_AT", "Terminal Year"])

	df_FCFE.loc["EQ_Reinvestment"] = df_FCFE.loc["Net Income"] * df_FCFE.loc["EQ_Reinvestment rate"]
	df_FCFE.loc["Reinvestment"] = df_FCFE.loc["EBIT_HDKD_AT"] * df_FCFE.loc["Reinvestment rate"]

	df_FCFE.loc["FCFE"] = df_FCFE.loc["Net Income"] * (1 - df_FCFE.loc["EQ_Reinvestment rate"])
	df_FCFE.loc["FCFF"] = df_FCFE.loc["EBIT_HDKD_AT"] * (1 - df_FCFE.loc["Reinvestment rate"])

	df_FCFE.loc["Ke","Terminal Year"] = Stable_Chi_phi_von_co_phan
	df_FCFE.loc["WACC","Terminal Year"] = Stable_WACC

	df_FCFE.loc["Terminal Value of Equity", cols_df_FCFE] = df_FCFE.loc["FCFE", "Terminal Year"]/(df_FCFE.loc["Ke", "Terminal Year"] - df_FCFE.loc["Expected growth rate NI", "Terminal Year"])
	df_FCFE.loc["Terminal Value of Firms", cols_df_FCFE] = df_FCFE.loc["FCFF", "Terminal Year"]/(df_FCFE.loc["WACC", "Terminal Year"] - df_FCFE.loc["Expected growth rate EBIT_AT", "Terminal Year"])

	tmp_Ke = (1 + df_FCFE.loc["Ke"][:-1])**df_FCFE.columns[:-1]
	tmp_WACC = (1 + df_FCFE.loc["WACC"][:-1])**df_FCFE.columns[:-1]

	df_FCFE.fillna(0, inplace=True)
	df_FCFE.loc["Present Value FCFE", :-1] = (df_FCFE.loc["FCFE"][:-1] + df_FCFE.loc["Terminal Value of Equity"][:-1])/(tmp_Ke)
	df_FCFE.loc["Present Value FCFF", :-1] = (df_FCFE.loc["FCFF"][:-1] + df_FCFE.loc["Terminal Value of Firms"][:-1])/(tmp_WACC)

	FCFE_value = (df_FCFE.loc["Present Value FCFE"][:-1].sum() + Cash_Investment)/Shares_Outstand
	FCFF_value = (df_FCFE.loc["Present Value FCFF"][:-1].sum() + Cash_Investment - Tong_no_vay)/Shares_Outstand

	#print(df_FCFE.loc["ROE_HDKD"])


	df_3_stages = df_FCFE
	df_3_stages.fillna(0, inplace=True)
	df_3_stages.reset_index(inplace=True)
	df_3_stages_styler = df_3_stages.style.format("{:>.2%}", subset = pd.IndexSlice[0:7, list(df_3_stages.columns)[1:]])                                        .format("{:>8,.0f}", subset = pd.IndexSlice[8:, list(df_3_stages.columns)[1:]])                                        .set_table_styles(styles)                                        .applymap(color_index, subset = ["index"]).hide_index()                                        .set_table_attributes('class= "table table-hover"')

	html_df_input = []
	#thay doi so slice columns cho lih dong
	mid_cols_df_3 = int(len(df_3_stages.columns)/2) + 1
	df_3_stages_first_range = list(df_3_stages.columns[1:mid_cols_df_3])
	df_3_stages_second_range = list(df_3_stages.columns[mid_cols_df_3:])

	#styler_df_2_export = df_2_stages_styler.export()

	first_html_df_3_stages = "".join(df_3_stages_styler.hide_columns(df_3_stages_second_range).render().split("\n"))
	html_df_input.append(first_html_df_3_stages)

	second_html_df_3_stages = "".join(df_3_stages_styler.hide_columns(df_3_stages_first_range).render().split("\n"))
	html_df_input.append(second_html_df_3_stages)
	#print(FCFE_value, " || ", FCFF_value)

	return FCFE_value, FCFF_value, html_df_input

def valuate_n_stages(data):
	Initial_ROE = data["Initial_ROE"]/100
	Initial_NI = data["Initial_NI"]
	Initial_Chi_tieu_von_dau_tu = data["Initial_Chi_tieu_von_dau_tu"]
	Initial_KH = data["Initial_KH"]
	Initial_Thay_doi_von_luu_dong = data["Initial_Thay_doi_von_luu_dong"]
	Initial_No_phat_hanh_thuan = data["Initial_No_phat_hanh_thuan"]

	Initial_Tai_dau_tu = (Initial_Chi_tieu_von_dau_tu - Initial_KH) + Initial_Thay_doi_von_luu_dong
	Initial_FCFE = Initial_NI - Initial_Tai_dau_tu + Initial_No_phat_hanh_thuan
	Initial_Ty_le_Tai_dau_tu_VCP = 1 - Initial_FCFE/Initial_NI
	Initial_Ty_le_no_tren_tai_dau_tu = Initial_No_phat_hanh_thuan/Initial_Tai_dau_tu
	first_g = Initial_ROE * Initial_Ty_le_Tai_dau_tu_VCP

	Initial_ROC = data["Initial_ROC"]/100
	Initial_EBIT_HDKD_AT = data["Initial_EBIT_HDKD_AT"]
	Initial_FCFF = Initial_EBIT_HDKD_AT - Initial_Tai_dau_tu
	Initial_Ty_le_Tai_dau_tu = Initial_Tai_dau_tu/Initial_EBIT_HDKD_AT
	first_g_FCFF = Initial_ROC * Initial_Ty_le_Tai_dau_tu

	Stable_g = data["Stable_g"]/100
	Stable_ROE = data["Stable_ROE"]/100
	Stable_ROC = data["Stable_ROC"]/100
	Stable_Ty_le_Tai_dau_tu_VCP = Stable_g/Stable_ROE
	Stable_Ty_le_Tai_dau_tu = Stable_g/Stable_ROC

	Tax = data["Tax"]/100
	Initial_Ty_le_no_vay = Initial_Ty_le_no_tren_tai_dau_tu
	Initial_Ty_le_VCP = 1 - Initial_Ty_le_no_vay
	Lai_suat_vay = data["Lai_suat_vay"]/100
	Beta = data["Beta"]
	Lai_suat_phi_rui_ro = data["Lai_suat_phi_rui_ro"]/100
	Phan_bu_rui_ro = data["Phan_bu_rui_ro"]/100
	Initial_Chi_phi_von_co_phan = Lai_suat_phi_rui_ro + Beta*Phan_bu_rui_ro
	#print(Initial_Chi_phi_von_co_phan)
	Initial_WACC = Lai_suat_vay * (1-Tax) * Initial_Ty_le_no_vay + Initial_Chi_phi_von_co_phan * Initial_Ty_le_VCP


	Stable_Ty_le_no_vay = Initial_Ty_le_no_vay
	Stable_Ty_le_VCP = 1 - Stable_Ty_le_no_vay

	Stable_Chi_phi_von_co_phan = Lai_suat_phi_rui_ro + 1*Phan_bu_rui_ro
	Stable_WACC = Lai_suat_vay * (1-Tax) * Stable_Ty_le_no_vay + Stable_Chi_phi_von_co_phan * Stable_Ty_le_VCP
	########################################################################################################################################
	Shares_Outstand = data["Shares_Outstand"]*1000000
	Tong_no_vay = data["Tong_no_vay"]
	Cash_Investment = data["Cash_Investment"]

	change_Ke = True if data["change_Ke_n"] == "1" else False
	change_WACC = True if data["change_WACC_n"] == "1" else False
	change_expected_growth_rate_NI = True if data["change_expected_growth_rate_NI_n"] == "1" else False
	change_expected_growth_rate_EBIT = True if data["change_expected_growth_rate_EBIT_n"] == "1" else False

	Initial_g_NI = data["Initial_g_NI"]/100
	Initial_g_EBIT_AT = data["Initial_g_EBIT_AT"]/100
	fix_n_year = data["fix_n_year"]

	df_FCFE = pd.DataFrame(columns=[i+1 for i in range(fix_n_year)])

	for cols_df_FCFE in df_FCFE.columns:
	    if cols_df_FCFE == 1:
	        if change_expected_growth_rate_NI:
	            df_FCFE.loc["Expected growth rate NI", cols_df_FCFE] = Initial_g_NI
	        else:
	            df_FCFE.loc["Expected growth rate NI", cols_df_FCFE] = Stable_g
	        if change_expected_growth_rate_EBIT:
	            df_FCFE.loc["Expected growth rate EBIT_AT", cols_df_FCFE] = Initial_g_EBIT_AT
	        else:
	            df_FCFE.loc["Expected growth rate EBIT_AT", cols_df_FCFE] = Stable_g

	        if change_Ke:
	            df_FCFE.loc["Ke", cols_df_FCFE] = Initial_Chi_phi_von_co_phan
	        else:
	            df_FCFE.loc["Ke", cols_df_FCFE] = Stable_Chi_phi_von_co_phan

	        if change_WACC:
	            df_FCFE.loc["WACC", cols_df_FCFE] = Initial_WACC
	        else:
	            df_FCFE.loc["WACC", cols_df_FCFE] = Stable_WACC

	        df_FCFE.loc["FCFE", cols_df_FCFE] = Initial_FCFE*(1 + df_FCFE.loc["Expected growth rate NI", cols_df_FCFE])
	        df_FCFE.loc["FCFF", cols_df_FCFE] = Initial_FCFF*(1 + df_FCFE.loc["Expected growth rate EBIT_AT", cols_df_FCFE])

	    else:
	        if change_expected_growth_rate_NI:
	            tmp_g_NI = ((Stable_g/Initial_g_NI)**(1/(fix_n_year - 1)))-1
	            df_FCFE.loc["Expected growth rate NI", cols_df_FCFE] = df_FCFE.loc["Expected growth rate NI", (cols_df_FCFE-1)] * (1+tmp_g_NI)
	        else:
	            df_FCFE.loc["Expected growth rate NI", cols_df_FCFE] = df_FCFE.loc["Expected growth rate NI", (cols_df_FCFE-1)]

	        if change_expected_growth_rate_EBIT:
	            tmp_g_EBIT = ((Stable_g/Initial_g_EBIT_AT)**(1/(fix_n_year - 1)))-1
	            df_FCFE.loc["Expected growth rate EBIT_AT", cols_df_FCFE] = df_FCFE.loc["Expected growth rate EBIT_AT", (cols_df_FCFE-1)] * (1+tmp_g_EBIT)
	        else:
	            df_FCFE.loc["Expected growth rate EBIT_AT", cols_df_FCFE] = df_FCFE.loc["Expected growth rate EBIT_AT", (cols_df_FCFE-1)]

	        if change_WACC:
	            tmp_WACC = ((Stable_WACC/Initial_WACC)**(1/(fix_n_year - 1)))-1
	            df_FCFE.loc["WACC", cols_df_FCFE] = df_FCFE.loc["WACC", (cols_df_FCFE-1)] * (1+tmp_WACC)
	        else:
	            df_FCFE.loc["WACC", cols_df_FCFE] = df_FCFE.loc["WACC", (cols_df_FCFE-1)]

	        if change_Ke:
	            tmp_Ke = ((Stable_Chi_phi_von_co_phan/Initial_Chi_phi_von_co_phan)**(1/(fix_n_year - 1)))-1
	            #print(tmp_Ke)
	            df_FCFE.loc["Ke", cols_df_FCFE] = df_FCFE.loc["Ke", (cols_df_FCFE-1)] * (1+tmp_Ke)
	        else:
	            df_FCFE.loc["Ke", cols_df_FCFE] = df_FCFE.loc["Ke", (cols_df_FCFE-1)]

	        df_FCFE.loc["FCFE", cols_df_FCFE] = df_FCFE.loc["FCFE", (cols_df_FCFE - 1)] * (1 + df_FCFE.loc["Expected growth rate NI", cols_df_FCFE])
	        df_FCFE.loc["FCFF", cols_df_FCFE] = df_FCFE.loc["FCFF", (cols_df_FCFE - 1)] * (1 + df_FCFE.loc["Expected growth rate EBIT_AT", cols_df_FCFE])
	tmp_Ke = (1 + df_FCFE.loc["Ke"])**df_FCFE.columns
	tmp_WACC = (1 + df_FCFE.loc["WACC"])**df_FCFE.columns
	#print(tmp_Ke)
	df_FCFE.loc["Present Value FCFE"] = (df_FCFE.loc["FCFE"])/tmp_Ke
	df_FCFE.loc["Present Value FCFF"] = (df_FCFE.loc["FCFF"])/tmp_WACC

	FCFE_value = (df_FCFE.loc["Present Value FCFE"].sum() + Cash_Investment)/Shares_Outstand
	FCFF_value = (df_FCFE.loc["Present Value FCFF"].sum() + Cash_Investment - Tong_no_vay)/Shares_Outstand

	df_1_stages = df_FCFE
	df_1_stages.fillna(0, inplace=True)
	df_1_stages.reset_index(inplace=True)
	df_1_stages_styler = df_1_stages.style.format("{:>.2%}", subset = pd.IndexSlice[0:3, list(df_1_stages.columns)[1:]])\
	                                        .format("{:>8,.0f}", subset = pd.IndexSlice[4:, list(df_1_stages.columns)[1:]])\
	                                        .set_table_styles(styles)\
	                                        .applymap(color_index, subset = ["index"]).hide_index()\
	                                        .set_table_attributes('class= "table table-hover table-responsive"')

	html_df_input = []
	#thay doi so slice columns cho lih dong
	mid_cols_df_1 = int(len(df_1_stages.columns)/2) + 1

	df_1_stages_first_range = list(df_1_stages.columns[1:mid_cols_df_1])
	df_1_stages_second_range = list(df_1_stages.columns[mid_cols_df_1:])

	first_html_df_1_stages = "".join(df_1_stages_styler.hide_columns(df_1_stages_second_range).render().split("\n"))
	html_df_input.append(first_html_df_1_stages)

	second_html_df_1_stages = "".join(df_1_stages_styler.hide_columns(df_1_stages_first_range).render().split("\n"))
	html_df_input.append(second_html_df_1_stages)

	return FCFE_value, FCFF_value, html_df_input

def valuate_stable(data):
	Initial_ROE = data["Initial_ROE"]/100
	Initial_NI = data["Initial_NI"]
	Initial_Chi_tieu_von_dau_tu = data["Initial_Chi_tieu_von_dau_tu"]
	Initial_KH = data["Initial_KH"]
	Initial_Thay_doi_von_luu_dong = data["Initial_Thay_doi_von_luu_dong"]
	Initial_No_phat_hanh_thuan = data["Initial_No_phat_hanh_thuan"]

	Initial_Tai_dau_tu = (Initial_Chi_tieu_von_dau_tu - Initial_KH) + Initial_Thay_doi_von_luu_dong
	Initial_FCFE = Initial_NI - Initial_Tai_dau_tu + Initial_No_phat_hanh_thuan
	Initial_Ty_le_Tai_dau_tu_VCP = 1 - Initial_FCFE/Initial_NI
	Initial_Ty_le_no_tren_tai_dau_tu = Initial_No_phat_hanh_thuan/Initial_Tai_dau_tu
	first_g = Initial_ROE * Initial_Ty_le_Tai_dau_tu_VCP

	Initial_ROC = data["Initial_ROC"]/100
	Initial_EBIT_HDKD_AT = data["Initial_EBIT_HDKD_AT"]
	Initial_FCFF = Initial_EBIT_HDKD_AT - Initial_Tai_dau_tu
	Initial_Ty_le_Tai_dau_tu = Initial_Tai_dau_tu/Initial_EBIT_HDKD_AT
	first_g_FCFF = Initial_ROC * Initial_Ty_le_Tai_dau_tu

	Stable_g = data["Stable_g"]/100
	Stable_ROE = data["Stable_ROE"]/100
	Stable_ROC = data["Stable_ROC"]/100
	Stable_Ty_le_Tai_dau_tu_VCP = Stable_g/Stable_ROE
	Stable_Ty_le_Tai_dau_tu = Stable_g/Stable_ROC

	Tax = data["Tax"]/100
	Initial_Ty_le_no_vay = Initial_Ty_le_no_tren_tai_dau_tu
	Initial_Ty_le_VCP = 1 - Initial_Ty_le_no_vay
	Lai_suat_vay = data["Lai_suat_vay"]/100
	Beta = data["Beta"]
	Lai_suat_phi_rui_ro = data["Lai_suat_phi_rui_ro"]/100
	Phan_bu_rui_ro = data["Phan_bu_rui_ro"]/100
	Initial_Chi_phi_von_co_phan = Lai_suat_phi_rui_ro + Beta*Phan_bu_rui_ro
	#print(Initial_Chi_phi_von_co_phan)
	Initial_WACC = Lai_suat_vay * (1-Tax) * Initial_Ty_le_no_vay + Initial_Chi_phi_von_co_phan * Initial_Ty_le_VCP


	Stable_Ty_le_no_vay = Initial_Ty_le_no_vay
	Stable_Ty_le_VCP = 1 - Stable_Ty_le_no_vay

	Stable_Chi_phi_von_co_phan = Lai_suat_phi_rui_ro + 1*Phan_bu_rui_ro
	Stable_WACC = Lai_suat_vay * (1-Tax) * Stable_Ty_le_no_vay + Stable_Chi_phi_von_co_phan * Stable_Ty_le_VCP
	########################################################################################################################################
	Shares_Outstand = data["Shares_Outstand"]*1000000
	Tong_no_vay = data["Tong_no_vay"]
	Cash_Investment = data["Cash_Investment"]

	Equity_value = (Initial_FCFE*(1+Stable_g))/(Stable_Chi_phi_von_co_phan - Stable_g)
	Firms_value = (Initial_FCFF*(1+Stable_g))/(Stable_WACC - Stable_g)

	FCFE_value = (Equity_value + Cash_Investment)/Shares_Outstand
	FCFF_value = (Firms_value + Cash_Investment - Tong_no_vay)/Shares_Outstand
	return FCFE_value, FCFF_value
