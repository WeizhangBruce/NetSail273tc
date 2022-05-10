@sp_ship = ("ship.gif<>1500<>1000<>8<>大和<>20000000<>1.5",
	    "galleass.gif<>1200<>400<>2<>巨型炮艦・海賊仕様<>10000000<>1",
	    "frigate.gif<>300<>100<>14<>武裝快船・改<>8000000<>1");
$min_demand = 50000000;

# Sub City Trade Dis #
sub ctrade_dis {
	&form_table('up','100%',1);
	&reload;
print <<CTUP;
港町「$cname」($owname支配下)</td></tr><tr><td align=left>
購入貨物：<br>
CTUP
	&reload;
	my @city_goods = split(/△/,$cload);
	foreach (0 .. $#city_goods) {
		($goods,$crest,$price) = split(/,/,$city_goods[$_]);
		$checked = $_ == 0 ? ' checked' : '';
		print qq|<input type=radio name=cgoods value="$_"$checked>|;
		print qq|$goods：$price G (庫存：$crest)<br>\n|;
	}
	&id_ps;
print <<CTMD;
<div align=right>購入量：<input type=text name=quan class=text size=10><br>
<input type=hidden name=mode value="ctrade_trade">
<input type=submit value="$sub_lbl" class=button></div></form><br>
<form method=$method action=$seacgi>
購入船艦：<br>
CTMD
	&reload;
	my @city_ship = split(/△/,$cship);
	foreach (0 .. $#city_ship) {
		($shipimg,$shipquan,$shiphp,$shipvec,$shipname,$price) = split(/,/,$city_ship[$_]);
		$checked = $_ == 0 ? ' checked' : '';
		print qq|<input type=radio name=cship value="$_"$checked>|;
		print qq|<img src="$img/$shipimg" height=15>$shipname：$price G<br>|;
		print qq|[積載：$shipquan 耐久：$shiphp 速度：$shipvec]<br>\n|;
	}
	if ($cmoney > $min_demand) {
		print qq|<br>秘寶船<br>\n|;
		foreach (0 .. $#sp_ship) {
			($shipimg,$shipquan,$shiphp,$shipvec,$shipname,$price,$demand) = split(/<>/,$sp_ship[$_]);
			next if $cmoney < $min_demand * $demand;
			$price = $price * 3 if $owner == $id;
			print qq|<input type=radio name=cship value="sp$_">|;
			print qq|<img src="$img/$shipimg" height=15>$shipname：$price G<br>|;
			print qq|[積載：$shipquan 耐久：$shiphp 速度：$shipvec]<br>\n|;
		}
	}
	&id_ps;
print <<CTDN;
<div align=right>
<input type=hidden name=mode value="ctrade_yard">
<input type=submit value="$sub_lbl" class=button></div></form><br>
<form method=$method action=$seacgi>
購入財寶：<br>
CTDN
	&reload;
	my @citem_ind = split(/△/,$citem);
	foreach (0 .. $#citem_ind) {
		($sellitem,$price) = split(/,/,$citem_ind[$_]);
		$checked = $_ == 0 ? ' checked' : '';
		print qq|<input type=radio name=citem value="$_"$checked>|;
		print qq|$sellitem：$price G<br>\n|;
	}
	&id_ps;
print <<CTBM;
<div align=right>
<input type=hidden name=mode value="ctrade_item">
<input type=submit value="$sub_lbl" class=button></div>
CTBM
if ($csell && (!$buyer || $buyer eq $id || $owner eq $id)) {
	print qq|</form><br><form method=$method action=$seacgi>\n|;
	print qq|購入町：<br>\n|;
	&reload;
	print qq|<input type=radio name=cbuy value="1">|;
	print qq|購入町：$csell G<br>\n|;
	&id_ps;
	print qq|<div align=right>\n|;
	print qq|<input type=hidden name=mode value="ctrade_csell">\n|;
	print qq|<input type=submit value="$sub_lbl" class=button></div>\n|;
}
	&form_table('down');
}

