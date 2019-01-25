$( document ).ready(function() {
    console.log( "ready!" );
    var list_chart = $("#list-chart").text();
    var FCFE_table = $("#FCFE_table").text();
    console.log("list_chart", list_chart.length);
    console.log("FCFE_table: ", FCFE_table.length);

    var pathname = $(location).attr('pathname');
    pathname = pathname.split("/")[1]
    //console.log("pathname: ", pathname);
    //console.log("pathname: ", pathname.split("/"));
    //Them js cho phan noi dung
    if (list_chart.length < 20 && FCFE_table.length < 300){
    	$("footer").attr("class","fixed-bottom");
    	console.log("tren");
    }else{
    	$("footer").removeClass("fixed-bottom");
    	//$("footer").attr("class","visible");
    	console.log("duooi");
    }
    var width = $(window).width();
	console.log("width ban đầu: ", width)

    if((pathname == "register" || pathname == "login" || pathname == "forgot") && width > 770){
    	$("footer").attr("class","fixed-bottom");
    	console.log("register or login big_screen");
    }
/*
    //Them js cho phan noi dung
    if ((FCFE_table.length) < 100){
    	$("footer").attr("class","fixed-bottom");
    }else{
    	$("footer").attr("class","visible");
    }
*/
	$("#download").click(function(){
		$("#submit_form").attr("action","/download/").submit();
		return false;
	});

	$("#btn-submit").click(function(){
		$("#submit_form").attr("action","/").submit();
	});

	$("#btn-valuation").click(function(){
		$("#submit_form").attr("action","/valuation/").submit();
	});

	$("#btn-visualize").click(function(){
		$("#submit_form").attr("action","/").submit();
	});

	$(".tmp-fade").fadeOut(7000);

	//MODEL
	$("#menu_save").click(function(){
		stock_id = $("#stock_id");
		$("#stock_id_send").val(stock_id.val());
		$("#exampleModal").modal('show');
	})
	/*
	
	*/
	function getFormData(form){
		form_data = {};
	    form.each(function(){
	    	//console.log($(this));
		   	if($(this).attr("type") == "radio" && $(this).is(":checked")){
		   		form_data[$(this).attr("name")] = $(this).val();
		   		//console.log($(this));
		   	}
		   	else if($(this).attr("type") != "radio") {
		   		form_data[$(this).attr("name")] = $(this).val();
		   	}
	   })
	    return form_data;
	   //console.log(form_data);
	}
	//console.log($("#form_3_stages input"));
	$("#send_data").click(function(){
		console.log("vao=======================> ")
		//Lay ma co phieu set vao form_input_hidden truoc khi set vao cac form va gui di
		//Lay cac form ra chuan bi gui di
		//console.log($("#Stock_id_hidden").val());
		$("#Stock_id_hidden").val($("#stock_id_send").val());
		console.log($("#Stock_id_hidden").val());
		
		form_input = $("#submit_form_input input");
		form_2_stages = $("#form_2_stages input");
		form_3_stages = $("#form_3_stages input");
		form_n_stages = $("#form_n_stages input");
		
		//console.log(getFormData(form_3_stages));
		/*
		k = JSON.stringify({"form_input": getFormData(form_input),
									"form_2_stages": getFormData(form_2_stages),
									"form_3_stages": getFormData(form_3_stages),
									"form_n_stages": getFormData(form_n_stages)
									});
		console.log(k);
		*/
		$.ajax({
			type: "POST",
			url: "/save_valuation/",
			dataType: 'json',
			beforeSend: function(){
				
				//form_3_stages = $("#form_3_stages input");
				//console.log(getFormData(form_3_stages));
			},
			contentType: 'application/json',
			data: JSON.stringify({"form_input": getFormData(form_input),
									"form_2_stages": getFormData(form_2_stages),
									"form_3_stages": getFormData(form_3_stages),
									"form_n_stages": getFormData(form_n_stages)
									}),
			success: function(data){
				console.log(data);
				if(data["message"] != undefined){
					//$("#message").removeClass("d-none");
					$("#message").html('<p class="wow bounceInUp alert alert-primary flex-fill mx-1 my-1">' + data["message"] + '</p>');
					$("#message").parent().removeAttr("style");
					$("#message").parent().fadeOut(4000);
				}
				$("#exampleModal").modal('hide');
				}
		});
		
	})


	//if width < 770
	if(width < 770){
		$("footer").attr("class","visible");
	}
	/*
	if(width){
			//console.log("html error_large_view: " ,$("#error_large_view").html()); 
			$("#error_small_view").html($("#error_large_view").html());
			$("#error_small_view").fadeOut(7000);
	}
	*/

	$( window ).resize(function(){
		var width = $(window).width();
		console.log("width khi resize: ", width);
		if(width < 770){
			$("footer").attr("class","visible");
		}else{
			// luu y them dong nay
			/*
			console.log("vao========");
			console.log("list_chart", list_chart.length);
			console.log("FCFE_table: ", FCFE_table.length);
			console.log(typeof(FCFE_table.length))
			*/
			if ((FCFE_table.length) < 300){
	    		$("footer").attr("class","visible fixed-bottom");
    		}else{
    			$("footer").attr("class","visible");
    		}
		}

		if((pathname == "register" || pathname == "login") && width > 770){
	    	$("footer").attr("class","fixed-bottom");
	    	console.log("register or login big_screen resize");
    	}
	})
	//==========================================================================start 1 ========================================================


	function input_(label_name = "", label_val = ""){
		str_return = '<div class="col-md-6 wow bounceInUp"> <div class="form-group row">';
		str_return +='<label class="col-sm-6 col-6 col-form-label" for="">'+label_name+'</label><div class="col-sm-6 col-6">';
		str_return +='<input class="form-control text-center form-control-plaintext" id="'+label_name+'" name="'+label_name+'" type="text" value="'+label_val+'"></div></div></div>';
		return str_return
	}

	tmp_1 = $("#Initial_ROE, #Initial_NI, #Initial_Chi_tieu_von_dau_tu, #Initial_KH, #Initial_Thay_doi_von_luu_dong, #Initial_No_phat_hanh_thuan");
	tmp_2 = $("#Initial_ROC, #Initial_EBIT_HDKD_AT");
	tmp_3 = $("#Stable_g, #Stable_ROE, #Stable_ROC");
	tmp_4 = $("#Tax, #Lai_suat_vay, #Beta, #Lai_suat_phi_rui_ro, #Phan_bu_rui_ro")
	tmp_5= $("#Shares_Outstand, #Tong_no_vay, #Cash_Investment");

	//console.log("tmp_2", tmp_2);
	//console.log(tmp_1);
	$("#submit_form_input").on("change", "#Initial_ROE, #Initial_NI, #Initial_Chi_tieu_von_dau_tu, #Initial_KH, #Initial_Thay_doi_von_luu_dong, #Initial_No_phat_hanh_thuan, #Initial_ROC, #Initial_EBIT_HDKD_AT, #Stable_g, #Stable_ROE, #Stable_ROC, #Tax, #Lai_suat_vay, #Beta, #Lai_suat_phi_rui_ro, #Phan_bu_rui_ro", function(){
		//console.log($(this));
		arr_1 = new Array();
		arr_2 = new Array();
		arr_3 = new Array();
		arr_4 = new Array();

		tmp_1.each(function(index){
			//console.log($(this).attr("id"), " || ", $(this).val());
			if($(this).val()){
				arr_1[index] = $(this).attr("id");
				//console.log("arr_1", Object.keys(arr_1).length);
			}
		})

		tmp_2.each(function(index){
			if($(this).val()){
				arr_2[index] = $(this).attr("id");
				//console.log(arr_2, "vao");
			}
		})

		tmp_3.each(function(index){
			if($(this).val()){
				arr_3[index] = $(this).attr("id");
			}
		})
		tmp_4.each(function(index){
			if($(this).val()){
				arr_4[index] = $(this).attr("id");
			}
		})
		//console.log(arr_1);
		//Kiểm tra dữ liệu đã được nhập đủ hay chưa
		if(Object.keys(arr_1).length == 6){
			//console.log(typeof(parseFloat($("#Initial_NI").val())));
			Initial_Tai_dau_tu = parseFloat($("#Initial_Chi_tieu_von_dau_tu").val()) - parseFloat($("#Initial_KH").val()) + parseFloat($("#Initial_Thay_doi_von_luu_dong").val());
			Initial_FCFE = parseFloat($("#Initial_NI").val()) - Initial_Tai_dau_tu + parseFloat($("#Initial_No_phat_hanh_thuan").val());
			Initial_Ty_le_Tai_dau_tu_VCP = 1 - Initial_FCFE/(parseFloat($("#Initial_NI").val()));
			Initial_Ty_le_no_tren_tai_dau_tu = parseFloat($("#Initial_No_phat_hanh_thuan").val())/Initial_Tai_dau_tu;
			first_g = parseFloat($("#Initial_ROE").val()) * Initial_Ty_le_Tai_dau_tu_VCP/100;
			//console.log("Toc do tang truong ban dau NI", first_g);
			//console.log("Ty_le_Tai_dau_tu_VCP", Initial_Ty_le_Tai_dau_tu_VCP);
			//console.log("Ty_le_no_tren_tai_dau_tu", Initial_Ty_le_no_tren_tai_dau_tu);
			str_first_g = input_("Toc_do_tang_truong_ban_dau_NI", Number((first_g*100).toFixed(2)));
			str_Initial_Ty_le_Tai_dau_tu_VCP = input_("Initial_Ty_le_Tai_dau_tu_VCP", Number((Initial_Ty_le_Tai_dau_tu_VCP*100).toFixed(2)));
			str_Initial_Ty_le_no_tren_tai_dau_tu = input_("Initial_Ty_le_no_tren_tai_dau_tu", Number((Initial_Ty_le_no_tren_tai_dau_tu*100).toFixed(2)));
			//console.log("test jquery: ", $("#Initial_No_phat_hanh_thuan_7").next()[0].id);
			if($("#Initial_No_phat_hanh_thuan_7").next()[0].id == "Initial_ROC_8"){
				$("#Initial_No_phat_hanh_thuan_7").after(str_Initial_Ty_le_no_tren_tai_dau_tu);
				$("#Initial_No_phat_hanh_thuan_7").after(str_Initial_Ty_le_Tai_dau_tu_VCP);
				$("#Initial_No_phat_hanh_thuan_7").after(str_first_g);
			}else{
				//console.log("vao");
				//console.log("=====> ",$("#Initial_Ty_le_Tai_dau_tu_VCP"));
				$("#Toc_do_tang_truong_ban_dau_NI").val(Number((first_g*100).toFixed(2)));
				$("#Initial_Ty_le_Tai_dau_tu_VCP").val(Number((Initial_Ty_le_Tai_dau_tu_VCP*100).toFixed(2)));
				$("#Initial_Ty_le_no_tren_tai_dau_tu").val(Number((Initial_Ty_le_no_tren_tai_dau_tu*100).toFixed(2)));

			}

			if(Object.keys(arr_2).length == 2){
				
				Initial_EBIT_HDKD_AT = parseFloat($("#Initial_EBIT_HDKD_AT").val());
				Initial_FCFF = Initial_EBIT_HDKD_AT - Initial_Tai_dau_tu;
				Initial_Ty_le_Tai_dau_tu = Initial_Tai_dau_tu/Initial_EBIT_HDKD_AT;
				//console.log("vao===============", Initial_Ty_le_Tai_dau_tu);

				first_g_FCFF = parseFloat($("#Initial_ROC").val()) * Initial_Ty_le_Tai_dau_tu/100;
				//console.log("first_g_FCFF", first_g_FCFF);

				str_first_g_FCFF = input_("Toc_do_tang_truong_BD_EBIT_AT", Number((first_g_FCFF*100).toFixed(2)));
				str_Initial_Ty_le_Tai_dau_tu = input_("Initial_Ty_le_Tai_dau_tu", Number((Initial_Ty_le_Tai_dau_tu*100).toFixed(2)));
				//console.log(str_first_g_FCFF);
				if($("#Initial_EBIT_HDKD_AT_9").next().attr("id") == "Stable_g_10"){
					$("#Initial_EBIT_HDKD_AT_9").after(str_Initial_Ty_le_Tai_dau_tu);
					$("#Initial_EBIT_HDKD_AT_9").after(str_first_g_FCFF);
				}
				else{
					$("#Toc_do_tang_truong_BD_EBIT_AT").val(Number((first_g_FCFF*100).toFixed(2)));
					$("#Initial_Ty_le_Tai_dau_tu").val(Number((Initial_Ty_le_Tai_dau_tu*100).toFixed(2)));
				}

			}else{
				if($("#Toc_do_tang_truong_BD_EBIT_AT").length != 0){
					for (i = 0; i < 2; i++) {
						$("#Initial_EBIT_HDKD_AT_9").next().remove();
					}
				}
			}
			//console.log("vao nek",Object.keys(arr_4).length);
			if(Object.keys(arr_4).length == 5){

				//console.log("vao");
				Initial_Ty_le_no_vay = Initial_Ty_le_no_tren_tai_dau_tu;
				Initial_Ty_le_VCP = 1 - Initial_Ty_le_no_vay;

				Initial_Chi_phi_von_co_phan = (parseFloat($("#Lai_suat_phi_rui_ro").val())/100) + parseFloat($("#Beta").val()) * (parseFloat($("#Phan_bu_rui_ro").val())/100);
				Initial_WACC = (parseFloat($("#Lai_suat_vay").val())/100) * (1-parseFloat($("#Tax").val())/100) * Initial_Ty_le_no_vay + Initial_Chi_phi_von_co_phan * Initial_Ty_le_VCP; 

				Stable_Ty_le_no_vay = Initial_Ty_le_no_vay
				Stable_Ty_le_VCP = 1 - Stable_Ty_le_no_vay

				Stable_Chi_phi_von_co_phan = (parseFloat($("#Lai_suat_phi_rui_ro").val())/100) + 1*(parseFloat($("#Phan_bu_rui_ro").val())/100);
				Stable_WACC = (parseFloat($("#Lai_suat_vay").val())/100) * (1-parseFloat($("#Tax").val())/100) * Stable_Ty_le_no_vay + Stable_Chi_phi_von_co_phan * Stable_Ty_le_VCP;


				str_Initial_Chi_phi_von_co_phan = input_("Initial_Chi_phi_von_co_phan", Number((Initial_Chi_phi_von_co_phan*100).toFixed(2))); 
				str_Initial_WACC = input_("Initial_WACC", Number((Initial_WACC*100).toFixed(2)));

				str_Stable_Chi_phi_von_co_phan = input_("Stable_Chi_phi_von_co_phan", Number((Stable_Chi_phi_von_co_phan*100).toFixed(2)));
				str_Stable_WACC = input_("Stable_WACC", Number((Stable_WACC*100).toFixed(2))); 

				//console.log("test: ", $("#Initial_WACC").length);
				if( $("#Initial_WACC").length == 0){
					//console.log("vao=============> ");
					$("#Phan_bu_rui_ro_17").after(str_Stable_WACC);
					$("#Phan_bu_rui_ro_17").after(str_Stable_Chi_phi_von_co_phan);
					$("#Phan_bu_rui_ro_17").after(str_Initial_WACC);
					$("#Phan_bu_rui_ro_17").after(str_Initial_Chi_phi_von_co_phan);
				}else{
					$("#Initial_Chi_phi_von_co_phan").val(Number((Initial_Chi_phi_von_co_phan*100).toFixed(2)));
					$("#Initial_WACC").val(Number((Initial_WACC*100).toFixed(2)));

					$("#Stable_Chi_phi_von_co_phan").val(Number((Stable_Chi_phi_von_co_phan*100).toFixed(2)));
					$("#Stable_WACC").val(Number((Stable_WACC*100).toFixed(2)));
				}

			}else if($("#Initial_WACC").length != 0){
				for (i = 0; i < 4; i++) {
					$("#Phan_bu_rui_ro_17").next().remove();
				}
			}


			
			//console.log(str_first_g);
		}else if($("#Toc_do_tang_truong_ban_dau_NI").length != 0){
				for (i = 0; i < 3; i++) {
	  				$("#Initial_No_phat_hanh_thuan_7").next().remove();
				}
				if($("#Toc_do_tang_truong_BD_EBIT_AT").length != 0){
					for (i = 0; i < 2; i++) {
						$("#Initial_EBIT_HDKD_AT_9").next().remove();
					}
				}

				if($("#Initial_WACC").length != 0){
					for (i = 0; i < 4; i++) {
						$("#Phan_bu_rui_ro_17").next().remove();
					}
				}
			/*
			$("#Toc_do_tang_truong_ban_dau_NI").val("");
			$("#Initial_Ty_le_Tai_dau_tu_VCP").val("");
			$("#Initial_Ty_le_no_tren_tai_dau_tu").val("");
			*/
		}
		//console.log("arr_3", arr_3);
		if(Object.keys(arr_3).length == 3){
			//console.log("vao===arr_3");
			Stable_Ty_le_Tai_dau_tu_VCP = parseFloat($("#Stable_g").val())/parseFloat($("#Stable_ROE").val())
			Stable_Ty_le_Tai_dau_tu = parseFloat($("#Stable_g").val())/parseFloat($("#Stable_ROC").val())
			str_Stable_Ty_le_Tai_dau_tu_VCP = input_("Stable_Ty_le_Tai_dau_tu_VCP", Number(Stable_Ty_le_Tai_dau_tu_VCP.toFixed(2)));
			str_Stable_Ty_le_Tai_dau_tu = input_("Stable_Ty_le_Tai_dau_tu", Number(Stable_Ty_le_Tai_dau_tu.toFixed(2)));
			//console.log("===> ", $("#Stable_ROC_12").next().attr("id"));
			if($("#Stable_ROC_12").next().attr("id") == "Tax_13"){
				$("#Stable_ROC_12").after(str_Stable_Ty_le_Tai_dau_tu);
				$("#Stable_ROC_12").after(str_Stable_Ty_le_Tai_dau_tu_VCP);
			}else{
				$("#Stable_Ty_le_Tai_dau_tu_VCP").val(Number((Stable_Ty_le_Tai_dau_tu_VCP*100).toFixed(2)));
				$("#Stable_Ty_le_Tai_dau_tu").val(Number((Stable_Ty_le_Tai_dau_tu*100).toFixed(2)));
			}
		}else if($("#Stable_Ty_le_Tai_dau_tu").length != 0){
				for (i = 0; i < 2; i++) {
						$("#Stable_ROC_12").next().remove();
					}
			}

	})
	tmp_1.keyup(function(){
		console.log("keyup event tmp_1");
		$(this).trigger("change");
	})

	tmp_2.keyup(function(){
		console.log("keyup event tmp_2 ");
		$(this).trigger("change");
	})

	tmp_3.keyup(function(){
		$(this).trigger("change");
	})

	tmp_4.keyup(function(){
		$(this).trigger("change");
	})

	

	//==========================================================================end 1 ========================================================

	//==========================================================================Start function help _stages =================================================
	function ajax_result (stages){
		//Lay ma co phieu set vao form_input_hidden truoc khi set vao cac form va gui di
		stock_id = $("#stock_id");
		if(stock_id.val().length == 3 ){
			$("#Stock_id_hidden").val(stock_id.val());
			//alert(stock_id.val());
		}else{
			$("#Stock_id_hidden").val("000");
		}
		tmp_1 = $("#Stock_id_hidden, #Initial_ROE, #Initial_NI, #Initial_Chi_tieu_von_dau_tu, #Initial_KH, #Initial_Thay_doi_von_luu_dong, #Initial_No_phat_hanh_thuan");
		arr_input = $.merge($.merge(tmp_1, tmp_2), $.merge(tmp_3, tmp_4));
		arr_input = $.merge(arr_input, tmp_5);
		input_hidden_stages = $("#input_hidden_" + stages + "_stages input");

		form_n_stages = $("#form_" + stages + "_stages");
		form_n_stages_result = $("#form_" + stages + "_stages_result");
		//Truoc khi gui ajax form. Lay thong tin cua form info de dien vao nhung form phia sau de gui di
		arr_input.each(function(index){
			//console.log($(this).attr("id"), $(this).val());
			$(input_hidden_stages[index]).val($(this).val());
		})
		input_hidden_stages.each(function(){
			//console.log($(this).attr("id"), $(this).val());
		})

		if(form_n_stages_result.text().length > 100){
			form_n_stages_result.html("");
		}

		$("#_" + stages + "_stages_FCFE").html("");
		$("#_" + stages + "_stages_FCFF").html("");

		$.ajax({
			type: "POST",
			url: "/_stages/",
			data: form_n_stages.serialize(),
			success: function(data){
				console.log(data);

				stages_1 = $(data["stages_1"]);
				stages_1_no_errors = $(data["stages_1_no_errors"]);
				stages_1_errors = $(data["stages_1_errors"]);

				stages_n = $(data["stages_" + stages + ""]);
				stages_n_no_errors = $(data["stages_" + stages + "_no_errors"]);
				stages_n_errors = $(data["stages_" + stages + "_errors"]);

				FCFE_value = data["FCFE_value"];
				FCFF_value = data["FCFF_value"];

				str_FCFE_value = '<div class="col-sm-6 col-6 wow fadeInLeft py-2 pl-0">Stock Price FCFE</div> <div class="col-sm-6 col-6 text-center border border-success wow fadeInLeft py-2" >';
				str_FCFF_value = '<div class="col-sm-6 col-6 wow fadeInRight py-2 pl-0">Stock Price FCFF</div> <div class="col-sm-6 col-6 text-center border border-success wow fadeInRight py-2">';

				if (FCFE_value != undefined){
					$("#_" + stages + "_stages_FCFE").html(str_FCFE_value + Number(FCFE_value).toFixed(2) + '</div>');
				}
				if (FCFF_value != undefined){
					$("#_" + stages + "_stages_FCFF").html(str_FCFF_value + Number(FCFF_value).toFixed(2) + '</div>');
				}

				html_df_input = $(data["html_df_input"]);
				//console.log("html_df_input: ", html_df_input);
				if( html_df_input.length > 0){
					table_n_stages = '';
					html_df_input.each(function(index, element){
						table_n_stages +='<div class="table-responsive-md wow fadeInUp">';
						table_n_stages += element;
						table_n_stages += '</div>'
					})

					form_n_stages_result.html(table_n_stages);
				}

				stages_1.each(function(index, element){
					$(element).removeClass("is-invalid");
					$(element).removeClass("is-valid");
				})

				stages_n.each(function(index, element){
					$(element).removeClass("is-invalid");
					$(element).removeClass("is-valid");
				})
				//console.log("stages_1_errors", stages_1_errors.length);
				if(stages_1_errors.length > 0){
					stages_1_errors.each(function(index, element){
						$(element).addClass("is-invalid");
					})
				}

				if(stages_1_no_errors.length > 0){
					//console.log("vaoooooooooooo");
					stages_1_no_errors.each(function(index, element){
						$(element).addClass("is-valid");
					})
				}

				//console.log("stages_1_errors: ", stages_1_errors);
				
				if(stages_n_errors.length > 0){
					stages_n_errors.each(function(index, element){
						$(element).addClass("is-invalid");
					})
				}

				if(stages_n_no_errors.length > 0){
					stages_n_no_errors.each(function(index, element){
						$(element).addClass("is-valid");
					})
				}

				tmp_1 = $("#Initial_ROE, #Initial_NI, #Initial_Chi_tieu_von_dau_tu, #Initial_KH, #Initial_Thay_doi_von_luu_dong, #Initial_No_phat_hanh_thuan");
				tmp_2 = $("#Initial_ROC, #Initial_EBIT_HDKD_AT");
				tmp_3 = $("#Stable_g, #Stable_ROE, #Stable_ROC");
				tmp_4 = $("#Tax, #Lai_suat_vay, #Beta, #Lai_suat_phi_rui_ro, #Phan_bu_rui_ro");
				tmp_5= $("#Shares_Outstand, #Tong_no_vay, #Cash_Investment");
				
			}
		});
	}

	//==========================================================================End function help _stages ========================================================

	//==========================================================================Start 2_stages ========================================================
	$("#submit_2_stages").click(function(){
		ajax_result(2);
	})
	/*
	//Moi vao thi do du lieu tu form_2_stages do vao form_input 
	submit_form_input = $('#submit_form_input [type = "text"]');

	//console.log("submit_form_input", submit_form_input);
	input_hidden_2_stages = $("#input_hidden_2_stages input");
	//console.log("input_hidden_2_stages: ", input_hidden_2_stages)
	submit_form_input.each(function(index, element){
		$(this).val($(input_hidden_2_stages[index]).val());
	})
	//console.log("submit_form_input: ", submit_form_input)
	*/
	//========================================================================== End 2_stages =================================================

	//========================================================================== Start 3_stages =================================================

	$("#submit_3_stages").click(function(){
		ajax_result(3);

	})

	//========================================================================== End  3_stages =================================================

	//========================================================================== Start n_stages =================================================

	$("#submit_n_stages").click(function(){
		ajax_result("n");
	})

	$("#submit_stable_stages").click(function(){
		ajax_result("stable");
	})

	//========================================================================== End  n_stages =================================================

	//========================================================================== Start collapse =================================================
	//Active menu khi click vao
	//console.log($(".nav-fill button").slice(0,4))
	$(".nav-fill button").slice(0,4).click(function(){
		//console.log($(this).attr("class"));
		$(".nav-fill button").each(function(index, element){
			$(this).removeClass("active");
		})
		$(this).addClass("active");
	})


	//========================================================================== End collapse   =================================================

	//console.log("======>trigger: ", $("#Initial_NI"));
	$("#Initial_NI").trigger("change");
		    
});
