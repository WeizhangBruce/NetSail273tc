# Sub Shipyard #
sub shipyard {
	if ($F{'yard'} == 1) { &yard_buy; return }
	if ($F{'yard'} == 2) { &yard_sell; return }
	if ($F{'yard'} == 3) { &yard_rep; return }
print <<YARD;
造船所<br><form method=$method action=$seacgi>
<input type=hidden name=id value="$F{'id'}">
<input type=hidden name=ps value="$F{'ps'}">
<input type=hidden name=mode value="play">
<input type=hidden name=yard value="1">
<input type=submit value="購入" class=button>
</form><form method=$method action=$seacgi>
<input type=hidden name=id value="$F{'id'}">
<input type=hidden name=ps value="$F{'ps'}">
<input type=hidden name=mode value="play">
<input type=hidden name=yard value="2">
<input type=submit value="售出" class=button>
</form><form method=$method action=$seacgi>
<input type=hidden name=id value="$F{'id'}">
<input type=hidden name=ps value="$F{'ps'}">
<input type=hidden name=mode value="play">
<input type=hidden name=yard value="3">
<input type=submit value="修理" class=button></form>
YARD
}

# Sub Buy Yard #
sub yard_buy {
	my $YardFile = new Nfile("$datadir/$yarddat",'read');
	my @yardline = $YardFile->read;
	&form_table('up','100%',1);
	&reload;
	print qq|造船所：購入　　|;
	&submit_button;
	print qq|</td></tr><tr><td align=left>\n|;
	foreach (0 .. $#yardline) {
		($goods,$kind,$goods_img,$sale_area,$sale_port,$volume,$ship_hp,$knot,$price)
		= split(/<>/,$yardline[$_]);
		if ($sale_area =~ /$area/ || $sale_port =~ /$port/) {
			$checked = !$first ? ' checked' : '';
			$first = 1;
			&price_up;
			print qq|<input type=radio name=goods value="$_"$checked>|;
			print qq|<img src="$img/$goods_img" height=15>$goods：$price G<br>|;
			if ($kind == 1) {
				print qq|[積載：$volume 耐久：$ship_hp 速度：$knot]<br>\n|;
			}
			elsif ($kind == 2) {
				print qq|戰鬥力＋$volume<br>\n|;
			}
			elsif ($kind == 3) {
				print qq|指揮力＋$volume<br>\n|;
			}
			elsif ($kind == 4) {
				print qq|航海力＋$volume<br>\n|;
			}
		}
	}
	print qq|<input type=hidden name=yard value="1"><input type=hidden name=mode value="buy_ship">\n|;
	&id_ps;
	&form_table('down');
}

# Sub Price Up #
sub price_up {
	if ($kind == 2 || $kind == 3 || $kind ==4) {
		my $rate = $atk + $cmd + $nav;
		$price = int($price * exp($rate * 0.03 - 3))
	}
}

