# Sub City Admin #
sub cadmin_dis {
	&form_table('up','100%',1);
	&reload;
print <<ADUP;
城鎮管理</td></tr><tr><td align=left>
提領資金：<br><div align=right><input type=text name=cmoney class=text size=10>G<br>
城鎮資金：$cmoney G<br>
<input type=hidden name=id value="$F{'id'}">
<input type=hidden name=ps value="$F{'ps'}">
<input type=hidden name=mode value="cadmin_money">
<input type=submit value="$sub_lbl" class=button></div><br>
</form>
<form method=$method action=$seacgi>
<input type=hidden name=reload value="$action">
修復城鎮：<br><div align=right><input type=text name=repair class=text size=10>pt<br>
(修復1pt需花費$r_fee G)<br>HP：($chp/$poten)<br>
<input type=hidden name=id value="$F{'id'}">
<input type=hidden name=ps value="$F{'ps'}">
<input type=hidden name=mode value="cadmin_repair">
<input type=submit value="$sub_lbl" class=button></div></form><br>
<form method=$method action=$seacgi>
搬入貨物：<br>
ADUP
	&reload;
	my @city_goods = split(/△/,$load);
	foreach (0 .. $#city_goods) {
		($goods) = split(/,/,$city_goods[$_]);
		$checked = $_ == 0 ? ' checked' : '';
		print qq|<input type=radio name=cgoods value="$_"$checked>|;
		print qq|$goods<br>\n|;
	}
	&id_ps;
print <<ADMD;
<div align=right>搬入量：<input type=text name=quan class=text size=10><br>
價格設定：<input type=text name=gprice class=text size=10><br>
<input type=hidden name=mode value="cadmin_intrade">
<input type=submit value="$sub_lbl" class=button></div></form><br>
<form method=$method action=$seacgi>
搬入船艦：<br>
ADMD
	&reload;
	foreach (0 .. $#ship_ind) {
		$checked = $_ == 0 ? ' checked' : '';
		print qq|<input type=radio name=cship value="$_"$checked>|;
		print qq|$ship[$_][4]<br>\n|;
		print qq|[積載：$ship[$_][1] 耐久：$ship[$_][2] 速度：$ship[$_][3]]<br>|;
	}
	&id_ps;
print <<ADDN;
<div align=right>價格設定：<input type=text name=sprice class=text size=10><br>
<input type=hidden name=mode value="cadmin_inyard">
<input type=submit value="$sub_lbl" class=button></div></form><br>
<form method=$method action=$seacgi>
搬入財寶：<br>
ADDN
	&reload;
	my @item_ind = split(/,/,$item_line);
	foreach (0 .. $#item_ind) {
		$checked = $_ == 0 ? ' checked' : '';
		print qq|<input type=radio name=citem value="$_"$checked>|;
		print qq|$item_ind[$_]<br>\n|;
	}
	&id_ps;
print <<ADBM;
<div align=right>價格設定：<input type=text name=iprice class=text size=10><br>
<input type=hidden name=mode value="cadmin_initem">
<input type=submit value="$sub_lbl" class=button></div></form><br>
<form method=$method action=$seacgi>
售出城鎮：<br>
ADBM
	&reload;
	print qq|<input type=checkbox name=csell value="1">|;
	print qq|售出城鎮<br>\n|;
	&id_ps;
print <<ADSL;
<div align=right>價格設定：<input type=text name=cprice class=text size=10><br>
（指定買方&lt;ID指定&gt;：<input type=text name=buyer class=text size=10>）<br>
<input type=hidden name=mode value="cadmin_csell">
<input type=submit value="$sub_lbl" class=button></div>
ADSL
	&form_table('down');
}

# Sub Cadmin Money #
sub cadmin_money {
	&get_me($F{'id'});
	if ($action ne $F{'reload'}) { &play; exit }
	require 'csys.cgi';
	&get_city;
	if ( $id != $owner ) { &error("ＥＲＲＯＲ") }
	if ($F{'cmoney'} =~ /[^0-9]/) { &play("數量輸入錯誤");exit }
	my $outmoney = int($F{'cmoney'});
	$outmoney = 0 if $outmoney < 0;
#	if ( ($money + $outmoney) < 0 ) { &play("資金不足"); exit }
	$outmoney = $cmoney if $outmoney > $cmoney;
	$money += $outmoney;
	$cmoney -= $outmoney;
	$F{'cmode'} = 4;
	&msg("在$cname提領$outmoney G");
	&add_record("在$cname提領$outmoney G");
	&set_city;
	&play;
}

