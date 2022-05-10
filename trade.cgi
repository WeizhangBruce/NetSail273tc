# Sub Set Port #
sub set_port {
	my $AreaFile = new Nfile("$datadir/$area\.dat",'save');
	@arealine = $AreaFile->read;
	my ($ch_port) = split(/<>/,$_[0]);
	foreach (0 .. $#arealine) {
		($num) = split(/<>/,$arealine[$_]);
		if ($num == $ch_port) { $arealine[$_] = $_[0]; last;}
	}
	$AreaFile->write(@arealine);
}

# Sub Trade Display #$_[0]=購入or賣出、$_[1]=$trade_line or $load、
sub trade_dis {
	return if !$port;
	@trade_goods = split(/△/,$_[1]);
	&form_table('up','100%',1);
	&reload;
	print qq|交易：$_[0]　　|;
	&submit_button;
	print qq|</td></tr><tr><td align=left>\n|;
	&t_random;
	foreach (0 .. $#trade_goods) {
		($goods,$alter) = split(/,/,$trade_goods[$_]); #購入の場合は$alterは値段、賣出の場合は$alterは在庫數
		$nrate = &fluctuate($goods);
		$checked = $_ == 0 ? ' checked' : '';
		if ($_[0] eq '購入') {
		$price = int($alter * $p_price * $nrate);
		$limit = $price != 0 ? int($money / $price) : 0 ;
		$limit = "($limit個購入可)";
		}
		elsif($_[0] eq '賣出') {
		undef $limit;
		&sell_search;
		$price = int($price * $p_price * $sell_rate * $nrate);
		}
		print qq|<input type=radio name=goods value="$_"$checked>|;
		print qq|$goods：$price G $limit<br>\n|;
	}
	print qq|<br><div align=right>$_[0]數：<input type=text name=quan size=10></div>\n|;
	undef @trade_goods;
	$buyorsell = $_[0] eq '賣出' ? 'trade_sell' : 'trade_buy';
	print qq|<input type=hidden name=mode value="$buyorsell">\n|;
	&id_ps;
	&form_table('down');
}

# Sub Sell Search #
sub sell_search {
	@port_trade = split(/△/,$trade_line) if !$port_tradeflag;
	$port_tradeflag = 1;
	foreach (@port_trade) {
		($port_goods,$price) = split(/,/,$_);
		if ($port_goods eq $goods) {
		$find = 1;
		last;
		}
	}
	if (!$find) {
		my $baseFile = new Nfile("$datadir/$g_basedat",'read');
		@base = $baseFile->read if !$baseflag;
		$baseflag = 1;
		foreach (@base) {
			($base_goods,$price) = split(/,/,$_);
			if ($base_goods eq $goods) {
				$find = 1;
				last;
			}
		}
		if (!$find) { $price = 0 }
	}
	undef $find;
}

# Sub Trade Sell #
sub trade_sell {
	&get_me($F{'id'});
	if ($action ne $F{'reload'}) { &play; exit }
	&get_port($area,$port);
	$F{'quan'} = int($F{'quan'});
	&sell_check;
	$action = '';
	my @trade_goods = split(/△/,$load);
	($goods,$load_quan) = split(/,/,$trade_goods[$F{'goods'}]);
	&sell_search;
	&t_random;
	$nrate = &fluctuate($goods);
	$price = int($price * $p_price * $sell_rate * $nrate);
	$added = $load_quan - $F{'quan'};
	if ($added > 0) {
		splice(@trade_goods , $F{'goods'} , 1 , "$goods,$added");
	}
	elsif ($added <= 0) {
		splice(@trade_goods , $F{'goods'} , 1 );
		$F{'quan'} = $load_quan;
	}
	$load = join('△',@trade_goods);
	&msg("賣出$goods $F{'quan'}個");
	&add_record("$goods以單價$price G賣出$F{'quan'}個($p_name)");
	&set_p_price(1);
	&play;
}

# Sub Trade Buy #
sub trade_buy {
	&get_me($F{'id'});
	if ($action ne $F{'reload'}) { &play; exit }
	&get_port($area,$port);
	$F{'quan'} = int($F{'quan'});
	my @trade_goods = split(/△/,$trade_line);
	($goods,$price) = split(/,/,$trade_goods[$F{'goods'}]);
	&t_random;
	$nrate = &fluctuate($goods);
	$price = int($price * $p_price * $nrate);
	if (rand(100) < &level($texp*(1 + $t_item*0.01))) { $price = int($price * 0.95); &msg("經過交涉，以單價$price G") }
	&trade_check;
	$action = '';
	@my_load = split(/△/,$load);
	foreach $ind(@my_load) {
		($load_name,$load_quan) = split(/,/,$ind);
		if ($load_name eq $goods) {
			$added = $load_quan + $F{'quan'};
			map {$_ = "$load_name,$added" if $_ eq "$load_name,$load_quan";} @my_load;
			$load = join('△',@my_load);
			&msg("追加購入$load_name共$F{'quan'}個");
			&add_record("$load_name以單價$price G追加購入$F{'quan'}個");
			&set_p_price(2);
			&play;
			exit
		}
	}
	$load = join('△',@my_load,"$goods,$F{'quan'}");
	&msg("購入$goods共$F{'quan'}個");
	&add_record("$goods以單價$price G購入$F{'quan'}個($p_name)");
	&set_p_price(2);
	&play;
}

# Sub Time Random #
sub t_random {
	&get_date(time);
	$cycle = 1 if $cycle == 0;
	$tr = (int($day / $cycle) + $month) * ($area % 1000)
}

# Sub Fluctuate #
sub fluctuate {
	my($value) = 0;
	foreach ( unpack("C*" , $_[0]) ) {
		$value += $_ * $cf * $tr
	}
	return  (0.3 * sin($value)) + 1
}

# Sub Set Port Price #
sub set_p_price {
	my $up_down = $price * $F{'quan'};
	my $p_updn = $flac * ($F{'quan'} * 50 + $up_down) < 0.1 ? $flac * ($F{'quan'} * 50 + $up_down) : 0.1;
	if ($_[0] == 1) {
		$money  += $up_down;
		$p_price = $p_price - $p_updn;
	}
	if ($_[0] == 2) {
		$money  -= $up_down;
		$p_price = $p_price + $p_updn;
	}
	$trade += int($up_down / 10000);
	$texp += int($up_down / 10000);
	$p_price = $trade_upper if $p_price > $trade_upper;
	$p_price = $trade_lower if $p_price < $trade_lower;
	$port_line = "$p_num<>$p_name<>$p_locate<>$trade_line<>$p_price<>\n";
	&set_port($port_line);
}

1;