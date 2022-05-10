# Sub Cbattle Display #
sub cbattle_dis {
	&form_table('up','100%',1);
	&reload;
print <<CBTL;
港町「$cname」($owname支配下)</td></tr><tr><td align=center>
「$cname」残HP：$chp pt</td></tr><tr><td>
<input type=radio name=atktype value="0" checked>
武力攻擊<br>[戰鬥力決勝負]<br>
<input type=radio name=atktype value="1">
破壞工作<br>[花費$atkfee G能給予$cityatked pt的傷害]<br>
<input type=hidden name=mode value="cbattle_atk">
CBTL
	&id_ps;
	&submit_button;
	&form_table('down');
}

# Sub Cbattle Attack #
sub cbattle_atk {
	&get_me($F{'id'});
	if ($action ne $F{'reload'}) { &play; exit }
	if ($F{'atktype'} && $money < $atkfee ) { &play("資金不足"); exit }
	if (!$F{'atktype'} && $#ship_ind < 0 ) { &play("沒有任何船艦"); exit }
	&cb_limit;
	require 'csys.cgi';
	&get_city;
	if ($F{'atktype'}) {
		$chp -= $cityatked;
		$money -= $atkfee;
		if ( $chp > 0 ) { &msg("給予$cname $cityatked pt的傷害！") }
	} else {
		my $i_pwr = int($atk + $sailor/10 + rand($b_flac) - ($b_flac / 2) );
		if ($i_pwr < 0 ) { $i_pwr = 0 }
		my $u_pwr = $citypwr + int( rand($citypwr) - $citypwr/2);
		&ship_data;
		$i_atked = int(rand($#ship_ind + 1));
		$iatked_hp = $ship[$i_atked][2] - $u_pwr;
		$chp -= $i_pwr;
		if ($iatked_hp <= 0 ) {
			&i_lost;
			&msg("$ship[$i_atked][4]被擊沉！");
			&add_record("攻擊城鎮「$cname」$ship[$i_atked][4]被擊沉！")
		} else {
			splice(@ship_ind , $i_atked , 1 , "$ship[$i_atked][0],$ship[$i_atked][1],$iatked_hp,$ship[$i_atked][3],$ship[$i_atked][4]");
		}
		if ( $chp > 0 ) { &msg("給予$cname $i_pwr pt的傷害！") }
	}
	$action = '';
	if ( $chp <= 0 ) {
		require 'event.cgi';
		&set_city;
		unlink("$citydir/$port\.dat");
		&msg("讓$cname毀滅了！！");
		&add_record("$cname毀滅");
		$piracy += 5000;
		$trade = int($trade / 2) if $trade > 10000;
		$trade -= 5000;
		&msg("海賊名聲大幅上升！商人名聲大幅下降！")
		&get_port($area,$port);
		&event_write("$name攻下了$p_name的$cname！");
	} else { &set_city }
	&play;
}

# Sub City Battle Limit # $battle_line=id,time△id,time△time
sub cb_limit {
	my $city_cont = int($cont * 3);
	my @battled = split(/△/,$battle_line);
	my $last_b = pop(@battled);
	my $now = time;
	if ( ($now - $last_b)/60 < $city_cont ) { &play("$city_cont分鐘以內禁止對城鎮發動連續攻擊"); exit }
	$battle_line = join('△' , @battled , $now);
}

# Sub I Lost #
sub i_lost {
	&fleet;
	$rate = $total ? 1 - ($ship[$i_atked][1] / $total) : 0;
	$food = int($food * $rate);
	$sailor = int($sailor * $rate);
	@my_lt = split(/△/,$load);
	foreach (0 .. $#my_lt) {
		($load_name,$load_quan) = split(/,/,$my_lt[$_]);
		$load_quan = int($load_quan * $rate);
		push(@my_load , "$load_name,$load_quan") if $load_quan != 0;
	}
	$load = join('△' , @my_load);			
	splice(@ship_ind , $i_atked ,1 );
}

1;