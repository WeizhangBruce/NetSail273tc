# Sub Move List #
sub move_list {
	&form_table('up','100%',1);
	&reload;
	print qq|移動　　|;
	&submit_button;
	print qq|</td></tr><tr><td align=left>\n|;
	shift(@arealine);
	$i = 0;
	foreach (@arealine) {
		$checked = $i == 0 ? ' checked' : '';
		($move_num,$move_name,$move_locate) = split(/<>/,$_);
		if ($move_num == $port) { next; }
		$take_second = &take_time($p_locate,$move_locate);
		print qq|<input type=radio name=target value="$area△$move_num"$checked>\n|;
		print qq|$move_name($take_second秒)<br>\n|;
		$i++;
	}
	undef @arealine;
	opendir(DIR,"$datadir") || &error("データディレクトリ読みこみエラー:$datadirという名前のディレクトリが無いかパーミッションが不正です");
	@areafiles = sort grep /^1.*\.dat$/,readdir(DIR);
	closedir(DIR);
	foreach (@areafiles) {
		open(IN,"$datadir\/$_") || &error("$datadir\/$_無法開啟");
		($a_line) = <IN>;
		push(@allarea,$a_line);
		close(IN);
	}
	undef @areafiles;
	print qq|<br>|;
	foreach (@allarea) {
		($area_num,$area_name,$area_locate) = split(/<>/,$_);
		if ($area_num == $area && !$port) { next; }
		$take_second = &take_time($p_locate,$area_locate);
		print qq|<input type=radio name=target value="$area_num△$area_num">\n|;
		print qq|$area_name($take_second秒)<br>\n|;
	}
	undef @allarea;
	print qq|<input type=hidden name=mode value="move">\n|;
	&id_ps;
	&form_table('down');
}

# Sub Move #
sub move {
	&get_me($F{'id'});
	if ($action ne $F{'reload'}) { &play; exit }
	$action = '';
	if ($#ship_ind < 0 ) { &play("沒有船怎麼出航呢？"); exit }
	if ($tactics == 4) { $tactics = 1 }
	&ship_data;
	&fleet;
	$port = $area if !$port; #港にいなければ
	&get_port($area,$port); #現在の港情報取得
	my $pre_area = $area;
	my $pre_port = $port;
	my $pre_locate = $p_locate;
	($area,$port) = split(/△/,$F{'target'});
	if ($area != $pre_area && $port != $area) { $port = $area } #不正対策
	&get_port($area,$port);#移動先の港情報取得
	$take_second = &take_time($p_locate,$pre_locate);
	my $request = int($waste * $take_second * ($sailor + 100));
	my $sv_exist = &item_search($item_line,@save);
	if ($sv_exist != -1) { $request = int($request * 0.8);}
	if ( $food < $request && $pre_area != $pre_port) {
		$area = $pre_area; $port = $pre_port;
		&play("食物不足[需要$request單位]");
		exit
	}
	if ($pre_area != $pre_port) {
		$food -= $request;
		&msg("$save[$sv_exist]使得食物消耗減少") if $sv_exist != -1;
	}
	undef $port if $area == $port;
	$moved = time + $take_second;
	&converge if $port;
	&play;
}	

# Sub Item Search # 引数[0]=$item_line or $uitem_line, 引数[1]... = 対象アイテム
sub item_search {
	foreach $j(1 .. $#_) {
		if (index($_[0],"$_[$j]") != -1) {
			return ($j - 1);
		}
	}
	return (-1);
}

# Sub Take Time #
sub take_time {
	my ($xa,$ya) = split(/,/,$_[0]);
	my ($xb,$yb) = split(/,/,$_[1]);
	my $y = abs($ya - $yb);
	$y = 360 - $y if $y > 180;
	$base_sec = sqrt( ($xa - $xb)*($xa - $xb) + $y * $y );
	return( int(($base_sec * $time_scale) /$vector) )if $vector;
	return(0) if !$vector;
}

# Sub Converge #
sub converge {
	return if 0.9 < $p_price && $p_price < 1.1;
	$p_price = ($p_price * $p_price * $p_price / 6) - ($p_price * $p_price / 2) + 1.457 * $p_price - 0.124;
	$port_line = "$p_num<>$p_name<>$p_locate<>$trade_line<>$p_price<>\n";
	&set_port($port_line);
}

# Sub Set Port #
sub set_port {
	my $AreaFile = new Nfile("$datadir/$area.dat",'save');
	@arealine = $AreaFile->read;
	my ($ch_port) = split(/<>/,$_[0]);
	foreach (0 .. $#arealine) {
		($num) = split(/<>/,$arealine[$_]);
		if ($num == $ch_port) { $arealine[$_] = $_[0]; last;}
	}
	$AreaFile->write(@arealine);
}

1;