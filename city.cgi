# Sub City #
sub city_top {
	require 'csys.cgi';
	&get_city('read');
	if ($F{'cmode'} == 1) { &make_city; return }
	$demand = $money > 10000000 ? int($money * 0.15) : $newcity;
	if ($no_city) {
print <<NWCY;
<br><form method=$method action=$seacgi>
<input type=hidden name=id value="$F{'id'}">
<input type=hidden name=ps value="$F{'ps'}">
<input type=hidden name=mode value="play">
<input type=hidden name=cmode value="1">
<input type=submit value="建立城鎮" class=button></form>
<font color="#FF0000">需要$demand G</font>
NWCY
	return
	}
	if ($F{'cmode'} == 2) { require 'ctrade.cgi'; &ctrade_dis; return }
	if ($F{'cmode'} == 3) { require 'cbattle.cgi'; &cbattle_dis; return } 
	if ($F{'cmode'} == 4) { require 'cadmin.cgi'; &cadmin_dis; return }
	if ($F{'cmode'} == 5) { require 'cadmin.cgi'; &cadmin_intro; return }
	if ($F{'cmode'} == 6) { require 'ctrade.cgi'; &ctrade_bank; return }
	if ($F{'cmode'} == 7) { require 'cadmin.cgi'; &cadmin_bank; return }
	if ($F{'cmode'} == 8) { require 'cadmin.cgi'; &cadmin_name; return }
print <<CTOP;
<table width='100%' bgcolor=$t_bgcol border=1  bordercolor=$bdcol cellspacing=0><tr><td align=center>
港町「$cname」($owname支配下)</td></tr><tr><td>$cintro</td></tr>
<tr><td align=center><br>
<form method=$method action=$seacgi>
<input type=hidden name=id value="$F{'id'}">
<input type=hidden name=ps value="$F{'ps'}">
<input type=hidden name=mode value="play">
<input type=hidden name=cmode value="2">
<input type=submit value="購買物品" class=button>
</form><br>
<form method=$method action=$seacgi>
<input type=hidden name=id value="$F{'id'}">
<input type=hidden name=ps value="$F{'ps'}">
<input type=hidden name=mode value="play">
<input type=hidden name=cmode value="6">
<input type=submit value="城鎮銀行" class=button>
</form><br>
<form method=$method action=$seacgi>
<input type=hidden name=id value="$F{'id'}">
<input type=hidden name=ps value="$F{'ps'}">
<input type=hidden name=mode value="play">
<input type=hidden name=cmode value="3">
<input type=submit value="城鎮破壞" class=button></form><br>
CTOP
	if ($id == $owner) {
print <<CCTL;
<form method=$method action=$seacgi>
<input type=hidden name=id value="$F{'id'}">
<input type=hidden name=ps value="$F{'ps'}">
<input type=hidden name=mode value="play">
<input type=hidden name=cmode value="4">
<input type=submit value="城鎮管理" class=button>
</form><br>
<form method=$method action=$seacgi>
<input type=hidden name=id value="$F{'id'}">
<input type=hidden name=ps value="$F{'ps'}">
<input type=hidden name=mode value="play">
<input type=hidden name=cmode value="7">
<input type=submit value="更改手續費" class=button>
</form><br>
<form method=$method action=$seacgi>
<input type=hidden name=id value="$F{'id'}">
<input type=hidden name=ps value="$F{'ps'}">
<input type=hidden name=mode value="play">
<input type=hidden name=cmode value="5">
<input type=submit value="廣告宣傳" class=button>
</form><br>
<form method=$method action=$seacgi>
<input type=hidden name=id value="$F{'id'}">
<input type=hidden name=ps value="$F{'ps'}">
<input type=hidden name=mode value="play">
<input type=hidden name=cmode value="8">
<input type=submit value="重新命名" class=button>
</form>
CCTL
	}
	print qq|</td></tr></table>|;
}

# Sub Make City #
sub make_city {
	if (!$no_city) { &play("發生錯誤"); exit }
	$demand = $money > 10000000 ? int($money * 0.15) : $newcity;
	&form_table('up','100%',1);
	&reload;
print <<MAKE;
建立城鎮</td></tr><tr><td align=left>
名字：
<input type=text name=cnm class=text size=$stx_wth><br><br>
<input type=hidden name=mode value="build_city">
<input type=hidden name=cmode value="4">
需要$demand G。<br>確定建立？
MAKE
	&id_ps;
	&submit_button;
	&form_table('down');
}

# Sub Build #
sub build_city {
	&get_me($F{'id'});
	if ($action ne $F{'reload'}) { &play; exit }
	$demand = $money > 10000000 ? int($money * 0.15) : $newcity;
	if ( $money < $demand ) { &play("資金不足"); exit }
	if (!$F{'cnm'}) { &play("此名字已有人使用"); exit }
	if (length($F{'cnm'}) > $def_nb) { &play("名字的長度必須在半形$def_nb個字以內"); exit }
	require 'csys.cgi';
	$owner = $id;
	$owname = $name;
	$cname = $F{'cnm'};
	$chp = $poten;
	$cmoney = $crate = 0;
	$cintro = '歡迎光臨';
	my $cityfile = "$citydir\/$port\.dat";
	if ( -e $cityfile ) { &play("城鎮已經存在"); exit }
	$money -= $demand;
	$CityFile = new Nfile("$citydir/$port\.dat",'new');
	&set_city('new');
	eval {
		chmod(0666,"$cityfile");
	};
	&play;
}

1;