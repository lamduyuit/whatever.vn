# coding: utf-8
import pandas as pd
#from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime

from bokeh.io import output_notebook, show
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.embed import components
import os
from bokeh.models import HoverTool,LinearAxis,Range1d,PanTool, ResetTool,NumeralTickFormatter,Legend,BoxAnnotation

import random
from bokeh.io import show,output_notebook
from bokeh.models import (
    LogColorMapper,
    FixedTicker
)

from bokeh.palettes import Viridis10 as palette

from home.models import *
#import pwd

def download_financial(stock_id):
	n_year = 2014
	#year_now = datetime.now().year
	year_now = 2018
	yearly_data  = report_yearly.objects.filter(stock_id=stock_id)
	if len(yearly_data)>=1 :
		# Create a Pandas Excel writer using XlsxWriter as the engine.
		path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"data/download_financial/"+stock_id+"-report.xlsx")
		if stock_id+"-report.xlsx" in os.listdir(os.path.dirname(path)):
			return path
		writer = pd.ExcelWriter(path, engine='xlsxwriter')
		# Write each dataframe to a different worksheet.
		#print(pwd.getpwuid( os.getegid() )[ 0 ])
		for y_data in yearly_data:
			if y_data.report_name == "CDKT":
				cdkt_year = change_type_df_y(y_data,n_year)
				if cdkt_year.ix[1,-1] == 0:
					cdkt_year.drop(str(year_now),axis=1, inplace= True)
				else:
					cdkt_year.rename(columns={str(year_now):"The latest quaters of "+str(year_now)},inplace=True)
				cdkt_year.to_excel(writer, sheet_name='Balance')

			if y_data.report_name == "KQKD":
				kqkd_year = change_type_df_y(y_data,n_year)
				if kqkd_year.ix[0,-1] == 0:
					kqkd_year.drop(str(year_now),axis=1, inplace= True)
				else:
					kqkd_year.rename(columns={str(year_now):"The latest 4 quaters of "+str(year_now)},inplace=True)
				kqkd_year.to_excel(writer, sheet_name='Income')

			if y_data.report_name == "LCTT":
				Lctt_year = change_type_df_y(y_data,n_year)
				Lctt_year.to_excel(writer, sheet_name='Cashflow')
			if y_data.report_name == "CSTC":
				cstc_year = change_type_df_y(y_data,n_year)
				if cstc_year.ix[2,-1] == 0:
					cstc_year.drop(str(year_now),axis=1, inplace= True)
				else:
					cstc_year.rename(columns={str(year_now):"The latest 4 quaters of "+str(year_now)},inplace=True)
				cstc_year.to_excel(writer, sheet_name='CSTC')
		# Close the Pandas Excel writer and output the Excel file.
		writer.save()
		return path
	else :
		return None


######################################################################################################################

def change_type_df_q(df,year):
	df = pd.DataFrame(df.data)
	df.reset_index(drop=True, inplace=True)
	# df.set_index("index",inplace=True)
	df.index = df.index.astype("int")
	df["Year"] = df["Year"].astype("int")
	for col in df.columns[1:6]:
		df[col] = df[col].astype("float")
	print(df[df["Year"]>=year].columns)
	return df[df["Year"]>=year]

def change_type_df_y(df,year):
	df = pd.DataFrame(df.data)
	df.reset_index(drop=True, inplace=True)
	# df.set_index("index",inplace=True)
	df.index = df.index.astype("int")
	df.sort_index(inplace= True)

	attr = df["Attribute"]
	df.drop("Attribute",inplace=True,axis=1)
	df.insert(0,"Attribute",attr)

	data = df[df.columns[1:][-(int(df.columns[-1])-year+1):]]
	#print(df.head())
	#df = df[[0]].join(data)
	df = df[df.columns[0]].to_frame().join(data)
	df.index = df.index.astype("int")
	for col in df.columns[1:]:
		df[col] = df[col].astype("float")
	return df

def get_price_from_df(df_p,cstc,num_q):
	tmp = df_p.copy()
	"""
	df_p["month"] = df_p["Date/Time"].dt.month
	df_p["month"] = df_p["month"].shift(1)
	df_p =df_p[(df_p["Date/Time"].dt.month>df_p["month"]) & (df_p["Date/Time"].dt.year.isin(cstc.columns[1:].astype("int")))]
	"""
	df_p = df_p[df_p["Date/Time"].dt.year.isin(cstc.columns[1:].astype("int"))]
	p_now = tmp.ix[0,"Close"]
	p_past = df_p["Close"].tolist()
	p_past.reverse()
	if num_q is None:
		p_past[-1] = p_now
	"""
	if num_q is not None:
		p_past.append(p_now)
	else:
		p_past[-1] = p_now
	"""
	return p_past

def change_type_df_price(df,year):
	df = pd.DataFrame(df.data)
	df.index = pd.to_datetime(df.index)
	df =  df["Close"].to_frame()
	df["Close"] = df["Close"].astype("float")
	df.reset_index(inplace=True)
	df.rename(columns={"index":"Date/Time"},inplace=True)
	df.sort_values("Date/Time",ascending=False,inplace=True)
	df.reset_index(inplace=True)
	return df



