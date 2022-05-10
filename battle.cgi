# Sub Enemy List #
sub enemy {
	&get_all_users;
	&form_table('up','100%',1);
	&reload;
	print qq|襲擊　　|;
	&submit_button;
	print qq|</td></tr><tr><td align=left>\n|;
	foreach (@alllines) {
		($uid,$uname,$usex,$uarea,$uport,$utactics) = (split(/<>/))[0,1,3,15,16,18];
		if ( ((($port != $uport) || !$port) && ($port || $uport || ($area != $uarea))) || $id == $uid) { next }
		$checked = !$first ? ' checked' : '';
		$surrender = $utactics == 3 ? ' 白旗' : '';
		$first =1;
		$sex_img = $usex ? $wmn_img : $man_img;
		$on_click = qq|onClick="return opWin('$listcgi?mode=uprofile&uid=$uid','win6')"|;
		print qq|<input type=radio name=uid value="$uid"$checked>\n|;
		print qq|<img src="$img/$sex_img"><a href="$listcgi?mode=uprofile&uid=$uid" $on_click target=_blank>$uname</a>$surrender<br>\n|;
	}
	if (!$sex_img) { print qq|附近沒有發現其他艦隊...| }
	print qq|<input type=hidden name=mode value="battle">\n|;
	&id_ps;
	&form_table('down');
	&b_lift;
}