# Sub Buy Ship #
sub buy_ship {
	&get_me($F{'id'});
	if ($action ne $F{'reload'}) { &play; exit }
	&get_port($area,$port);
	&ship_data;
	my $YardFile = new Nfile("$datadir/$yarddat",'read');
	my @yardline = $YardFile->read;
	($goods,$kind,$goods_img,$sale_area,$sale_port,$volume,$ship_hp,$knot,$price)
	 = split(/<>/, $yardline[$F{'goods'}] );
	if ( $sale_area !~ /$area/ && $sale_port !~ /$port/ ) { &play("發生錯誤"); exit }
	&price_up;
	if ( $money < $price ) { &play("資金不足"); exit }
	if ( $#ship_ind == 16 && $kind == 1 ) { &play("船艦數已滿，無法再購買"); exit}
	if ( $kind == 1 && $#ship_ind < 16 ) {
		push(@ship_ind , "$goods_img,$volume,$ship_hp,$knot,$goods");
		&msg("購入$goods");
		&add_record("以$price G購入$goods")
	}
	elsif ( $kind == 2 ) {
		if ($atk >= $atk_limit) { &play("已至極限，無法再強化"); exit }
		$atk += $volume;
		&msg("武裝強化");
		&add_record("戰鬥力 + $volume")
	}
	elsif ( $kind == 3 ) {
		if ($cmd >= $cmd_limit) { &play("已至極限，無法再強化"); exit }
		$cmd += $volume;
		&msg("指揮力提高了");
		&add_record("指揮力 + $volume")
	}
	elsif ( $kind == 4 ) {
		if ($nav >= $nav_limit) { &play("已至極限，無法再強化"); exit }
		$nav += $volume;
		&msg("航海力提高了");
		&add_record("航海力 + $volume")
	}
	$action = '';
	$money -= $price;
	&play;
}

# Sub Yard Sell #
sub yard_sell {
	if ( $#ship_ind < 0) { print qq|你已經沒有船了|; &return_button; return }
	my $YardFile = new Nfile("$datadir/$yarddat",'read');
	my @yardline = $YardFile->read;
	&form_table('up','100%',1);
	&reload;
	print qq|造船所：售出　　|;
	&submit_button;
	print qq|</td></tr><tr><td align=left>\n|;
	for ($i = 0; $i <= $#ship_ind; $i++) {
		($price) = map{ (split(/<>/))[8] } grep {$ship[$i][4] eq (split(/<>/,$_))[0]} @yardline;
		$price = int($price / 2);
		$checked = $i == 0 ? ' checked' : '';
		print qq|<input type=radio name=goods value="$i"$checked>|;
		print qq|$ship[$i][4]：$price G<br>\n|;
		print qq|[積載：$ship[$i][1] 耐久：$ship[$i][2] 速度：$ship[$i][3]]<br>|;
	}
	print qq|<input type=hidden name=yard value="2"><input type=hidden name=mode value="sell_ship">\n|;
	&id_ps;
	&form_table('down');
}

# Sub Sell Ship #
sub sell_ship {
	&get_me($F{'id'});
	if ($action ne $F{'reload'}) { &play; exit }
	&ship_data;
	&fleet;
	&load_data;
	if ( ($total - $total_load - $food - $sailor - $ship[$F{'goods'}][1]) < 0 ) {
		&play("剩餘的容量不足");
		return
	}
	$action = '';
	my $YardFile = new Nfile("$datadir/$yarddat",'read');
	my @yardline = $YardFile->read;
	($price) = map{ (split(/<>/))[8] } grep {$ship[$F{'goods'}][4] eq (split(/<>/,$_))[0]} @yardline;
	splice(@ship_ind , $F{'goods'} ,1);
	my $upmoney = int($price / 2);
	$money += $upmoney;
	&msg("售出$ship[$F{'goods'}][4]");
	&add_record("以$upmoney G售出$ship[$F{'goods'}][4]");
	&play;
}

# Sub Yard Repair #
sub yard_rep {
	if ( $#ship_ind < 0) { print qq|沒有船怎麼修理？|; &return_button; return }
	my $YardFile = new Nfile("$datadir/$yarddat",'read');
	my @yardline = $YardFile->read;
	&form_table('up','100%',1);
	&reload;
	print qq|造船所：修理　　|;
	&submit_button;
	print qq|</td></tr><tr><td align=left>\n|;
	for ($i = 0; $i <= $#ship_ind; $i++) {
		($max_hp,$price) = map{ (split(/<>/))[6,8] } grep {$ship[$i][4] eq (split(/<>/,$_))[0]} @yardline;
		if (!$max_hp) { $max_hp = $ship[$F{'goods'}][1] * 0.2; $price = $ship[$F{'goods'}][1] * 10000; }
		if ($max_hp <= $ship[$i][2]) { next }
		$price = $max_hp ? int($price * 0.03 / ($ship[$i][2] / $max_hp)) : 0;
		if ($ship[$i][1] > 500) { $down = $ship[$i][1] - 20 }
		elsif ($ship[$i][1] > 100) { $down = $ship[$i][1] - 10 }
		else { $down = $ship[$i][1] }
		$checked = !$f ? ' checked' : '';
		$f = 1;
		print qq|<input type=radio name=goods value="$i"$checked>|;
		print qq|$ship[$i][4]：$price G<br>\n|;
		print qq|[積載：$ship[$i][1] 耐久：$ship[$i][2] 速度：$ship[$i][3]]<br>|;
		print qq|修理後　[積載：$down 耐久：$max_hp]<br>|;
	}
	print qq|沒有需要修理的船<input type=hidden name=mode value="play">\n| if !$f;
	print qq|<input type=hidden name=yard value="3"><input type=hidden name=mode value="rep_ship">\n| if $f;
	&id_ps;
	&form_table('down');
}

# Sub Repair Ship #
sub rep_ship {
	&get_me($F{'id'});
	if ($action ne $F{'reload'}) { &play; exit }
	&ship_data;
	&fleet;
	&load_data;
	my $YardFile = new Nfile("$datadir/$yarddat",'read');
	my @yardline = $YardFile->read;
	($max_hp,$price) = map{ (split(/<>/))[6,8] } grep {$ship[$F{'goods'}][4] eq (split(/<>/,$_))[0]} @yardline;
	if (!$max_hp) { $max_hp = $ship[$F{'goods'}][1] * 0.2; $price = $ship[$F{'goods'}][1] * 10000; }
	$price = $max_hp ? int($price * 0.03 / ($ship[$F{'goods'}][2] / $max_hp)) : 0;
	if ( $money < $price ) { &play("資金不足"); exit }
	if ($ship[$F{'goods'}][1] > 500) { $down = 20 }
	elsif ($ship[$F{'goods'}][1] > 100) { $down = 10 }
	if ( ($total - $total_load - $food - $sailor - $down) < 0 ) {
		&play("剩餘的容量不足");
		return
	}
	$action = '';
	$ship[$F{'goods'}][1] = $ship[$F{'goods'}][1] - $down;
	splice(@ship_ind , $F{'goods'} ,1 ,"$ship[$F{'goods'}][0],$ship[$F{'goods'}][1],$max_hp,$ship[$F{'goods'}][3],$ship[$F{'goods'}][4]");
	$money -= $price;
	&msg("修理$ship[$F{'goods'}][4]");
	&add_record("花費$price G修理$ship[$F{'goods'}][4]");
	&play;
}

1;