# Sub Bar #
sub bar_meet {
	if ($F{'ad'}) { &ad_dis; return }
	&get_all_users;
	&form_table('up','100%',1);
	&reload;
	print qq|酒場　　|;
	&submit_button;
	print qq|</td></tr><tr><td align=left>\n|;
	$p_sail = int($pay * (100 - &level($pexp*(1 + $t_item*0.01)) )/100);
print <<BAR;
	<input type=radio name=goods value="1" checked>雇用水手(一人需$p_sail G)<br>
	<input type=radio name=goods value="2">解雇水手<br>
	<input type=radio name=goods value="3">購入食物：$f_price G<br>
	<input type=radio name=goods value="4">捨棄食物<br>
	<div align=right>指定數量：<input type=text name=quan size=10></div>
	<input type=hidden name=mode value="bar_trade">
BAR
	&id_ps;
	&form_table('down');
	&form_table('up','100%',1);
	&reload;
	print qq|聽取冒險情報　　|;
	&submit_button;
	print qq|<input type=hidden name=mode value="play">\n|;
	print qq|<input type=hidden name=ad value="1">\n|;
	&id_ps;
	&form_table('down');
	print qq|<table width="100%" bgcolor=$t_bgcol border="1" bordercolor=$bdcol cellspacing=0><tr><td align=center>\n|;
	print qq|來店者</td></tr><tr><td align=center>\n|;
	foreach (@alllines) {
		($uid,$uname,$usex,$uarea,$uport,$upoint,$ufriend_line) = (split(/<>/))[0,1,3,15,16,17,22];
		if ($uport == $port && $upoint == 4 && $uid != $id) {
			if ( $friend_line !~ /$uid/ ) {
				if (!$friend_line) { $friend_line = "$uid,$uname" }
				else { $friend_line .= "△$uid,$uname" }
			}
			if ( $ufriend_line !~ /$id/ ) {
				&get_u($uid);
				if (!$ufriend_line) { $ufriend_line = "$id,$name" }
				else { $ufriend_line .= "△$id,$name" }
				&set_u;
			}
			$sex_img = $usex ? $wmn_img : $man_img;
			$on_click = qq|onClick="return opWin('$listcgi?mode=uprofile&uid=$uid','win6')"|;
			print qq|<img src="$img/$sex_img"><a href="$listcgi?mode=uprofile&uid=$uid" $on_click target=_blank>$uname</a><br>\n|;
		}
	}
	if (!$sex_img) { print qq|店裡一個客人也沒有...| }
	print qq|</td></tr></table>\n|;
}

# Sub Adventure Display #
sub ad_dis {
	my $AdFile = new Nfile("$datadir/$adfiles",'read');
	my @adfline = $AdFile->read;
	&form_table('up','100%',1);
	&reload;
	print qq|冒險情報　　|;
	&submit_button;
	print qq|</td></tr><tr><td align=left>\n|;
	foreach (0 .. $#adfline) {
		($harea,$hport,$price,$file)
		= split(/<>/,$adfline[$_]);
		if ($harea =~ /$area/ || $hport =~ /$port/) {
			$checked = !$first ? ' checked' : '';
			$first = 1;
			print qq|<input type=radio name=goods value="$_"$checked>$price G<br>|;
		}
	}
	print qq|目前沒有情報可以提供| if !$first;
	print qq|<input type=hidden name=mode value="adven">\n|;
	print qq|<input type=hidden name=check value="$first">\n|;
	&id_ps;
	&form_table('down');
}


# Sub Bar Trade #
sub bar_trade {
	&get_me($F{'id'});
	if ($action ne $F{'reload'}) { &play; exit }
	if ($F{'quan'} =~ /[^0-9]/) { &play("輸入的數值錯誤");exit }
	$F{'quan'} = int($F{'quan'});
	if ( $F{'goods'} == 1 ) {
		$price = int($pay * (100 - &level($pexp*(1 + $t_item*0.01)))/100);
		&trade_check;
		$action = '';
		$sailor += $F{'quan'};
		$money -= $price * $F{'quan'};
		&msg("雇用水手$F{'quan'}人");
		&add_record("水手以每人$price G共雇用$F{'quan'}人");
		&play; return;
	} elsif ( $F{'goods'} == 3 ) {
		$price = $f_price;
		&trade_check;
		$action = '';
		$food += $F{'quan'};
		$money -= $f_price * $F{'quan'};
		&msg("購入食物$F{'quan'}單位");
		&add_record("食物以每單位$price G共購入$F{'quan'}單位");
		&play; reurtn;
	} elsif ( $F{'goods'} == 2 ) {
		&sell_check;
		$action = '';
		$sailor -= $F{'quan'};
		if ($sailor < 0 ) { $sailor = 0; $F{'quan'} = '全部的'; }
		&msg("將水手$F{'quan'}人解雇");
		&add_record("將水手$F{'quan'}人解雇");
		&play; return;
	} elsif ( $F{'goods'} == 4 ) {
		&sell_check;
		$action = '';
		$food -= $F{'quan'};
		if ($food < 0 ) { $food = 0; $F{'quan'} = '全部的'; }
		&msg("將食物$F{'quan'}單位捨棄");
		&add_record("將食物$F{'quan'}單位捨棄");
		&play; return;
	}
}

# Sub Adven #
sub adven {
	&get_me($F{'id'});
	if (($action ne $F{'reload'}) || !$F{'check'}) { &play; exit }
	my $AdFile = new Nfile("$datadir/$adfiles",'read');
	my @adfline = $AdFile->read;
	($harea,$hport,$price,$file,$fguide) = split(/<>/,$adfline[$F{'goods'}]);
	if ($money < $price) { &play("所持金額不足"); exit }
	$money -= $price;
	$quest_flag = $file;
	my $QFile = new Nfile("$datadir/$file",'read');
	($quest_line) = $QFile->read;
	chomp($quest_line);
	$quest_line .= ",0";
	&msg("聽取冒險情報<br>$fguide");
	&add_record("$fguide");
	&play
}

1;