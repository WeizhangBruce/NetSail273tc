# Sub Buy Item Display #
sub buy_item_dis {
	print qq|財寶|;
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

}

# Sub Sell Item Display #
sub sell_item_dis {
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

}

# Sub Sell Item #
sub cadmin_initem {
	&get_me($F{'id'});
	if ($action ne $F{'reload'}) { &play; exit }
	require 'csys.cgi';
	&get_city;
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

# Sub Buy Item #
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
	if ($find) { &play("$sellitem已經持有"); exit }
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