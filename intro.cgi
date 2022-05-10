# Sub Introduce #
sub introduce {
	&get_me($F{'id'},'read');
	&header;
	&title;
	&label('自我介紹');
	print qq|<form method=$method action=$listcgi>\n|;
	&table('up','95%',1);
print <<INTRO;
編輯個人簡介。<br>
<textarea name=in cols=30 rows=4 class=text>$intro</textarea><br>
電子郵件（可不填寫）<br>
<input type=text name=ml value="$mail" size=$ltx_wth class=text><br>
個人網頁（可不填寫）<br>
<input type=text name=ul value="$url" size=$ltx_wth class=text>
<input type=hidden name=mode value="set_introduce">
<input type=hidden name=id value="$F{'id'}">
<input type=hidden name=ps value="$F{'ps'}">
<div align=right>
<input type=submit value="$sub_lbl" class=button>
</div>
INTRO
	&table('down');
	print qq|</form><br>\n</body>\n</html>\n|;
}

# Sub Set Introduce #
sub set_introduce {
	&get_me($F{'id'});
	&error("自我介紹文的長度需在半形$def_ib個字以內") if length $F{'in'} > $def_ib;
	&error("郵件的格式輸入錯誤") if  $F{'ml'} && $F{'ml'} !~ /(.*)\@(.*)\.(.*)/;

	&get_all_users;

	($mailcheck) = grep { $_->[0] ne $F{'id'} }
	   	   	 grep { $_->[1] && $_->[1] eq $F{'ml'} }
	   	   	 map  { [(split(/<>/))[0,4]] } @alllines if $F{'ml'};
	($urlcheck)  = grep { $_->[0] ne $F{'id'} }
	   	   	 grep { $_->[1] && $_->[1] eq $F{'ul'} }
	   	   	 map  { [(split(/<>/))[0,5]] } @alllines if $F{'ul'};

	if ($mailcheck) { &error("此電子郵件已經有人使用") }
	if ($urlcheck)  { &error("此個人網頁已經有人使用") }

	$intro =  $F{'in'};
	$mail =  $F{'ml'};
	$url =  $F{'ul'};
	$intro =~ s/<br>//g;
	$F{'uid'} = $id;
	&set_me;
	&uprofile;
}

1;