# Sub Ctrade Trade #
sub ctrade_trade {
	&get_me($F{'id'});
	if ($action ne $F{'reload'}) { &play; exit }
	require 'csys.cgi';
	&get_city;
	if ($F{'quan'} =~ /[^0-9]/) { &play("數的輸入錯誤");exit }
	my @city_goods = split(/△/,$cload);
	($goods,$crest,$price) = split(/,/,$city_goods[$F{'cgoods'}]);
	if (!$goods) { &play; exit }
	my $temp_price = $price;
	if ($owner == $id) { $price = 0 }
	&trade_check;
	$action = '';
	$cadded = $crest - $F{'quan'};
	if ($cadded > 0) {
		splice(@city_goods , $F{'cgoods'} , 1 , "$goods,$cadded,$temp_price");
	}
	elsif ($cadded <= 0) {
		splice(@city_goods , $F{'cgoods'} , 1 );
		$F{'quan'} = $crest;
	}
	$cmoney += $F{'quan'} * $price;
	$cload = join('△',@city_goods);

	$money -= $F{'quan'} * $price;
	@my_load = split(/△/,$load);
	foreach $ind(@my_load) {
		($load_name,$load_quan) = split(/,/,$ind);
		if ($load_name eq $goods) {
			$added = $load_quan + $F{'quan'};
			map {$_ = "$load_name,$added" if $_ eq "$load_name,$load_quan";} @my_load;
			$load = join('△',@my_load);
			&msg("追加購入$load_name共$F{'quan'}個");
			&add_record("$load_name以單價$price G追加購入$F{'quan'}個");
			&set_city;
			$F{'cmode'} = 2;
			&play;
			exit
		}
	}
	$load = join('△',@my_load,"$goods,$F{'quan'}");
	&msg("購入$goods共$F{'quan'}個");
	&add_record("$goods以單價$price G購入$F{'quan'}個");
	&set_city;
	$F{'cmode'} = 2;
	&play;
}