# Sub Cadmin Repair #
sub cadmin_repair {
	&get_me($F{'id'});
	if ($action ne $F{'reload'}) { &play; exit }
	require 'csys.cgi';
	&get_city;
	if ($id != $owner) { &error("ＥＲＲＯＲ") }
	if ($F{'repair'} =~ /[^0-9]/) { &play("數量輸入錯誤");exit }
	my $hpup = int($F{'repair'});
	$hpup = (-1) * $hpup if $hpup < 0;
	if ( $hpup * $r_fee > $money ) { &play("資金不足"); exit }
	if ( $hpup + $chp > $poten ) {
		$money -= ($poten - $chp) * $r_fee;
		$chp = $poten;
	} else {
		$money -= $hpup * $r_fee;
		$chp += $hpup;
	}
	&msg("修復城鎮");
	&set_city;
	$F{'cmode'} = 4;
	&play;
}

# Sub Cadmin In Trade #
sub cadmin_intrade {
	&get_me($F{'id'});
	if ($action ne $F{'reload'}) { &play; exit }
	require 'csys.cgi';
	&get_city;
	if ($id != $owner) { &error("ＥＲＲＯＲ") }
	if ($F{'quan'} =~ /[^0-9]/) { &play("數量輸入錯誤");exit }
	if ($F{'gprice'} =~ /[^0-9]/) { &play("數量輸入錯誤");exit }
	$F{'gprice'} = int($F{'gprice'});
	if ($F{'gprice'} < 0 ) { &play("價格設定錯誤"); exit }
	my @cload_ind = split(/△/,$cload);
	if (@cload_ind > $cl_limit) { &play("放不下這麼多的貨物"); exit }
	my @city_goods = split(/△/,$load);
	($goods,$load_quan) = split(/,/,$city_goods[$F{'cgoods'}]);
	if (!$goods) { &play; exit }
	$added = $load_quan - $F{'quan'};
	if ($added > 0) {
		splice(@city_goods , $F{'cgoods'} , 1 , "$goods,$added");
	}
	elsif ($added <= 0) {
		splice(@city_goods , $F{'cgoods'} , 1 );
		$F{'quan'} = $load_quan;
	}
	$load = join('△',@city_goods);
	$cload = join('△',@cload_ind,"$goods,$F{'quan'},$F{'gprice'}");
	&msg("搬入$goods共$F{'quan'}個");
	&add_record("在$cname搬入$goods ＠$F{'gprice'}共$F{'quan'}個");
	&set_city;
	$F{'cmode'} = 4;
	&play;
}

# Sub Cadmin In Yard #
sub cadmin_inyard {
	&get_me($F{'id'});
	if ($action ne $F{'reload'}) { &play; exit }
	require 'csys.cgi';
	&get_city;
	if ($id != $owner) { &error("ＥＲＲＯＲ") }
	if ($F{'sprice'} =~ /[^0-9]/) { &play("數量輸入錯誤");exit }
	$F{'sprice'} = int($F{'sprice'});
	if ($F{'sprice'} < 0) { &play("價格設定錯誤"); exit }
	my @cship_ind = split(/△/,$cship);
	if (@cship_ind > $cs_limit) { &play("放不下這麼多的船艦"); exit }
	&ship_data;
	&fleet;
	&load_data;
	if (!$ship[$F{'cship'}][4]) { &play; exit }
	if ( ($total - $total_load - $food - $sailor - $ship[$F{'cship'}][1]) < 0 ) {
		&play("剩餘的容量不足");
		return;
	}
	$cship = join('△',@cship_ind,"$ship_ind[$F{'cship'}],$F{'sprice'}");
	&msg("搬入$ship[$F{'cship'}][4]");
	&add_record("在$cname搬入$ship[$F{'cship'}][4]");
	splice(@ship_ind , $F{'cship'} ,1);
	&set_city;
	$F{'cmode'} = 4;
	&play;
}