def get_chart(stock_id):
	n_year =2014
	#year_now = datetime.now().year
	year_now = 2018
	#print("dirname:",os.path.dirname(__file__))
	#print(os.path.join(os.path.dirname(__file__), 'data/Income-quaters-1.csv'))
	#kqkd_q = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data/Income-quaters-1.csv'),index_col="stock_id")

	#cdkt_q = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data/Balance-quaters-2.csv'),index_col="stock_id")

	kqkd_5_cdkt_5 = report_quaterly.objects.filter(stock_id=stock_id)
	#print(len(kqkd_5_cdkt_5), "==========================================", type(kqkd_5_cdkt_5), kqkd_5_cdkt_5.count())
	#print(dir(kqkd_5_cdkt_5),)
	if kqkd_5_cdkt_5.count() == 0:
		return None
	yearly_data  = report_yearly.objects.filter(stock_id=stock_id)
	if yearly_data.count() == 0:
		return None
	#price_data = stock_price.objects.filter(stock_id = stock_id).first()

	list_reports_name = []

	for i in kqkd_5_cdkt_5:
		#print(i.report_name, " ============>")
		#print(i.report_name, "==============================================")
		if i.report_name == "KQKD":
			list_reports_name.append(i.report_name)
			kqkd_5 = change_type_df_q(i,n_year)
			#print(kqkd_5, "=================================================================>")
		if i.report_name == "CDKT":
			list_reports_name.append(i.report_name)
			cdkt_5 = change_type_df_q(i,n_year)
	if "KQKD" not in list_reports_name or "CDKT" not in list_reports_name:
		return None

	# def as_type(df1):
	#     df = df1.copy()
	#     df["Attribute"] = df["Attribute"].astype("category")
	#     df["index"] = df["index"].astype("category")
	#     df["Year"] = df["Year"].astype("category")
	#     df.index = pd.CategoricalIndex(df.index)
	#     df.sort_index(inplace=True)

	#     df = df.ix[stock_id]
	#     df["Year"] = df["Year"].astype("int")
	#     df = df[df["Year"]>=n_year]
	#     df.set_index("index",inplace=True)
	#     df.index = df.index.astype("int")
	#     return df

	#kqkd_5 = as_type(kqkd_q)
	#cdkt_5 = as_type(cdkt_q)
	#print(kqkd_5)

	"""
	def get_ys_report(path):
	    df = pd.read_csv(path,index_col="stock_id")
	    if "Unnamed: 1" in df.columns:
	    	df.rename(columns={"Unnamed: 1":"index"},inplace=True)

	    df["Attribute"] = df["Attribute"].astype("category")
	    df["index"] = df["index"].astype("category")
	    df.index = pd.CategoricalIndex(df.index)
	    df.sort_index(inplace=True)

	    df = df.ix[stock_id]
	    df.set_index("index",inplace=True)

	    data = df[df.columns[1:][-(int(df.columns[-1])-n_year+1):]]
	    df = df[[0]].join(data)
	    df.index = df.index.astype("int")
	    return df
	"""
	list_reports = []
	for y_data in yearly_data:
		list_reports.append(y_data.report_name)
		if y_data.report_name == "CDKT":
			cdkt_year = change_type_df_y(y_data,n_year)
		if y_data.report_name == "KQKD":
			kqkd_year = change_type_df_y(y_data,n_year)
		if y_data.report_name == "LCTT":
			Lctt_year = change_type_df_y(y_data,n_year)
		if y_data.report_name == "CSTC":
			cstc_year = change_type_df_y(y_data,n_year)
	##print("++++++++++++++++++++KQKD+++++++++++++++++++++++++++++++++++++++++++++++++++",kqkd_year)
	##print("++++++++++++++++++++CDKT+++++++++++++++++++++++++++++++++++++++++++++++++++",cdkt_year)
	##print("++++++++++++++++++++CSTC+++++++++++++++++++++++++++++++++++++++++++++++++++",cstc_year)
	##################		Kiem tra co du lieu quy nam hien tai   ################################
	flag = True #Co du lieu nam hien tai
	if kqkd_year.ix[0,-1]==0 or cdkt_year.ix[1,-1]==0 or cstc_year.ix[2,-1]==0:
		kqkd_year.drop(str(year_now),axis=1, inplace= True)
		cdkt_year.drop(str(year_now),axis=1, inplace= True)
		cstc_year.drop(str(year_now),axis=1, inplace= True)
		flag = False

	##################		Kiem tra co dulieu luu chuyen tien te va 3 bao cao con lai ###############
	#Co LCTT va co du lieu nam hien tai va khong co du lieu nam hien tai:
	if "LCTT" in list_reports:
		if flag:
			Lctt_year[str(year_now)]=Lctt_year[str(year_now-1)]
		EBITDA = cstc_year.ix[90,1:]+Lctt_year.ix[3,1:]
		EBITDA["Attribute"] = "EBITDA"
		cstc_year.ix[91] = EBITDA

		Enterprise_multiple=cstc_year.ix[92,1:]/cstc_year.ix[91,1:]
		Enterprise_multiple["Attribute"] = "EV/EBITDA (Enterprise multiple)"
		cstc_year.ix[94] = Enterprise_multiple

	def get_bottom_top(df,num_cols):
	    return df[df.columns[1:(num_cols+1)]].sum(axis=1)


	def get_data_chart(data_frame,row):
	    data = data_frame.ix[row].copy()
	    for t in range(1,5):
	        data["q"+str(t)] = get_bottom_top(data_frame.ix[row],t).tolist()
	    data.sort_values("Year",inplace=True)
	    data.rename(columns={"Quý 1":"Quy1","Quý 2":"Quy2","Quý 3":"Quy3","Quý 4":"Quy4"},inplace=True)
	    return data


	def get_new_data_source(df,pre_fix):
	    iii = df.copy()
	    iii.columns = [pre_fix+ i for i in iii.columns]
	    iii = ColumnDataSource(iii)
	    return iii

	list_chart = []
	##################################################CHART1##############################################################################
	#chart1 = figure(plot_width=600, plot_height=400, title="Income")
	chart1 = figure(plot_height=500,title="Net Sales")
	upper = BoxAnnotation(top=0, fill_alpha=0.1, fill_color='olive')
	chart1.add_layout(upper)

	#PB line

	pb = cstc_year.ix[4,1:].copy()
	pb.name = "PB"
	chart1_data = get_data_chart(kqkd_5,0)
	chart1_data["PB"] = pb.tolist()
	#chart1_data = ColumnDataSource(data)
	# Setting the second y axis range name and range
	chart1.extra_y_ranges = {"foo": Range1d(start=0, end=max(get_new_data_source(chart1_data,"g1_r").data.get("g1_rPB"))+1)}
	chart1.toolbar_sticky = False
	# Adding the second axis to the plot.
	chart1.add_layout(LinearAxis(y_range_name="foo"), 'right')



	#data

	g1_r = chart1.vbar("g1_rYear",width=0.5,            top="g1_rq1",color="#04a78c",source= get_new_data_source(chart1_data,"g1_r"),hover_fill_color="#140F2E",hover_fill_alpha=0.6)
	g2_r = chart1.vbar("g2_rYear",width=0.5,bottom="g2_rq1",top="g2_rq2",color="#f4b11f",source= get_new_data_source(chart1_data,"g2_r"),hover_fill_color="firebrick",hover_fill_alpha=0.6)
	g3_r = chart1.vbar("g3_rYear",width=0.5,bottom="g3_rq2",top="g3_rq3",color="#2b3e51",source= get_new_data_source(chart1_data,"g3_r"),hover_fill_color="#8F37A4",hover_fill_alpha=0.6)
	g4_r = chart1.vbar("g4_rYear",width=0.5,bottom="g4_rq3",top="g4_rq4",color="#ff4043",source= get_new_data_source(chart1_data,"g4_r"),hover_fill_color="#4BC393",hover_fill_alpha=0.6)

	g5_r = chart1.line("g5_rYear","g5_rPB",source= get_new_data_source(chart1_data,"g5_r"),y_range_name="foo",line_dash="4 4",color="orange",hover_line_color="red")
	g6_r = chart1.diamond("g6_rYear","g6_rPB",source= get_new_data_source(chart1_data,"g6_r"),y_range_name="foo",size=12,color="#A29FDF",line_width=2,hover_fill_color="#CD8CD9")

	#hover
	hover1 = HoverTool(
	        renderers=[g1_r],
	        tooltips=[
	            ("Quý 1", "@g1_rQuy1{00,000,000.}"),
	            ("Year", "$x{int}"),
	        ]
	    )
	hover2 = HoverTool(
	        renderers=[g2_r],
	        tooltips=[
	            ("Quý 2", "@g2_rQuy2{00,000,000.}"),
	            ("Year", "$x{int}"),
	        ]
	    )
	hover3 = HoverTool(
	        renderers=[g3_r],
	        tooltips=[
	            ("Quý 3", "@g3_rQuy3{00,000,000.}"),
	            ("Year", "$x{int}"),
	        ]
	    )
	hover4 = HoverTool(
	        renderers=[g4_r],
	        tooltips=[
	            ("Quý 4", "@g4_rQuy4{00,000,000}"),
	            ("Year", "$x{int}"),
	        ]
	    )
	hover5 = HoverTool(
	        renderers=[g5_r],
	        tooltips=None
	    )
	hover6 = HoverTool(
	        renderers=[g6_r],
	        tooltips=[
	            ("P/B", "@g6_rPB{00.00}"),
	            ("Year", "$x{int}"),
	        ]
	    )
	chart1.add_tools(hover1)
	chart1.add_tools(hover2)
	chart1.add_tools(hover3)
	chart1.add_tools(hover4)
	chart1.add_tools(hover5)
	chart1.add_tools(hover6)


	chart1.toolbar_location = "left"
	chart1.toolbar.logo = None

	chart1.legend.location = "top_left"
	chart1.title.align = "center"
	chart1.xaxis.axis_label = "Year"
	chart1.xaxis.minor_tick_line_color = None
	chart1.yaxis.axis_label = "Trieu (vnd)"

	legend_chart1 = Legend(items=[
	    ("Quý 1"  , [g1_r]),
	    ("Quý 2" , [g2_r]),
	    ("Quý 3" , [g3_r]),
	    ("Quý 4"   , [g4_r]),
	    ("P/B"   , [g5_r,g6_r]),
	], location=(-10,-30),label_text_font_size="8pt",
	               orientation="vertical",
	               padding=10,
	               background_fill_color="#99D98C")
	legend_chart1.label_text_color="red"
	#legend.label_text_font_size

	chart1.add_layout(legend_chart1, 'right')


	chart1.yaxis.formatter = NumeralTickFormatter(format="00,000,000")
	chart1.right[0].formatter = NumeralTickFormatter(format="0.00")
	chart1.right[0].axis_label = "Lần"
	chart1.xaxis[0].ticker=FixedTicker(ticks=get_new_data_source(chart1_data,"g1_r").data.get("g1_rYear"))

	#p.tools=[PanTool(),ResetTool()]

	list_chart.append(chart1)
	#show(chart1) # show the results



	##########################################################CHART2####################################################################


	chart2 = figure (plot_height=500, title="Net income")
	chart2.toolbar_sticky = False
	upper = BoxAnnotation(top=0, fill_alpha=0.1, fill_color='olive')
	chart2.add_layout(upper)

	#,x_range=kqkd_5.ix[0,6].tolist()
	#PB line
	pe = cstc_year.ix[95,1:].copy()
	pe.name = "PE"
	data2 = get_data_chart(kqkd_5,19)
	data2["PE"] = pe.tolist()
	#chart2_data = ColumnDataSource(data2)
	# Setting the second y axis range name and range
	chart2.extra_y_ranges = {"foo": Range1d(start=0, end=int(max(get_new_data_source(data2,"g1_r").data.get("g1_rPE"))+2))}

	# Adding the second axis to the plot.
	chart2.add_layout(LinearAxis(y_range_name="foo"), 'right')



	#data

	g1_r = chart2.vbar("g1_rYear",width=0.5,top="g1_rq1",color="#006ba4",source=get_new_data_source(data2,"g1_r"),hover_fill_color="#140F2E",hover_fill_alpha=0.6)
	g2_r = chart2.vbar("g2_rYear",width=0.5,bottom="g2_rq1",top="g2_rq2",color="#ff800e",source=get_new_data_source(data2,"g2_r"),hover_fill_color="firebrick",hover_fill_alpha=0.6)
	g3_r = chart2.vbar("g3_rYear",width=0.5,bottom="g3_rq2",top="g3_rq3",color="#a2c8ec",source=get_new_data_source(data2,"g3_r"),hover_fill_color="#8F37A4",hover_fill_alpha=0.6)
	g4_r = chart2.vbar("g4_rYear",width=0.5,bottom="g4_rq3",top="g4_rq4",color="#595959",source=get_new_data_source(data2,"g4_r"),hover_fill_color="#4BC393",hover_fill_alpha=0.6)

	g5_r = chart2.line("g5_rYear","g5_rPE",source=get_new_data_source(data2,"g5_r"),y_range_name="foo",line_dash="4 4",color="red",hover_color="green")
	g6_r = chart2.asterisk("g6_rYear","g6_rPE",source=get_new_data_source(data2,"g6_r"),y_range_name="foo",size=12,color="olive")

	#hover
	hover1 = HoverTool(
	        renderers=[g1_r],
	        tooltips=[
	            ("Quý 1", "@g1_rQuy1{0,00.}"),
	            ("Year", "$x{int}"),
	        ]
	    )
	hover2 = HoverTool(
	        renderers=[g2_r],
	        tooltips=[
	            ("Quý 2", "@g2_rQuy2{0,00.}"),
	            ("Year", "$x{int}"),
	        ]
	    )
	hover3 = HoverTool(
	        renderers=[g3_r],
	        tooltips=[
	            ("Quý 3", "@g3_rQuy3{0,0.}"),
	            ("Year", "$x{int}"),
	        ]
	    )
	hover4 = HoverTool(
	        renderers=[g4_r],
	        tooltips=[
	            ("Quý 4", "@g4_rQuy4{0,00.}"),
	            ("Year", "$x{int}"),
	        ]
	    )
	hover5 = HoverTool(
	        renderers=[g5_r],
	        tooltips=None
	    )
	hover6 = HoverTool(
	        renderers=[g6_r],
	        tooltips=[
	            ("P/E", "@g6_rPE"),
	            ("Year", "$x{int}"),
	        ]
	    )

	chart2.add_tools(hover1)
	chart2.add_tools(hover2)
	chart2.add_tools(hover3)
	chart2.add_tools(hover4)
	chart2.add_tools(hover5)
	chart2.add_tools(hover6)


	chart2.legend.location = "top_left"
	chart2.title.align = "center"
	chart2.xaxis.axis_label = "Year"
	chart2.yaxis.axis_label = "Trieu (vnd)"

	legend_chart2 = Legend(items=[
	    ("Quý 1"  , [g1_r]),
	    ("Quý 2" , [g2_r]),
	    ("Quý 3" , [g3_r]),
	    ("Quý 4"   , [g4_r]),
	    ("PE"   , [g5_r,g6_r]),
	], location=(-10,-30),label_text_font_size="8pt",
	               orientation="vertical",
	               padding=10,
	               background_fill_color="#99D98C")
	legend_chart2.label_text_color="red"
	#legend.label_text_font_size

	chart2.add_layout(legend_chart2, 'right')

	chart2.xaxis.minor_tick_line_color = None
	chart2.xaxis[0].ticker=FixedTicker(ticks=get_new_data_source(data2,"g1_r").data.get("g1_rYear"))

	chart2.yaxis.formatter = NumeralTickFormatter(format="00,000,000")
	chart2.right[0].formatter = NumeralTickFormatter(format="0.00")
	chart2.right[0].axis_label = "Lần"
	chart2.toolbar_location ="left"
	chart2.toolbar.logo = None


	#p.tools=[PanTool(),ResetTool()]
	list_chart.append(chart2)
	#show(chart2) # show the results
	#chart1_data.data.get("Quý 1")

	##################################################CHART3######################################################################
	chart3_4_data = cstc_year.ix[[19,21,15,18],1:].T
	chart3_4_data.columns = ["ROE","ROA","Gross_profit_margin","ROS"]

	chart3 = figure(plot_height=500, title="Income ratio")
	chart3.y_range = Range1d(start =min(get_new_data_source(chart3_4_data,"g1_r").data.get("g1_rROA"))-20 ,end = max(get_new_data_source(chart3_4_data,"g1_r").data.get("g1_rROE"))+20)

	chart3.toolbar_sticky = False

	upper = BoxAnnotation(top=0, fill_alpha=0.1, fill_color='olive')
	chart3.add_layout(upper)

	g1_r = chart3.line("index","g1_rROE",source=get_new_data_source(chart3_4_data,"g1_r"), line_dash=[4, 4], line_color="orange", line_width=2,hover_color="#3CB464")
	g2_r = chart3.line("index","g2_rROA",source=get_new_data_source(chart3_4_data,"g2_r"),line_dash=[4, 4], line_width =2, line_color="green",hover_color="#75D1AE")

	g3_r = chart3.diamond_cross("index","g3_rROE",source=get_new_data_source(chart3_4_data,"g3_r"), color="#BF40BF",size=12,fill_color=None,hover_fill_color="#BAE5E8")
	g4_r = chart3.cross("index","g4_rROA",source=get_new_data_source(chart3_4_data,"g4_r"),size=12,color="red")

	#hover
	hover1 = HoverTool(
	        renderers=[g1_r],
	        tooltips=None
	    )
	hover2 = HoverTool(
	        renderers=[g2_r],
	        tooltips=None
	    )
	hover3 = HoverTool(
	        renderers=[g3_r],
	        tooltips=[
	            ("ROE", "@g3_rROE"),
	            #("ROA", "@ROA{0,00.}"),
	            ("Year", "$x{int}"),
	        ]
	    )
	hover4 = HoverTool(
	        renderers=[g4_r],
	        tooltips=[
	            #("ROE", "@ROE"),
	            ("ROA", "@g4_rROA"),
	            ("Year", "$x{int}"),
	        ]
	    )

	chart3.add_tools(hover1)
	chart3.add_tools(hover2)
	chart3.add_tools(hover3)
	chart3.add_tools(hover4)

	chart3.legend.location = "top_left"
	chart3.title.align = "center"
	chart3.xaxis.axis_label = "Year"
	chart3.xaxis[0].ticker=FixedTicker(ticks=chart3_4_data.index.astype("int").tolist())

	chart3.yaxis.axis_label = "(%)"

	#labels = LabelSet(x='index', y='ROE', text='ROE', level='glyph', x_offset=5, y_offset=5, source=chart3_4_data, render_mode='canvas',text_font_size="10")


	#chart3.add_layout(labels)
	legend_chart3 = Legend(items=[
	    ("Roe_ratio"  , [g1_r,g3_r]),
	    ("Roa_ratio" , [g2_r,g4_r]),

	], location=(10,-30),label_text_font_size="10pt",
	               orientation="vertical",
	               padding=10,
	               background_fill_color="#EDE8F7")
	legend_chart3.label_text_color="#568A2E"
	legend_chart3.label_width = 120
	#legend.label_text_font_size

	chart3.add_layout(legend_chart3, 'right')
	chart3.toolbar.logo = None
	chart3.toolbar_location = "left"
	list_chart.append(chart3)

	#show(chart3) # show the results
	##################################################CHART4######################################################################
	chart4 = figure(plot_height=500, title="Income ratio")
	chart4.y_range = Range1d(start =min(get_new_data_source(chart3_4_data,"g1_r").data.get("g1_rROS"))-10 ,end = max(get_new_data_source(chart3_4_data,"g1_r").data.get("g1_rGross_profit_margin"))+20)

	upper = BoxAnnotation(top=0, fill_alpha=0.1, fill_color='olive')
	chart4.add_layout(upper)

	chart4.toolbar_sticky = False
	g1_r = chart4.line("index","g1_rROS",source=get_new_data_source(chart3_4_data,"g1_r"), line_dash=[4, 4], line_color="orange", line_width=2,hover_color="#80B43C")
	g2_r = chart4.line("index","g2_rGross_profit_margin",source=get_new_data_source(chart3_4_data,"g2_r"),line_dash=[4, 4], line_width =2, line_color="green",hover_color="#C25A47")

	g3_r = chart4.x("index","g3_rROS",source=get_new_data_source(chart3_4_data,"g3_r"),size=10,line_width=2,color="#1C4C54")
	g4_r = chart4.circle("index","g4_rGross_profit_margin",source=get_new_data_source(chart3_4_data,"g4_r"),size=12,fill_color="#675EC9",fill_alpha=0.7,hover_fill_color="#4493C1")

	#hover
	hover1 = HoverTool(
	        renderers=[g1_r],
	        tooltips=None
	    )
	hover2 = HoverTool(
	        renderers=[g2_r],
	        tooltips=None
	    )
	hover3 = HoverTool(
	        renderers=[g3_r],
	        tooltips=[
	            ("ROS", "@g3_rROS"),
	            #("Gross_profit_margin", "@Gross_profit_margin{0,00.}"),
	            ("Year", "$x{int}"),
	        ]
	    )
	hover4 = HoverTool(
	        renderers=[g4_r],
	        tooltips=[
	            #("ROS", "@ROS"),
	            ("Gross_profit_margin", "@g4_rGross_profit_margin"),
	            ("Year", "$x{int}"),
	        ]
	    )

	chart4.add_tools(hover1)
	chart4.add_tools(hover2)
	chart4.add_tools(hover3)
	chart4.add_tools(hover4)

	chart4.legend.location = "top_left"
	chart4.title.align = "center"
	chart4.xaxis.axis_label = "Year"
	chart4.xaxis.minor_tick_line_color = None
	chart4.xaxis[0].ticker=FixedTicker(ticks=chart3_4_data.index.astype("int").tolist())
	chart4.yaxis.axis_label = "(%)"

	#labels = LabelSet(x='index', y='ROE', text='ROE', level='glyph', x_offset=5, y_offset=5, source=chart3_4_data, render_mode='canvas',text_font_size="10")


	#chart3.add_layout(labels)

	legend_chart4 = Legend(items=[
	    ("ROS"  , [g1_r,g3_r]),
	    ("Gross_profit_margin" , [g2_r,g4_r]),

	], location=(10,-30),label_text_font_size="10pt",
	               orientation="vertical",
	               padding=10,
	               background_fill_color="#EDE8F7")
	legend_chart3.label_text_color="red"
	legend_chart4.label_width = 120
	#legend.label_text_font_size

	chart4.add_layout(legend_chart4, 'right')
	chart4.toolbar.logo = None
	chart4.toolbar_location = "left"

	list_chart.append(chart4)
	#show(chart4) # show the results
	##################################################CHART5######################################################################
	def get_data_chart_year(dff):
    #df["Sum_year"] = df.sum(axis =1)
    #df.columns = [str(i)+"_" for i in df.columns]
	    dff = dff.T
	    if  dff.get("Attribute"):
	        dff.drop("Attribute",inplace=True)
	    dff.columns = ["_" +str(i)for i in dff.columns]
	    for i in dff.columns:
	        dff["_"+str(i)] = dff.ix[:,dff.columns[0]:i].copy().sum(axis=1)
	        #print(dff.ix[:,dff.columns[0]:i].copy())

	    return dff


	cstc_chart5 = (cdkt_year.ix[[2,5,9,18,21,28,36,46,49,52,59,64]])
	cstc_chart5.ix[73]=cstc_year.ix[73]
	chart5_data = get_data_chart_year(cstc_chart5.ix[:,1:])


	chart5 = figure(plot_height=500,plot_width=660,x_range=get_new_data_source(chart5_data,"g1_r").data.get("index"), title="Asset Structure")
	chart5.toolbar_sticky = False

	#chart5_data = ColumnDataSource(chart5_data)
	# Setting the second y axis range name and range
	chart5.extra_y_ranges = {"foo": Range1d(start=0, end=max(get_new_data_source(chart5_data,"g1_r").data.get("g1_r_73"))+10)}

	# Adding the second axis to the plot.
	chart5.add_layout(LinearAxis(y_range_name="foo"), 'right')



	#data

	g1_r = chart5.vbar("index",width=0.5,bottom=0,top="g1_r__2",color="#4f8545",source=get_new_data_source(chart5_data,"g1_r"),hover_fill_color="#140F2E",hover_fill_alpha=0.6)
	g2_r = chart5.vbar("index",width=0.5,bottom="g2_r__2",top="g2_r__5",color="#004F97",source=get_new_data_source(chart5_data,"g2_r"),hover_fill_color="firebrick",hover_fill_alpha=0.6)
	g3_r = chart5.vbar("index",width=0.5,bottom="g3_r__5",top="g3_r__9",color="#6F97D7",source=get_new_data_source(chart5_data,"g3_r"),hover_fill_color="#8F37A4",hover_fill_alpha=0.6)
	g4_r = chart5.vbar("index",width=0.5,bottom="g4_r__9",top="g4_r__18",color="#B7CFDF",source=get_new_data_source(chart5_data,"g4_r"),hover_fill_color="#4BC393",hover_fill_alpha=0.6)
	g5_r = chart5.vbar("index",width=0.5,bottom="g5_r__18",top="g5_r__21",color="#374767",source=get_new_data_source(chart5_data,"g5_r"),hover_fill_color="#7E512A",hover_fill_alpha=0.6)
	g6_r = chart5.vbar("index",width=0.5,bottom="g6_r__21",top="g6_r__28",color="#97CF00",source=get_new_data_source(chart5_data,"g6_r"),hover_fill_color="#474BC2",hover_fill_alpha=0.6)
	g7_r = chart5.vbar("index",width=0.5,bottom="g7_r__28",top="g7_r__36",color="#8F8F9F",source=get_new_data_source(chart5_data,"g7_r"),hover_fill_color="#99D98C",hover_fill_alpha=0.6)
	g8_r = chart5.vbar("index",width=0.5,bottom="g8_r__36",top="g8_r__46",color="#FFFF67",source=get_new_data_source(chart5_data,"g8_r"),hover_fill_color="#99D98C",hover_fill_alpha=0.6)
	g9_r = chart5.vbar("index",width=0.5,bottom="g9_r__46",top="g9_r__49",color="#2F6700",source=get_new_data_source(chart5_data,"g9_r"),hover_fill_color="#99D98C",hover_fill_alpha=0.6)
	g10_r = chart5.vbar("index",width=0.5,bottom="g10_r__49",top="g10_r__52",color="#65C144",source=get_new_data_source(chart5_data,"g10_r") ,hover_fill_color="#99D98C",hover_fill_alpha=0.6)
	g11_r = chart5.vbar("index",width=0.5,bottom="g11_r__52",top="g11_r__59",color="#CD9FDF",source=get_new_data_source(chart5_data,"g11_r"),hover_fill_color="#99D98C",hover_fill_alpha=0.6)

	g12_r = chart5.line("index","g12_r_73",source=get_new_data_source(chart5_data,"g12_r"),legend="TSNH_ratio", line_dash=[4, 4], line_color="orange", line_width=2,y_range_name="foo",hover_color="#79D2C8")
	g13_r = chart5.asterisk("index","g13_r_73",source=get_new_data_source(chart5_data,"g13_r"),legend="TSNH_ratio", size=12,color="olive",y_range_name="foo")

	#chart5.line("index","",source=chart5_data,y_range_name="foo")

	#hover
	hover1 = HoverTool(
	        renderers=[g1_r],
	        tooltips=[
	            ("Tiền và tương đương tiền", "@g1_r__2{0,00.}"),
	            ("Year", "$x"),
	        ]
	    )
	hover2 = HoverTool(
	        renderers=[g2_r],
	        tooltips=[

	            ("Đầu tư tài chính ngắn hạn", "@g2_r_5{0,00.}"),
	            ("Year", "$x"),
	        ]
	    )
	hover3 = HoverTool(
	        renderers=[g3_r],
	        tooltips=[

	            ("Phải thu ngắn hạn", "@g3_r_9{0,0.}"),
	            ("Year", "$x"),
	        ]
	    )
	hover4 = HoverTool(
	        renderers=[g4_r],
	        tooltips=[
	            ("Hàng tồn kho", "@g4_r_18{0,00.}"),
	            ("Year", "$x"),
	        ]
	    )
	hover5 = HoverTool(
	        renderers=[g5_r],
	        tooltips=[
	            ("Tài sản ngắn hạn khác", "@g5_r_21{0,00.}"),
	            ("Year", "$x"),
	        ]
	    )
	hover6 = HoverTool(
	        renderers=[g6_r],
	        tooltips=[
	            ("Các khoản phải thu dài hạn", "@g6_r_28{0,00.}"),
	            ("Year", "$x"),
	        ]
	    )
	hover7 = HoverTool(
	        renderers=[g7_r],
	        tooltips=[
	            ("Tài sản cố định", "@g7_r_36{0,00.}"),
	            ("Year", "$x"),
	        ]
	    )
	hover8 = HoverTool(
	        renderers=[g8_r],
	        tooltips=[
	            ("Bất động sản đầu tư", "@g8_r_46{0,00.}"),
	            ("Year", "$x"),
	        ]
	    )
	hover9 = HoverTool(
	        renderers=[g9_r],
	        tooltips=[
	            ("Tài sản dở dang dài hạn", "@g9_r_49{0,00.}"),
	            ("Year", "$x"),
	        ]
	    )
	hover10 = HoverTool(
	        renderers=[g10_r],
	        tooltips=[
	            ("Đầu tư tài chính dài hạn", "@g10_r_52{0,00.}"),
	            ("Year", "$x"),
	        ]
	    )
	hover11 = HoverTool(
	        renderers=[g11_r],
	        tooltips=[
	            ("Tài sản dài hạn khác", "@g11_r_59{0,00.}"),
	            ("Year", "$x"),
	        ]
	    )
	hover12 = HoverTool(
	        renderers=[g12_r],
	        tooltips=None
	    )
	hover13 = HoverTool(
	        renderers=[g13_r],
	        tooltips=[
	            ("Tỷ lệ tài sản thanh khoản", "@g13_r_73{0,00.}"),
	            ("Year", "$x"),
	        ]
	    )

	chart5.add_tools(hover1)
	chart5.add_tools(hover2)
	chart5.add_tools(hover3)
	chart5.add_tools(hover4)
	chart5.add_tools(hover5)
	chart5.add_tools(hover6)
	chart5.add_tools(hover7)
	chart5.add_tools(hover8)
	chart5.add_tools(hover9)
	chart5.add_tools(hover10)
	chart5.add_tools(hover11)
	chart5.add_tools(hover12)
	chart5.add_tools(hover13)

	chart5.legend.location = "top_left"

	chart5.legend.location = "top_left"#(400,100)#"bottom_left"
	chart5.legend.label_text_font_size = "7pt"
	chart5.legend.visible = False

	chart5.title.align = "center"
	chart5.xaxis.axis_label = "Year"
	chart5.yaxis.axis_label = "Trieu (vnd)"

	chart5.yaxis.formatter = NumeralTickFormatter(format="00,000,000")
	#chart5.right[0].formatter = NumeralTickFormatter(format="0.00")
	legend = Legend(items=[
	    ("Tiền và các khoản tương đương tiền"  , [g1_r]),
	    ("Đầu tư tài chính ngắn hạn" , [g2_r]),
	    ("Các khoản phải thu ngắn hạn" , [g3_r]),
	    ("Hàng tồn kho"   , [g4_r]),
	    ("Tài sản ngắn hạn khác" , [g5_r]),
	    ("Các khoản phải thu dài hạn" , [g6_r]),
	    ("Tài sản cố định"   , [g7_r]),
	    ("Bất động sản đầu tư" , [g8_r]),
	    ("Tài sản dở dang dài hạn" , [g9_r]),
	    ("Đầu tư tài chính dài hạn"   , [g10_r]),
	    ("Tài sản dài hạn khác" , [g11_r]),
	], location=(-10,-30),label_text_font_size="8pt",
	               orientation="vertical",
	               padding=10,)
	               #background_fill_color="#99D98C")
	#legend.label_text_color="red"
	#legend.label_text_font_size

	chart5.right[0].axis_label = "( % )"
	chart5.add_layout(legend, 'right')


	chart5.toolbar_location = "left"
	chart5.toolbar.logo = None
	#p.tools=[PanTool(),ResetTool()]
	#output_file("asset.html")
	list_chart.append(chart5)
	#show(chart5) # show the results


	##################################################CHART6######################################################################

	chart6_data = cdkt_year.ix[[69,78,91,100],1:]
	chart6_data.ix[130] = (cdkt_year.ix[99,1:]-cdkt_year.ix[100,1:])
	chart6_data.ix[131] = (cdkt_year.ix[68,1:]-cdkt_year.ix[69,1:]-cdkt_year.ix[78,1:]) # No ngan han khac
	chart6_data.ix[132] = (cdkt_year.ix[83,1:]-cdkt_year.ix[91,1:]) # No dai han khac
	#debt ratio having interest/total assets
	chart6_data.ix[133] = cstc_year.ix[50,1:]
	#debt ratio
	chart6_data.ix[134] = cstc_year.ix[51,1:]

	chart6_data = get_data_chart_year(chart6_data)


	chart6 = figure(plot_height=500,plot_width=660,x_range=get_new_data_source(chart6_data,"g1_r").data.get("index"), title="Liability Structure",tools = "reset,pan,wheel_zoom,box_zoom,save")
	chart6.toolbar_sticky = False

	#chart5_data = ColumnDataSource(chart5_data)
	# Setting the second y axis range name and range
	chart6.extra_y_ranges = {"foo": Range1d(start=0, end=max(get_new_data_source(chart6_data,"g1_r").data.get("g1_r_134"))+10)}

	# Adding the second axis to the plot.
	chart6.add_layout(LinearAxis(y_range_name="foo"), 'right')

	g1_r = chart6.vbar("index",width=0.5,bottom=0,        top="g1_r__69",color="#3DB854",source=get_new_data_source(chart6_data,"g1_r"),hover_fill_color="#140F2E",hover_fill_alpha=0.6)
	g2_r = chart6.vbar("index",width=0.5,bottom="g2_r__69",top="g2_r__78",color="#90C6DA",source=get_new_data_source(chart6_data,"g2_r"),hover_fill_color="firebrick",hover_fill_alpha=0.6)
	g3_r = chart6.vbar("index",width=0.5,bottom="g3_r__78",top="g3_r__91",color="#24266B",source=get_new_data_source(chart6_data,"g3_r"),hover_fill_color="#8F37A4",hover_fill_alpha=0.6)
	g4_r = chart6.vbar("index",width=0.5,bottom="g4_r__91",top="g4_r__100",color="#71D0C8",source=get_new_data_source(chart6_data,"g4_r"),hover_fill_color="#4BC393",hover_fill_alpha=0.6)
	g5_r = chart6.vbar("index",width=0.5,bottom="g5_r__100",top="g5_r__130",color="#174445",source=get_new_data_source(chart6_data,"g5_r"),hover_fill_color="#7E512A",hover_fill_alpha=0.6)
	g6_r = chart6.vbar("index",width=0.5,bottom="g6_r__130",top="g6_r__131",color="#D1B775",source=get_new_data_source(chart6_data,"g6_r"),hover_fill_color="#474BC2",hover_fill_alpha=0.6)
	g7_r = chart6.vbar("index",width=0.5,bottom="g7_r__131",top="g7_r__132",color="#BAD0E8",source=get_new_data_source(chart6_data,"g7_r"),hover_fill_color="#99D98C",hover_fill_alpha=0.6)
	#g8_r = chart6.vbar("index",width=0.5,bottom="__131",top="__132",color="#6A9ACD",source=chart6_data)

	g9_r = chart6.line("index","g9_r_133",source=get_new_data_source(chart6_data,"g9_r"),legend="Debt having interest_ratio", line_dash=[4, 4], line_color="olive", line_width=2,y_range_name="foo",hover_color="#CD6AB4")
	g10_r = chart6.line("index","g10_r_134",source=get_new_data_source(chart6_data,"g10_r"),legend="Debt_ratio", line_dash=[4, 4], line_color="red", line_width=2,y_range_name="foo",hover_color="#75D1A8")

	g11_r = chart6.x("index","g11_r_133",source=get_new_data_source(chart6_data,"g11_r"),legend="Debt having interest_ratio",size=10,line_width=2,color="#675EC9",y_range_name="foo")
	g12_r = chart6.inverted_triangle("index","g12_r_134",source=get_new_data_source(chart6_data,"g12_r"),legend="Debt_ratio", size=12,color="#94DBDA",y_range_name="foo")



	#chart5.line("index","",source=chart5_data,y_range_name="foo")

	#hover
	hover1 = HoverTool(
	        renderers=[g1_r],
	        tooltips=[
	            ("Phải trả người bán ngắn hạn", "@g1_r_69{0,00.}"),
	            ("Year", "$x"),
	        ]
	    )
	hover2 = HoverTool(
	        renderers=[g2_r],
	        tooltips=[

	            ("Vay và nợ thuê tài chính ngắn hạn", "@g2_r_78{0,00.}"),
	            ("Year", "$x"),
	        ]
	    )
	hover3 = HoverTool(
	        renderers=[g3_r],
	        tooltips=[

	            ("Vay và nợ thuê tài chính dài hạn", "@g3_r_91{0,0.}"),
	            ("Year", "$x"),
	        ]
	    )
	hover4 = HoverTool(
	        renderers=[g4_r],
	        tooltips=[
	            ("Vốn góp của chủ sở hữu", "@g4_r_100{0,00.}"),
	            ("Year", "$x"),
	        ]
	    )
	hover5 = HoverTool(
	        renderers=[g5_r],
	        tooltips=[
	            ("Quỹ và vốn khác", "@g5_r_130{0,00.}"),
	            ("Year", "$x"),
	        ]
	    )
	hover6 = HoverTool(
	        renderers=[g6_r],
	        tooltips=[
	            ("Nợ ngắn hạn khác", "@g6_r_131{0,00.}"),
	            ("Year", "$x"),
	        ]
	    )
	hover7 = HoverTool(
	        renderers=[g7_r],
	        tooltips=[
	            ("Nợ dài hạn khác", "@g7_r_132{0,00.}"),
	            ("Year", "$x"),
	        ]
	    )
	hover9= HoverTool(
	        renderers=[g9_r],
	        tooltips=None
	    )
	hover10 = HoverTool(
	        renderers=[g10_r],
	        tooltips=None
	    )
	hover11 = HoverTool(
	        renderers=[g11_r],
	        tooltips=[
	            ("Debt having interest_ratio", "@g11_r_133{0,00.00}"),
	            ("Year", "$x"),
	        ]
	    )
	hover12 = HoverTool(
	        renderers=[g12_r],
	        tooltips=[
	            ("Debt", "@g12_r_134{0,00.00}"),
	            ("Year", "$x"),
	        ]
	    )


	chart6.add_tools(hover1)
	chart6.add_tools(hover2)
	chart6.add_tools(hover3)
	chart6.add_tools(hover4)
	chart6.add_tools(hover5)
	chart6.add_tools(hover6)
	chart6.add_tools(hover7)
	chart6.add_tools(hover9)
	chart6.add_tools(hover10)
	chart6.add_tools(hover11)
	chart6.add_tools(hover12)


	chart6.legend.location = "top_left"

	chart6.legend.location = "top_left"#(400,100)#"bottom_left"
	chart6.legend.label_text_font_size = "7pt"
	chart6.legend.visible = False

	chart6.title.align = "center"
	chart6.xaxis.axis_label = "Year"
	chart6.yaxis.axis_label = "Trieu (vnd)"

	chart6.yaxis.formatter = NumeralTickFormatter(format="00,000,000")
	#chart5.right[0].formatter = NumeralTickFormatter(format="0.00")
	legend = Legend(items=[
	    ("Phải trả người bán ngắn hạn"  , [g1_r]),
	    ("Vay và nợ thuê tài chính ngắn hạn" , [g2_r]),
	    ("Vay và nợ thuê tài chính dài hạn" , [g3_r]),
	    ("Vốn góp của chủ sở hữu"   , [g4_r]),
	    ("Quỹ và vốn khác" , [g5_r]),
	    ("Nợ ngắn hạn khác" , [g6_r]),
	    ("Nợ dài hạn khác"   , [g7_r]),

	], location=(0,-100))
	legend.label_text_font_size = "8pt"

	#chart6.right[0].axis_label = "( % )"

	chart6.toolbar_location = "left"
	chart6.add_layout(legend, 'right')
	chart6.toolbar.logo=None
	#chart6.toolbar
	#p.tools=[PanTool(),ResetTool()]
	#output_file("asset.html")
	chart6.right[0].axis_label = "( % )"

	list_chart.append(chart6)
	#show(chart6) # show the results
	##################################################CHART7#####################################################################

	def get_data_chart_percent(df):
	    df = df.T
	    df["Sum"] = df.sum(axis=1)
	    start = len(df.columns)
	    for i in df.columns:
	        if i is not "Sum":
	            df["_"+str(i)] = df[i]/df["Sum"]*100
	    df.columns = ["_" + str(j) for j in df.columns]
	    for k in df.columns[start:]:
	        df["_"+str(k)] = df.ix[:,df.columns[start]:k].copy().sum(axis=1)
	    return df
	def get_data_area(df,num_attr):
	    df_tmp = get_data_chart_percent(df.ix[:,1:])
	    year = df_tmp.index.tolist()
	    #year = [y for y in range(3,7)]
	    #print(type(year))
	    #print("df_tmp =>>>>>>>>>>>>>>>>>>>>>>",df_tmp)
	    #print("year=============>",year)
	    year_tmp = year[:]
	    year.reverse()
	    year_tmp.extend(year)
	    data = {
	        "x":[],
	        "y":[],
	        "rate":[],
	    }
	    for k,i in enumerate(df_tmp.columns[:num_attr]):
	        data["x"].append(year_tmp)
	        data["rate"].append(random.random()*10)
	        if k is 0:
	            temp = df_tmp["__"+i].tolist()
	            temp.extend([0 for i in range (0,len(kqkd_year.columns[1:]))])
	            data["y"].append(temp)
	        else:
	            temp = df_tmp["__"+i].tolist()
	            reverse_tmp = data["y"][k-1][:len(kqkd_year.columns[1:])]
	            reverse_tmp.reverse()
	            temp.extend(reverse_tmp)
	            data["y"].append(temp)
	    #print(data["y"])
	    #temp_y = data["y"].copy()
	    #temp_y.reverse()
	    #data["y"] = temp_y
	    attr = df["Attribute"].copy().tolist()
	    #attr.reverse()
	    data["name"] = [name.split(".")[1] for name in attr]
	    for k,i in enumerate(df_tmp.index):
	        data["N_value"+str(i)] = df_tmp.ix[k,:num_attr].tolist()
	        data["N_percent"+str(i)] = df_tmp.ix[k,(num_attr+1):(2*num_attr+1)].tolist()
	    #data["value"] =[]
	    return data,df_tmp.index.astype("int").tolist()
	##################################################CHART7######################################################################

	color_mapper = LogColorMapper(palette=palette)
	#1,2,3,4,4,3,2,1
	color_list = ["#131E39","#131E39","#576B24","#1D5820","#BE8CD9","#B8B3E6"]
	county_xs = [[2014,2015,2016,2017,2017,2016,2015,2014],[2014,2015,2016,2017,2017,2016,2015,2014]]
	county_ys = [[6, 7, 5, 2,0,0,0,0],[8, 9, 10, 4,2,5,7,6]]
	county_names=["First","Secound"]
	county_rates = [2.7,4]
	#source = ColumnDataSource(data=get_data_area(kqkd_year.ix[[4,5,8,12]],4))
	data,index =get_data_area(kqkd_year.ix[[3,6,9,10,13,17]],6)
	source = ColumnDataSource(data)
	#source = ColumnDataSource(data=dict(x=county_xs,y=county_ys,name=county_names,rate=county_rates,))
	TOOLS = "pan,wheel_zoom,box_zoom,reset,hover,save"

	chart7 = figure(
		plot_height=500,
	    title="Expenses Structure", tools=TOOLS
	)
	chart7.grid.grid_line_color = None

	chart7.patches('x', 'y', source=source,
	          fill_color={'field': 'rate', 'transform': color_mapper},
	          fill_alpha=0.5, line_color="white", line_width=0.5,hover_fill_color="#90DAB0",hover_fill_alpha=0.2,legend="name")

	hover = chart7.select_one(HoverTool)
	#hover.point_policy = "follow_mouse"
	tool_tips=[("Name", "@name")]
	tool_tips.extend([("%-value-"+str(y), "(@N_percent"+str(y)+"{00.00}%|||"+"@N_value"+str(y)+"{00,000,000.})") for y in index[-4:]])
	#tool_tips.extend([("Value-"+str(y), "@N_value"+y+"{00,000,000.}") for y in index])
	tool_tips.append(("(Year, %)", "($x{int}, $y)"))
	tool_tips
	hover.tooltips = tool_tips
	chart7.xaxis[0].ticker=FixedTicker(ticks=index)
	chart7.title.align = "center"
	chart7.legend.location = "bottom_left"
	chart7.toolbar.logo = None
	list_chart.append(chart7)
	#show(chart7)
	##################################################CHART 8 ####################################################################

	color_mapper = LogColorMapper(palette=palette)
	#1,2,3,4,4,3,2,1
	county_xs = [[2014,2015,2016,2017,2017,2016,2015,2014],[2014,2015,2016,2017,2017,2016,2015,2014]]
	county_ys = [[6, 7, 5, 2,0,0,0,0],[8, 9, 10, 4,2,5,7,6]]
	county_names=["First","Secound"]
	county_rates = [2.7,4]
	#source = ColumnDataSource(data=get_data_area(kqkd_year.ix[[4,5,8,12]],4))
	data,index =get_data_area(kqkd_year.ix[[4,5,8,12]],4)
	source = ColumnDataSource(data)
	#source = ColumnDataSource(data=dict(x=county_xs,y=county_ys,name=county_names,rate=county_rates,))
	TOOLS = "pan,wheel_zoom,box_zoom,reset,hover,save"

	chart8 = figure(
		plot_height=500,
	    title="Net Sales Structure", tools=TOOLS
	)
	chart8.grid.grid_line_color = None

	chart8.patches('x', 'y', source=source,
	          fill_color={'field': 'rate', 'transform': color_mapper},
	          fill_alpha=0.7, line_color="white", line_width=0.5,hover_fill_color="#90DAB0",hover_fill_alpha=0.2,legend="name")

	hover = chart8.select_one(HoverTool)
	#hover.point_policy = "follow_mouse"
	tool_tips=[("Name", "@name")]
	tool_tips.extend([("%-value-"+str(y), "(@N_percent"+str(y)+"{00.00}%|||"+"@N_value"+str(y)+"{00,000,000.})") for y in index[-4:]])
	#tool_tips.extend([("Value-"+str(y), "@N_value"+y+"{00,000,000.}") for y in index])
	tool_tips.append(("(Year, %)", "($x{int}, $y)"))
	tool_tips
	hover.tooltips = tool_tips

	chart8.xaxis[0].ticker=FixedTicker(ticks=index)
	chart8.title.align = "center"
	chart8.legend.location = "bottom_left"
	chart8.toolbar.logo = None
	list_chart.append(chart8)
	#show(chart8)
	##################################################CHART 9 ####################################################################
	if "LCTT" in list_reports:
		chart9_data = get_data_chart_year(cstc_year.ix[[92,93,94],1:])
	else:
		chart9_data = get_data_chart_year(cstc_year.ix[[92,93],1:])
	chart9 = figure(plot_height=500,x_range=get_new_data_source(chart9_data,"g1_r").data.get("index"), title="Enterprise",tools = "reset,pan,wheel_zoom,box_zoom,save")
	chart9.toolbar_sticky = False

	upper = BoxAnnotation(top=0, fill_alpha=0.1, fill_color='olive')
	chart9.add_layout(upper)

	#chart5_data = ColumnDataSource(chart5_data)
	# Setting the second y axis range name and range
	chart9.extra_y_ranges = {"foo": Range1d(start=0, end=max(get_new_data_source(chart9_data,"g1_r").data.get("g1_r_93"))+1)}

	# Adding the second axis to the plot.
	chart9.add_layout(LinearAxis(y_range_name="foo"), 'right')

	g1_r = chart9.vbar("index",width=0.5,bottom=0,top="g1_r__92",color="#34495e",source=get_new_data_source(chart9_data,"g1_r"),hover_fill_color="#2c3e50",hover_fill_alpha=0.8)

	g2_r = chart9.line("index","g2_r_93",source=get_new_data_source(chart9_data,"g2_r"), line_dash=[4, 4], line_color="olive", line_width=2,y_range_name="foo")

	g4_r = chart9.diamond_cross("index","g4_r_93",source=get_new_data_source(chart9_data,"g4_r"), size=10,color="#3CB464",y_range_name="foo", fill_color=None, line_width=2)

	if "LCTT" in list_reports:
		g3_r = chart9.line("index","g3_r_94",source=get_new_data_source(chart9_data,"g3_r"), line_dash=[4, 4], line_color="orange", line_width=2,y_range_name="foo")
		g5_r = chart9.asterisk("index","g5_r_94",source=get_new_data_source(chart9_data,"g5_r"), size=12,color="#9FD7DF",y_range_name="foo")

	# chart5.line("index","",source=chart5_data,y_range_name="foo")

	# hover
	hover1 = HoverTool(
	        renderers=[g1_r],
	        tooltips=[
	            ("Enterprise value", "@g1_r_92{0,00.}"),
	            #("EV/EBIT", "@g1_r_93{0,0.00}"),
	            #("EV/EBITDA", "@g1_r_94{0,0.00}"),
	            ("Year", "$x"),
	        ]
	    )
	hover2 = HoverTool(
	        renderers=[g2_r],
	        tooltips=None
	    )

	hover4 = HoverTool(
	        renderers=[g4_r],
	        tooltips=[
	            ("EV/EBIT", "@g4_r_93{0,0.00}"),
	            ("Year", "$x"),
	        ]
	    )
	if "LCTT" in list_reports:
		hover3 = HoverTool(
		        renderers=[g3_r],
		        tooltips=None
		    )

		hover5 = HoverTool(
		        renderers=[g5_r],
		        tooltips=[
		            ("EV/EBITDA", "@g5_r_94{0,0.00}"),
		            ("Year", "$x"),
		        ]
		    )
		chart9.add_tools(hover3)
		chart9.add_tools(hover5)

	chart9.add_tools(hover1)
	chart9.add_tools(hover2)
	chart9.add_tools(hover4)






	chart9.title.align = "center"
	chart9.xaxis.axis_label = "Year"
	chart9.yaxis.axis_label = "Trieu (vnd)"

	chart9.yaxis.formatter = NumeralTickFormatter(format="00,000,000")
	chart9.legend.location = "top_left"

	chart9.toolbar.logo=None
	l = chart9.right[0]
	l.axis_label = "Lần"

	items=[
	    ("Enterprise value"  , [g1_r]),
	    ("EV/EBIT" , [g2_r,g4_r]),

	]
	if "LCTT" in list_reports:
		items.append(("EV/EBITDA" , [g3_r,g5_r]))
	legend_chart9 = Legend(items=items, location=(0,-100))
	legend_chart9.label_text_font_size = "8pt"

	#chart6.right[0].axis_label = "( % )"

	chart9.toolbar_location = "left"
	chart9.add_layout(legend_chart9, 'right')

	list_chart.append(chart9)

	#show(chart9) # show the results
	##################################################CHART 11 ###################################################################
	"""
	if num_q is not None:
	    chart11_data = Lctt_year.ix[[22,35,45],1:-1].T
	else:
	    chart11_data = Lctt_year.ix[[22,35,45],1:].T
	"""
	############# 3 Truong hop vs LC: co data va khong duoc cap nhat,co data dc cap nhat va khong co data
	if "LCTT" in list_reports:
		if flag:
			chart11_data = Lctt_year.ix[[22,35,45],1:-1].T
		else:
			chart11_data = Lctt_year.ix[[22,35,45],1:].T
		chart11_data.columns = ["KD","DT","TC"]
		chart11_data = ColumnDataSource(chart11_data)


		chart11 = figure(plot_height=500,x_range=chart11_data.data.get("index"), title="CashFlow")
		#PB line

		# region that always fills the top of the plot
		upper = BoxAnnotation(top=0, fill_alpha=0.1, fill_color='olive')
		chart11.add_layout(upper)

		#chart10_data = ColumnDataSource(chart10_data)
		# Setting the second y axis range name and range




		#data

		g1_r = chart11.line("index","KD",source=chart11_data,line_dash="8 4",color="#81A1D5")
		g2_r = chart11.line("index","DT",source=chart11_data,line_dash="4 4",color="#B4843C")
		g3_r = chart11.line("index","TC",source=chart11_data,line_dash="4 4",color="#194D4B")

		g4_r = chart11.x("index","KD",source=chart11_data,size=10,line_width=2,color="#675EC9")
		g5_r = chart11.asterisk("index","DT",source=chart11_data,size=12,color="olive")
		g6_r = chart11.inverted_triangle("index","TC",source=chart11_data,size=12,color="red")


		#hover
		hover1 = HoverTool(
		        renderers=[g4_r],
		        tooltips=[
		            ("value", "@KD{00,000,000.}"),
		            ("Year", "$x"),
		        ]
		    )
		hover2 = HoverTool(
		        renderers=[g5_r],
		        tooltips=[
		            ("value", "@DT{00,000,000.}"),
		            ("Year", "$x"),
		        ]
		    )
		hover3= HoverTool(
		        renderers=[g6_r],
		        tooltips=[
		            ("value", "@TC{00,000,000.}"),
		            ("Year", "$x"),
		        ]
		    )

		chart11.add_tools(hover1)
		chart11.add_tools(hover2)
		chart11.add_tools(hover3)


		chart11.legend.location = "top_left"
		chart11.title.align = "center"
		chart11.xaxis.axis_label = "Year"
		chart11.yaxis.axis_label = "Triệu (vnd)"

		chart11.yaxis.formatter = NumeralTickFormatter(format="00,000,000")
		#p.tools=[PanTool(),ResetTool()]

		legend_chart11 = Legend(items=[
		    ("Hoạt động kinh doanh"  , [g1_r,g4_r]),
		    ("Hoạt động đầu tư" , [g2_r,g5_r]),
		    ("Hoạt động tài chính" , [g3_r,g6_r]),

		], location=(30,-100))
		legend_chart11.label_text_font_size = "8pt"
		legend_chart11.label_width = 130
		legend_chart11
		#chart6.right[0].axis_label = "( % )"

		chart11.toolbar_location = "right"
		chart11.add_layout(legend_chart11, 'right')
		chart11.toolbar.logo=None

		list_chart.append(chart11)

	#show(chart11) # show the results
	##################################################CHART 10 ###################################################################
	"""
	if num_q is not None:
	    chart10_data = cstc_year.ix[[23,25],1:-1].T
	else:
	    chart10_data = cstc_year.ix[[23,25],1:].T
	"""
	################     CSTC da duoc xu ly o tren     ###################################
	if flag:
		chart10_data = cstc_year.ix[[23,25],1:-1].T
	else:
		chart10_data = cstc_year.ix[[23,25],1:].T

	chart10_data.columns = ["DTyoy","LNyoy"]


	chart10 = figure(plot_height=500,x_range=get_new_data_source(chart10_data,"g1_r").data.get("index"), title="Tốc độ tăng trưởng")
	#PB line
	#,x_range=chart10_data.data.get("index")s
	#,y_range=Range1d(start=0,end=100)
	#chart10_data = ColumnDataSource(chart10_data)
	# Setting the second y axis range name and range
	upper = BoxAnnotation(top=0, fill_alpha=0.1, fill_color='olive')
	chart10.add_layout(upper)



	#data

	g1_r = chart10.line("index","g1_rDTyoy",source=get_new_data_source(chart10_data,"g1_r"),line_dash="4 4",color="orange",hover_color="green")
	g2_r = chart10.line("index","g2_rLNyoy",source=get_new_data_source(chart10_data,"g2_r"),line_dash="4 4",color="red",hover_color="#A14BC3")

	g3_r = chart10.asterisk("index","g3_rDTyoy",source=get_new_data_source(chart10_data,"g3_r"),size=12,color="#9471D0")
	g4_r = chart10.circle_cross("index","g4_rLNyoy",source=get_new_data_source(chart10_data,"g4_r"),size=12,color="#8AC85B",hover_fill_color="#98DDAC")


	#hover
	hover1 = HoverTool(
	        renderers=[g1_r],
	        tooltips=None
	    )
	hover2 = HoverTool(
	        renderers=[g2_r],
	        tooltips=None
	    )
	hover3 = HoverTool(
	        renderers=[g3_r],
	        tooltips=[
	            ("value", "@g3_rDTyoy{00.00}"),
	            ("Year", "$x"),
	        ]
	    )
	hover4 = HoverTool(
	        renderers=[g4_r],
	        tooltips=[
	            ("value", "@g4_rLNyoy{00.00}"),
	            ("Year", "$x"),
	        ]
	    )

	chart10.add_tools(hover1)
	chart10.add_tools(hover2)
	chart10.add_tools(hover3)
	chart10.add_tools(hover4)



	chart10.legend.location = "top_left"
	chart10.title.align = "center"
	chart10.xaxis.axis_label = "Year"
	chart10.yaxis.axis_label = "%"

	chart10.yaxis.formatter = NumeralTickFormatter(format="00,000,000")
	#p.tools=[PanTool(),ResetTool()]

	legend_chart10 = Legend(items=[
	    ("Doanh thu yoy"  , [g1_r,g3_r]),
	    ("Lợi nhuận yoy" , [g2_r,g4_r]),

	], location=(30,-30),label_text_font_size="8pt",
	               orientation="vertical",
	               padding=10,
	               background_fill_color="#EDE8F7")
	legend_chart10.label_text_color="red"
	legend_chart10.label_width = 120
	#legend.label_text_font_size

	chart10.add_layout(legend_chart10, 'right')
	chart10.toolbar.logo = None
	list_chart.append(chart10)
	#show(chart10) # show the results

	##################################################LIST_CHART##################################################################
	return list_chart
