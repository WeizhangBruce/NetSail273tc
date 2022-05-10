# Sub Ranking #
sub ranking {
	my @mlabel = ('資金王','大富豪','富豪');
	my @alabel = ('冒險王','大冒險家','冒險家');
	my @plabel = ('海賊王','大海賊','海賊');
	my @tlabel = ('交易王','大商人','商人');
	my @rlabel = ('新人冒險家','新人海賊','新人商人');

	&get_all_users;

	@moneyrnk = map  { $_->[0] }
			sort { $b->[1] <=> $a->[1] }
			map  { [$_,(split(/<>/))[4]] } @alllines;
	@advenrnk = map  { $_->[0] }
			sort { $b->[1] <=> $a->[1] }
			map  { [$_,(split(/<>/))[8]] } @alllines;
	@piracyrnk = map  { $_->[0] }
			sort { $b->[1] <=> $a->[1] }
			map  { [$_,(split(/<>/))[9]] } @alllines;
	@tradernk = map  { $_->[0] }
			sort { $b->[1] <=> $a->[1] }
			map  { [$_,(split(/<>/))[10]] } @alllines;

	$old = $#alllines < $rookie ? 0 : $#alllines + 1 - $rookie;
	@rookies = @alllines[$old .. $#alllines];
	@r_adrnk =  map  { $_->[0] }
			sort { $b->[1] <=> $a->[1] }
			map  { [$_,(split(/<>/))[8]] } @rookies;
	@r_pirnk =  map  { $_->[0] }
			sort { $b->[1] <=> $a->[1] }
			map  { [$_,(split(/<>/))[9]] } @rookies;
	@r_trrnk =  map  { $_->[0] }
			sort { $b->[1] <=> $a->[1] }
			map  { [$_,(split(/<>/))[10]] } @rookies;
	

	print qq|<table><tr><td><table border=1 bgcolor=$t_bgcol bordercolor=$bdcol cellspacing=0>\n|;
	foreach (0 .. 2) {
		($rname,$rsex,$xx) = (split(/<>/,$advenrnk[$_]))[1,3,8];
		$sex_img = $rsex ? 'woman.gif' : 'man.gif';
		$crown = $_ == 0 ? qq|<img src="$img/crown.gif">| : '';
		print qq|<tr><td><img src="$img/$sex_img"></td>\n|;
		print qq|<td>$alabel[$_]</td><td>$crown$rname</td>\n|;
		print qq|<td align=right nowrap>$xx pt</td></tr>\n|;
	}
	print qq|</table></td>\n|;

	print qq|<td><table border=1 bgcolor=$t_bgcol bordercolor=$bdcol cellspacing=0>\n|;
	foreach (0 .. 2) {
		($rname,$rsex,$xx) = (split(/<>/,$piracyrnk[$_]))[1,3,9];
		$sex_img = $rsex ? 'woman.gif' : 'man.gif';
		$crown = $_ == 0 ? qq|<img src="$img/crown.gif">| : '';
		print qq|<tr><td><img src="$img/$sex_img"></td>\n|;
		print qq|<td>$plabel[$_]</td><td>$crown$rname</td>\n|;
		print qq|<td align=right nowrap>$xx pt</td></tr>\n|;
	}
	print qq|</table></td>\n|;

	print qq|<td><table border=1 bgcolor=$t_bgcol bordercolor=$bdcol cellspacing=0>\n|;
	foreach (0 .. 2) {
		($rname,$rsex,$xx) = (split(/<>/,$tradernk[$_]))[1,3,10];
		$sex_img = $rsex ? 'woman.gif' : 'man.gif';
		$crown = $_ == 0 ? qq|<img src="$img/crown.gif">| : '';
		print qq|<tr><td><img src="$img/$sex_img"></td>\n|;
		print qq|<td>$tlabel[$_]</td><td>$crown$rname</td>\n|;
		print qq|<td align=right nowrap>$xx pt</td></tr>\n|;
	}
	print qq|</table></td></tr></table><br>\n|;

	print qq|<table><tr><td><table border=1 bgcolor=$t_bgcol bordercolor=$bdcol cellspacing=0>\n|;
	foreach (0 .. 2) {
		($rname,$rsex,$xx) = (split(/<>/,$moneyrnk[$_]))[1,3,4];
		$sex_img = $rsex ? 'woman.gif' : 'man.gif';
		$crown = $_ == 0 ? qq|<img src="$img/crown.gif">| : '';
		print qq|<tr><td><img src="$img/$sex_img"></td>\n|;
		print qq|<td>$mlabel[$_]</td><td>$crown$rname</td>\n|;
		print qq|<td align=right nowrap>$xx G</td></tr>\n|;
	}
	print qq|</table></tr>\n|;

	print qq|<tr><table border=1 bgcolor=$t_bgcol bordercolor=$bdcol cellspacing=0>\n|;
	print qq|<tr><td colspan=4 align=center>新人排行</td></tr>\n|;
	($rname,$rsex,$xx) = (split(/<>/,$r_adrnk[0]))[1,3,8];
	$sex_img = $rsex ? 'woman.gif' : 'man.gif';
	print qq|<tr><td><img src="$img/$sex_img"></td>\n|;
	print qq|<td>$rlabel[0]</td><td>$rname</td>\n|;
	print qq|<td align=right nowrap>$xx pt</td></tr>\n|;
	($rname,$rsex,$xx) = (split(/<>/,$r_pirnk[0]))[1,3,9];
	$sex_img = $rsex ? 'woman.gif' : 'man.gif';
	print qq|<tr><td><img src="$img/$sex_img"></td>\n|;
	print qq|<td>$rlabel[1]</td><td>$rname</td>\n|;
	print qq|<td align=right nowrap>$xx pt</td></tr>\n|;
	($rname,$rsex,$xx) = (split(/<>/,$r_trrnk[0]))[1,3,10];
	$sex_img = $rsex ? 'woman.gif' : 'man.gif';
	print qq|<tr><td><img src="$img/$sex_img"></td>\n|;
	print qq|<td>$rlabel[2]</td><td>$rname</td>\n|;
	print qq|<td align=right nowrap>$xx pt</td></tr></table></tr></table><br>\n|;

}

1;