# Sub Battle #
sub battle {
	&get_me($F{'id'});
	if ($action ne $F{'reload'}) { &play; exit }
	if ($#ship_ind < 0 ) { &play("沒有船怎麼戰鬥呢？"); exit }
	if (!$F{'uid'}) { &play; exit }
	&get_u($F{'uid'});
	if ( ((($port != $uport) || !$port) && ($port || $uport || ($area != $uarea))) || $id == $uid) { &play; exit }
	&b_limit;
	$urecord  .= "受到$name的襲擊！<br>";
	if (($utactics >= 3) ||($#uship_ind < 0) || ($utactics == 2 && rand(100) < &level($utexp*(1 + $ut_item*0.01)) ) ) {
		$piracy += 100;
		my $lost_money = int($umoney * 0.005);
		$money += $lost_money;
		$umoney -= $lost_money;
		$upiracy -= 200;
		$uadven -= 100;
		&add_record("對$name投降，獻上$lost_money G",1);
		&set_me;
		&set_u;
		&msg("<font color=\"#00AA00\">$uname投降<br>獻上$lost_money G</font>");
		&play;
		exit
	}
	&ship_data;
	&uship_data;
	if ($tactics == 0) { $turn = @ship_ind < 3 ? @ship_ind : 3 }
	elsif ($tactics == 1) { $turn = @ship_ind < 2 ? @ship_ind : 2 }
	else { $turn = 1 }
	my $aup_exist = &item_search($item_line,@atkup);
	if ($aup_exist != -1 && rand(100) < 1 && @ship_ind > 3) {
		$turn++;
		&msg("<font color=\"#00AA00\">$atkup[$aup_exist]發出一陣詭異的笑聲！<br>攻擊回數＋１！</font>");
	}
	$uturn = $tactics - $utactics > 0 ? 1 : 0; # 被襲擊側の方がより好戦である場合
	my $van_exist = &item_search($uitem_line,@vanish);
	if ($utactics == 2 && $van_exist != -1 && rand(100) < 5) {
		$turn = -1;
		$uturn = -1;
		&msg("<font color=\"#00AA00\">$uname的$vanish[$van_exist]發出耀眼的光芒！隨後消失在大海上・・・</font>");
		$urecord .= "由於$vanish[$van_exist]的庇護！回避了戰鬥！<br>";
	}
	$a_i_atk = $a_u_atk = 0;
	for (0 .. ($turn - 1)) {
		$i_atked = &s_sort;
		$u_atked = int(rand(@uship));
		if ($utactics) {
			my $uavoid = $utactics == 2 ? $ucmd / 3 : $ucmd / 5;
			$uavoid = $uavoid * (($uship[$u_atked][3] + ($unav * 0.01))/ 7);
			if (rand(100) < $uavoid) {
				&msg("<font color=\"#0000FF\">對$uname的$uship[$u_atked][4]攻擊失誤！</font>");
				next
			}
		}
		&b_p_d;
		my $sh_exist = &item_search($uitem_line,@shield);
		if ($sh_exist != -1) {
			if (rand(100) < 10 - 2 * $sh_exist) {
				&msg("<font color=\"#00AA00\">$uname的$shield[$sh_exist]將攻擊吸收！我方攻擊力下降！</font>");
				$i_pow = int($i_pow * 0.9);
				$protect = $shield[$sh_exist];
			}
		}
		$a_i_atk += $i_pow;
		if ($i_pow - int($us_pow / 5) < 0) { $usailor -= 5 * $i_pow } # 水夫で耐えた場合(被)
		else {
			$usailor -= $us_pow;
			$usailor -= 1 if $usailor > 0;
			$i_pow -= int($us_pow / 5);
			if ($uship[$u_atked][2] - $i_pow > 0) {
				$uship[$u_atked][2] -= $i_pow;
				&msg("<font color=\"#0000FF\">攻擊$uname的$uship[$u_atked][4]！給予$i_pow pt的傷害！")
			} else {
				if($#ship < 16 ) {
					push(@ship, $uship[$u_atked]);
					&msg("<font color=\"#0000FF\">奪取$uname的$uship[$u_atked][4]！</font>");
					$get_s .= "$uship[$u_atked][4] "
				} else {
					&msg("<font color=\"#0000FF\">擊沉$uname的$uship[$u_atked][4]！</font>");
					$sink_s .= "$uship[$u_atked][4] "
				}
				&u_lost;
				if ($#uship < 0) { $a_u_atk = 0; last }
			}
		}
		my $ualv = &level($uaexp*(1 + $ut_item*0.01));
		if (rand(200) < $ualv) { $u_pow += $ualv }
		my $plv = &level($pexp*(1 + $t_item*0.01));
		if (rand(200) < $plv) { $u_pow = int($u_pow * 0.9); &msg("<font color=\"#00AA00\">讓敵人畏怯了！</font>") }
		$a_u_atk += $u_pow;
		if (&u_attack == -1) { $a_i_atk = 0; last }
		if ($utactics == 2) { last if rand(100) < $ucmd * 0.5 }
	}
	for (0 .. ($uturn -1)) {
		if ($#uship < 0 || $#ship < 0) { last; }
		last if $uturn == 0;
		$i_atked = int(rand(@ship));
		$u_atked = int(rand(@uship));
		&b_p_d;
		$a_u_atk += $u_pow;
		if (&u_attack == -1) { $a_i_atk = 0; last }
	}

	if ($a_i_atk >= $a_u_atk && $a_i_atk != 0) {
		my $pup = 3000;
		$pup += int( ($upiracy - $piracy) * 0.5 ) if $upiracy > $piracy;
		$piracy += $pup; $pexp += $pup;
		my $aup = int( ($upiracy - $piracy) * 0.01 ) if $piracy < $upiracy;
		$adven += $aup; $aexp += $aup;
		$upiracy -= 200;
		$utrade -= 200;
		&item_get;
		&msg("<font color=\"#0000FF\">戰鬥勝利！</font>");
		my $lost_money = int($umoney * rand($robmoney) * 0.01);
		if (int(rand(100)) > ($ucmd / 4) && $lost_money) {
			$get_money = $lost_money;
			$money += $lost_money;
			$umoney -= $lost_money;
			&msg("<font color=\"#0000FF\">掠奪$uname $lost_money G！</font>")
		}
	} elsif ($a_i_atk != 0) {
		my $upup = 2000;
		$upup += int($piracy/10) if $piracy > $upiracy;
		$upiracy += $upup; $upexp += $upup;
		$piracy = int(0.9 * $piracy);
		$trade = int(0.9 * $trade);
		&msg("<font color=\"#FF0000\">不敵！敗逃...</font>");
		$urecord  .= "擊退！<br>"
	}
	$urecord .= "受到了$protect的庇護<br>" if $protect;
	$get_s = '無' if !$get_s; $sink_s = '無' if !$sink_s; $get_money = '0' if !$get_money; $rob_item = '無' if !$rob_item;
	$uget_s = '無' if !$uget_s; $usink_s = '無' if !$usink_s;
	if ($a_i_atk == 0 && $uturn <= 0) {
		&add_record("襲擊$uname！襲擊失敗！");
		&add_record("受到$name襲擊！回避成功！",1)
	} else {
		&add_record("襲擊$uname！<br>獲得[奪取：$get_s、擊沉：$sink_s、資金：$get_money G、財寶：$rob_item]<br>被害[奪取：$uget_s、擊沉：$usink_s]");
		&add_record("受到$name襲擊！<br>被害[奪取：$get_s、擊沉：$sink_s、資金：$get_money G、財寶：$rob_item]<br>獲得[奪取：$uget_s、擊沉：$usink_s]",1)
	}
	&into_ind; &into_uind;
	&set_me;
	&set_u;
	&play
}

# Sub Battle Pre-disposal #
sub b_p_d {
	$utotal = 0;
	for(0 .. $#uship){ $utotal += $uship[$_][1] }
	&fleet;
	$is_pow = $total ? int($sailor * $ship[$i_atked][1] / $total) : 0; # 積荷割合によって水夫配置
	$us_pow = $utotal ? int($usailor * $uship[$u_atked][1] / $utotal) : 0;
	$i_pow = int(rand(2 * $atk) + ($is_pow / 5)); # 戦闘力 = 船長戦闘力 + 水夫/５
	$u_pow = int(rand(2 * $uatk) + ($us_pow / 5))
}

# Sub U Attack #
sub u_attack {
	if ($u_pow - int($is_pow / 5) < 0) { $sailor -= 5 * $u_pow; return 1; } # 水夫で耐えた場合(自)
	else {
		$sailor -= $is_pow;
		$sailor -= 1 if $sailor > 0;
		$u_pow -= int($is_pow / 5);
		if ($ship[$i_atked][2] - $u_pow > 0) {
			$ship[$i_atked][2] -= $u_pow;
			&msg("<font color=\"#FF0000\">$ship[$i_atked][4]被攻擊！受到$u_pow pt的傷害！</font>");
			return 1;
		} else {
			if($#uship < 16 ) {
				push(@uship , $ship[$i_atked]);
				&msg("<font color=\"#FF0000\">$ship[$i_atked][4]被$uname奪取！</font>");
				$uget_s .= "$ship[$i_atked][4] ";
				&i_lost;
				return -1 if $#ship < 0;
				return 1;
			} else { &msg("<font color=\"#FF0000\">$ship[$i_atked][4]被擊沉！</font>"); $usink_s .= "$ship[$i_atked][4] " }
			&i_lost;
			return -1 if $#ship < 0;
			return 1;
		}
	}
}

# Sub Ship Sort #
sub s_sort {
	$most_ld = 0;
	for (0 .. $#ship) {
		if ($most_ld < $ship[$_][1]) {
			$most_ld = $ship[$_][1];
			$most_nb = $_;
		}
	}
	return $most_nb;
}

# Sub Get U Ship Data #
sub uship_data {
	undef @uship;
	foreach (0 .. $#uship_ind) {
		@{$uship[$_]} = split(/,/,$uship_ind[$_])
	}
}

# Sub Into I ind #
sub into_ind {
	undef @ship_ind;
	return if @ship < 0;
	foreach (0 .. $#ship) {
		next if !$ship[$_][0];
		push(@ship_ind , "$ship[$_][0],$ship[$_][1],$ship[$_][2],$ship[$_][3],$ship[$_][4]")
	}
}

# Sub Into U ind #
sub into_uind {
	undef @uship_ind;
	return if $#uship < 0;
	foreach (0 .. $#uship) {
		next if !$uship[$_][0];
		push(@uship_ind , "$uship[$_][0],$uship[$_][1],$uship[$_][2],$uship[$_][3],$uship[$_][4]")
	}
}

# Sub Battle Limit # $battle_line=id,time△id,time△time
sub b_limit {
	my @battled = split(/△/,$battle_line);
	my $last_b = pop(@battled);
	if ($battle_line =~ /$F{'uid'},/ ) { &play("短時間內不得再對$uname襲擊！"); exit }
	my $now = time;
	if ( ($now - $last_b)/60 < $cont ) { &play("$cont分以內不得連續戰鬥"); exit }
	unshift(@battled , "$F{'uid'},$now");
	$battle_line = join('△' , @battled , $now);
}

# Sub Battle Lift #
sub b_lift {
	my @battled = split(/△/,$battle_line);
	my $last_b = pop(@battled);
	my $now = time;
	my @battled = grep { ($now - (split(/,/))[1])/(60*60*24) < $same } @battled;
	$battle_line = join('△' , @battled , $last_b);
}

# Sub I Lost #
sub i_lost {
	&fleet;
	undef @my_load;
	$rate = $total ? 1 - ($ship[$i_atked][1] / $total) : 0;
	$food = int($food * $rate);
	my @my_lt = split(/△/,$load);
	foreach (0 .. $#my_lt) {
		($load_name,$load_quan) = split(/,/,$my_lt[$_]);
		$load_quan = int($load_quan * $rate);
		push(@my_load , "$load_name,$load_quan") if $load_quan != 0;
	}
	$load = join('△' , @my_load);			
	splice(@ship , $i_atked ,1 )
}

# Sub U Lost #
sub u_lost {
	$utotal = 0;
	undef @u_load;
	for(0 .. $#uship){ $utotal += $uship[$_][1] }
	$urate = $utotal ? 1 - ($uship[$u_atked][1] / $utotal) : 0;
	$ufood = int($ufood * $urate);
	my @u_lt = split(/△/,$uload);
	foreach (0 .. $#u_lt) {
		($uload_name,$uload_quan) = split(/,/,$u_lt[$_]);
		$uload_quan = int($uload_quan * $urate);
		push(@u_load , "$uload_name,$uload_quan") if $uload_quan != 0;
	}
	$uload = join('△' , @u_load);			
	splice(@uship , $u_atked ,1 )
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

# Sub Item Get #
sub item_get {
	return if !$uitem_line;
	return if int(rand(100)) < ($ucmd / 4);
	my $gd_exist = &item_search($uitem_line,@gard);
	if ($gd_exist != -1 && rand(100) > 5) {
		$urecord  .= "由於$gard[$gd_exist]的庇護把財寶守護住了<br>";
		return;
	}
	my @uitem_ind = split(/,/,$uitem_line);
	srand(time*time);
	my $rob = int(rand($#uitem_ind));
	my @item_check = split(/,/,$item_line);
	foreach (@item_check) { if ($_ eq $uitem_ind[$rob]) { $find = 1; last } }
	return if $find;
	$item_line = join(',' , @item_check , $uitem_ind[$rob]);
	&msg("<font color=\"#0000FF\">奪得$uitem_ind[$rob]！</font>");
	$rob_item = $uitem_ind[$rob];
	splice(@uitem_ind , $rob , 1);
	$uitem_line = join(',' , @uitem_ind)
}

1;