# Sub Cadmin In Item #
sub cadmin_initem {
	&get_me($F{'id'});
	if ($action ne $F{'reload'}) { &play; exit }
	require 'csys.cgi';
	&get_city;
	if ($id != $owner) { &error("ＥＲＲＯＲ") }
	if ($F{'iprice'} =~ /[^0-9]/) { &play("數量輸入錯誤");exit }
	$F{'iprice'} = int($F{'iprice'});
	if ($F{'iprice'} < 0) { &play("價格設定錯誤"); exit }
	my @item_ind = split(/,/,$item_line);
	my @citem_ind = split(/△/,$citem);
	if (!$item_ind[$F{'citem'}]) { &play; exit }
	$citem = join('△',@citem_ind,"$item_ind[$F{'citem'}],$F{'iprice'}");
	&msg("搬入$item_ind[$F{'citem'}]");
	&add_record("在$cname搬入$item_ind[$F{'citem'}]");
	splice(@item_ind , $F{'citem'} , 1);
	$item_line = join(',',@item_ind);
	&set_city;
	$F{'cmode'} = 4;
	&play;
}

# Sub Cadmin Bank #
sub cadmin_bank {
	&form_table('up','100%',1);
	&reload;
	print qq|銀行‧手續費設定　　|;
	&submit_button;
print <<CBNK;
</td></tr><tr><td>
提領額　×　<input type=text name=rate value="$crate" class=text size=5>％<br>
<input type=hidden name=mode value="cadmin_setbk">
CBNK
	&id_ps;
	&form_table('down');
}

# Sub Cadmin Set Bank #
sub cadmin_setbk {
	&get_me($F{'id'});
	if ($action ne $F{'reload'}) { &play; exit }
	require 'csys.cgi';
	&get_city;
	if ($id != $owner) { &error("ＥＲＲＯＲ") }
	if ($F{"rate"} =~ /[^0-9]/) { &play("設定值錯誤"); exit }
	if ($F{'rate'} >= 99) { &play("這樣做太無道理"); exit }
	$crate = int($F{'rate'});
	$action = '';
	&set_city;
	&play;
}

# Sub Cadmin Intro #
sub cadmin_intro {
	&form_table('up','100%',1);
	&reload;
	print qq|編輯宣傳文　　|;
	&submit_button;
print <<CIN;
</td></tr><tr><td>
<textarea name=cin cols=30 rows=4 class=text>$cintro</textarea><br>
<input type=hidden name=mode value="cadmin_setin">
CIN
	&id_ps;
	&form_table('down');
}

# Sub Cadmin Set Intro #
sub cadmin_setin {
	&get_me($F{'id'});
	if ($action ne $F{'reload'}) { &play; exit }
	require 'csys.cgi';
	&get_city;
	if ($id != $owner) { &error("ＥＲＲＯＲ") }
	if (length($F{'cin'}) > $def_ib) { &play("宣傳文的長度須在半行 $def_ib 文字之內"); exit }
	$cintro = $F{'cin'};
	$action = '';
	&set_city;
	&play;
}

# Sub Cadmin City Sell #
sub cadmin_csell {
	&get_me($F{'id'});
	if ($action ne $F{'reload'}) { &play; exit }
	if (!$F{'csell'}) { &play; exit }
	require 'csys.cgi';
	&get_city;
	if ($id != $owner) { &error("ＥＲＲＯＲ") }
	if ($F{'cprice'} =~ /[^0-9]/) { &play("價格輸入錯誤"); exit }
	if ($F{'buyer'} && $F{'buyer'} =~ /[^0-9]/) { &play("指定ID錯誤"); exit }
	$csell = $F{'cprice'} + 1000000;
	$buyer = $F{'buyer'};
	$action = '';
	&set_city;
	&play;
}

# Sub Cadmin Name #
sub cadmin_name {
	&form_table('up','100%',1);
	&reload;
	print qq|重新命名　　|;
	&submit_button;
print <<CNM;
</td></tr><tr><td>
<input type=text name=cnm class=text size=$stx_wth><br>
<input type=hidden name=mode value="cadmin_setnm">
CNM
	&id_ps;
	&form_table('down');
}

# Sub Cadmin Set Name #
sub cadmin_setnm {
	&get_me($F{'id'});
	if ($action ne $F{'reload'}) { &play; exit }
	require 'csys.cgi';
	&get_city;
	if ($id != $owner) { &error("ＥＲＲＯＲ") }
	if (!$F{'cnm'}) { &play("[錯誤]名字尚未填寫。"); exit }
	if (length($F{'cnm'}) > $def_nb) { &play("名字的長度須在半行$def_nb文字之內"); exit }
	$cname = $F{'cnm'};
	$action = '';
	&set_city;
	&play;
}

1;