# Sub Ctrade Yard #
sub ctrade_yard {
	&get_me($F{'id'});
	if ($action ne $F{'reload'}) { &play; exit }
	require 'csys.cgi';
	&get_city;
	my @city_ship = split(/△/,$cship);
	if ($F{'cship'} =~ /sp/) {
		$sp = 1;
		$F{'cship'} =~ s/sp//;
	}
	($shipimg,$shipquan,$shiphp,$shipvec,$shipname,$price) = split(/,/,$city_ship[$F{'cship'}]) if !$sp;
	if ($sp) {
		($shipimg,$shipquan,$shiphp,$shipvec,$shipname,$price,$demand) = split(/<>/,$sp_ship[$F{'cship'}]);
		&error("ＥＲＲＯＲ") if $cmoney < $min_demand * $demand;
	}
	if (!$shipimg) { &play; exit }
	if ($owner == $id) {
		$price = 0 if !$sp;
		$price = $price * 3 if $sp;
	}
	if ( $money < $price ) { &play("資金不足"); exit }
	&ship_data;
	if ( $#ship_ind == 16 ) { &play("船艦數已滿，無法再購買"); exit}
	if ( $#ship_ind < 16 ) {
		push(@ship_ind , "$shipimg,$shipquan,$shiphp,$shipvec,$shipname");
		&msg("購入$shipname");
		&add_record("以$price G購入$shipname")
	}
	$action = '';
	$money -= $price;
	if (!$sp) {
		splice(@city_ship , $F{'cship'} ,1);
		$cship = join('△' , @city_ship);
		$cmoney += $price;
		&set_city;
	}
	$F{'cmode'} = 2;
	&play;
}

# Sub Ctrade Item #
sub ctrade_item {
	&get_me($F{'id'});
	if ($action ne $F{'reload'}) { &play; exit }
	require 'csys.cgi';
	&get_city;
	my @citem_ind = split(/△/,$citem);
	($sellitem,$price) = split(/,/,$citem_ind[$F{'citem'}]);
	if (!$sellitem) { &play; exit }
	if ($owner == $id) { $price = 0 }
	if ( $money < $price ) { &play("資金不足"); exit }
	my @item_check = split(/,/,$item_line);
	foreach (@item_check) { if ($_ eq $sellitem) { $find = 1; last } }
	if ($find) { &play("已經持有$sellitem"); exit }
	$item_line = join(',' , @item_check , $sellitem);
	$money -= $price;
	&msg("購入$sellitem");
	&add_record("以$price G購入$sellitem");
	$cmoney += $price;
	splice(@citem_ind , $F{'citem'} , 1);
	$citem = join('△',@citem_ind);
	&set_city;
	$F{'cmode'} = 2;
	&play;
}

# Sub Ctrade Bank #
sub ctrade_bank {
	&form_table('up','100%',1);
	&get_city;
	my @citybank = split(/△/,$city_line);
	foreach (@citybank) {
		($bnum,$bquan) = split(/,/);
		if ($bnum == $port) { $find = 1; last }
	}
	$bquan = $find ? $bquan : 0;
	print qq|$cname 銀行(手續費：提款金額×$crate％)|;
print <<CBKU;
</td></tr><tr><td align=center>
存款金額：$bquan G<br><br>
存款　<input type=text name=quan class=text size=15>G
<input type=hidden name=mode value="ctrade_inbk">
CBKU
	&reload;
	&id_ps;
	&submit_button;
print <<CBKD;
</form><form method=$method action=$seacgi>
提款　<input type=text name=quan class=text size=15>G
<input type=hidden name=mode value="ctrade_outbk">
CBKD
	&reload;
	&id_ps;
	&submit_button;
	&form_table('down');
}

# Sub Ctrade In Bank #
sub ctrade_inbk {
	&get_me($F{'id'});
	if ($action ne $F{'reload'}) { &play; exit }
	if ($F{'quan'} =~ /[^0-9]/) { &play("數的輸入錯誤");exit }
	if ($money < $F{'quan'}) { &play("資金不足"); exit }
	$money -= $F{'quan'};
	my @citybank = split(/△/,$city_line);
	foreach (0 .. $#citybank) {
		($bnum,$bquan) = split(/,/,$citybank[$_]);
		if ($bnum == $port) {
			$bquan += $F{'quan'};
			splice(@citybank , $_ , 1 , "$bnum,$bquan");
			$city_line = join('△' , @citybank);
			$find = 1;
			last
		}
	}
	if (!$find) { $city_line = join('△' , @citybank , "$port,$F{'quan'}") }
	&msg("存入 $F{'quan'} G");
	&get_port($area,$port);
	&add_record("在 $p_name 的銀行存入 $F{'quan'} G");
	&play;
}

# Sub Ctrade Out Bank #
sub ctrade_outbk {
	&get_me($F{'id'});
	if ($action ne $F{'reload'}) { &play; exit }
	if ($F{'quan'} =~ /[^0-9]/) { &play("數的輸入錯誤");exit }
	my @citybank = split(/△/,$city_line);
	foreach (0 .. $#citybank) {
		($bnum,$bquan) = split(/,/,$citybank[$_]);
		if ($bnum == $port) {
			if ($bquan - $F{'quan'} <= 0) {
				splice(@citybank , $_ , 1);
				$F{'quan'} = $bquan
			} else {
				$bquan -= $F{'quan'};
				splice(@citybank , $_ , 1 , "$bnum,$bquan")
			}
			$city_line = join('△' , @citybank);
			$find = 1;
			last
		}
	}
	if (!$find) { &play("這個銀行沒存款"); exit }
	require 'csys.cgi';
	&get_city;
	my $fee = int($F{'quan'} * $crate * 0.01);
	$money += $F{'quan'} - $fee;
	$cmoney += $fee if $owner ne $id;
	&get_port($area,$port);
	&msg("提出$F{'quan'} G，支付手續費 $fee G");
	&add_record("在 $p_name 的銀行提出$F{'quan'} G");
	&set_city;
	&play;
}

# Sub Ctrade City Sell #
sub ctrade_csell {
	&get_me($F{'id'});
	if ($action ne $F{'reload'}) { &play; exit }
	if ($F{'cbuy'} ne '1') { &play; exit }
	require 'csys.cgi';
	&get_city;
	#Ver2.73
	if (!$csell) {
		&error("ＥＲＲＯＲ");
	}
	##
	if ($buyer && $buyer ne $id) {
		&error("ＥＲＲＯＲ") if $owner ne $id;
	}
	if ($owner == $id) { $csell = 0 }
	$pre_owner = $owner; $pre_csell = $csell;
	if ( $money < $csell ) { &play("資金不足"); exit }
	$money -= $csell;
	$owner = $id; $owname = $name; $csell = 0;
	if (-f "$usrdir\/$pre_owner\.dat") {
		&get_u($pre_owner);
		if (!$dead && $pre_owner ne $id) {
			$umoney += $pre_csell;
			&add_record("$name 以 $pre_csell G 購入城鎮：「$cname」。",1);
			$urecord .= "$cname被買下來了<br>";
		}
		&set_u;
	}
	&msg("購入城鎮：「$cname」");
	&add_record("以 $pre_csell G 購入城鎮：「$cname」");
	$F{'cmode'} = 2;
	&set_city;
	&play;
}

1;