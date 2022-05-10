#!/usr/bin/perl
# ↑サーバに合わせて変更

# #############################################################
# ネット航海時代
# Copyright (C) 2002 コスミー, All rights reserved.
# E-Mail : impulse@kun.ne.jp
# Web : http://www.kosumi.vxx.jp/
# 本スクリプトはフリーウェアです。
# 利用する方は次のURL:http://www.kosumi.vxx.jp/rules.htm
# に記載された利用規定に同意したものと見なします。
# 著作権はコスミーが保有しますが、
# 本スクリプトの一部においてMissing Link様の保有する「PeoPle」より
# 引用させていただいております。
# 引用部分についての著作権等はMissing LinkのSho様に帰属いたしますので、
# 詳しくはReadMeをご覧下さい。(Missing Link:http://www.area-s.com/)
# 本スクリプトを利用した事によるいかなる損害も作者(コスミー)は一切の責任を負いません。
# 質問等はサポート掲示板へ(http://www.kosumi.vxx.jp/support.htm)
# #############################################################

# 以下設定
use Nfile;
$g_basedat	= 'base.dat';	# 交易品基本價格
$yarddat	= 'item.dat';	# 船價格與販賣港
$adfiles	= 'a_list.dat';	# 冒險情報列表

$trade_lower	= 0.5;		# 物價的下限(0.5以上)
$trade_upper	= 1.5;		# 物價的上限(1.5以下)
$flac       	= 0.00000003;	# 1G影響的變動量
$sell_rate  	= 0.6;		# 賣出時的價格(預設是買值 ×0.6)
$cf		= 213;		# 交易品的變動係數(要是正好整數,0不變動)
$cycle		= 7;		# 物價的變動周期(日)
$pay		= 100;		# 水手一人基本購入價格
$f_price	= 10;		# 食物一單位基本購入價格
$time_scale	= 250;		# 移動時間(推薦200～500)
$waste		= 0.001;	# 水夫一人一秒所消耗食物量
$cont		= 15;		# 連續戰鬥限制（單位：分）
$same		= 0.5;		# 同一對手限制（1日=1）
$stop		= 3;		# 係留時間（小時）
$robmoney	= 5;		# 戰鬥奪取對手資金的百分之幾(%)
$b_flac		= 100;		# 町襲擊時的亂數幅度
$atk_limit	= 200;		# 戰鬥力限界
$cmd_limit	= 150;		# 指揮力限界
$nav_limit	= 200;		# 航海力限界
$newcity	= 1000000;	# 建立城鎮所需金額
$poten		= 10000;	# 城鎮初期的HP
$r_fee		= 50;		# 城鎮的修理費用(修復1HP所需花費)
$atkfee		= 1000000;	# 使城鎮陷落的必要值(同城鎮HP)
$cityatked 	= 1000;		# 進行破壞工作的傷害
$citypwr	= 400;		# 城鎮的基本攻擊力
$cl_limit	= 7;		# 城鎮存放的可能數(交易品)
$cs_limit	= 7;		# 城鎮存放的可能數(船)
$rookie		= 30;		# ルーキー数
$retry		= 1;		# 再登錄限制(時)(防止無限制重複登錄)

$x_rev	= 85;			# 地圖的(0,0)的值(象素)
$y_rev	= 73;
$map_x	= 0.556;		# x方向の１°当たりのピクセル数、(地図の幅)/360
$map_y	= 0.733;		# (地圖的縱)/180
$map_height = 132;		# 地図的縦
$map_width = 200;		# 地図的幅
$move_ship = "move.gif";	# 移動用船圖像
$move_width = 400;		# 移動距離（象素）

# 財寶特殊効果
@shield = ('サットン＝フーの兜','王族の剣','水晶のどくろ');	# 被襲擊時吸收敵方攻擊力
@atkup = ('シペ＝トテク神の仮面');							# 攻擊回合數增加
@gard = ('キングシンボル');									# 財寶保護
@vanish = ('太陽の石');										# 戰鬥回避
@save = ('ジョン王の酒杯');									# 食物消費低減

# ↓各ポイントでのメッセージ('海上','港','交易品屋','造船所','酒場','町','襲撃')
@ms = ( '' , '「要小心海賊呀！」' , '「交易的基本就是低買高賣」' , '「資金要靈活運用」' , '「酒場是港的情報交換處」' , '' , 'Good luck !');

#require 'jcode.pl';
require 'setting.cgi';		# セッティングファイル
require 'sys.cgi';

# 設定ここまで

# ###################################################################
&error("請於[setting.cgi]更改用戶目錄名") if $usrdir eq 'userdir';
&decode;
if ($F{'id'} =~ /\W/) { &error('不正な入力です') }
if (!$F{'mode'})      { require 'rank.cgi'; &start_view }
else                  {
				if	(($F{'mode'} eq 'trade_sell') || ($F{'mode'} eq 'trade_buy')) { require 'trade.cgi' }
				elsif ($F{'mode'} eq 'move') { require 'move.cgi' }
				elsif (($F{'mode'} eq 'bar_trade') || ($F{'mode'} eq 'adven')) { require 'bar.cgi' }
				elsif (($F{'mode'} eq 'rep_ship') || ($F{'mode'} eq 'buy_ship') || ($F{'mode'} eq 'sell_ship')) { require 'yard.cgi' }	
				elsif ($F{'mode'} eq 'battle') { require 'battle.cgi' }
				elsif ($F{'mode'} =~ /city/) { require 'city.cgi' }
				elsif ($F{'mode'} =~ /ctrade/) { require 'ctrade.cgi' }
				elsif ($F{'mode'} =~ /cadmin/) { require 'cadmin.cgi' }
				elsif ($F{'mode'} eq 'cbattle_atk')	{ require 'cbattle.cgi' }
	&{$F{'mode'}}   }
exit;
# ###################################################################

# Sub Ships #
sub ships {
	if ( $#ship_ind < 0 && $money < 2000 ) {
		print qq|<form method=$method action=$seacgi>無任何船隻<br>資金低於2000。<br>是否要帳號自殺？<br>\n|;
		print qq|<input type=hidden name=mode value="restart">\n|;
		&id_ps;
		&submit_button;
		print qq|</form>\n|;
		return
	}
	for ($i=0; $i <= 16; $i++){
		if(!$ship[$i][0]){ $ship[$i][0] = $damgif; }
	}
print <<SHIP_TABLE;
<table border=0 cellspacing=0 cellpadding=0 background="$img/$seaimg" cols=5>
<tr>
<td height=40 width=40 align=center valign=center><br></td>
<td height=40 width=40 align=center valign=center><br></td>
<td height=40 width=40 align=center valign=center><img src="$img/$ship[11][0]" alt="$ship[11][4](HP$ship[11][2])"></td>
<td height=40 width=40 align=center valign=center><img src="$img/$ship[15][0]" alt="$ship[15][4](HP$ship[15][2])"></td>
<td height=40 width=40 align=center valign=center><br></td>
</tr>
<tr>
<td height=40 width=40 align=center valign=center><br></td>
<td height=40 width=40 align=center valign=center><img src="$img/$ship[9][0]" alt="$ship[9][4](HP$ship[9][2])"></td>
<td height=40 width=40 align=center valign=center><img src="$img/$ship[3][0]" alt="$ship[3][4](HP$ship[3][2])"></td>
<td height=40 width=40 align=center valign=center><img src="$img/$ship[7][0]" alt="$ship[7][4](HP$ship[7][2])"></td>
<td height=40 width=40 align=center valign=center><img src="$img/$ship[13][0]" alt="$ship[13][4](HP$ship[13][2])"></td>
</tr>
<tr>
<td height=40 width=40 align=center valign=center><img src="$img/$ship[6][0]" alt="$ship[6][4](HP$ship[6][2])"></td>
<td height=40 width=40 align=center valign=center><img src="$img/$ship[2][0]" alt="$ship[2][4](HP$ship[2][2])"></td>
<td height=40 width=40 align=center valign=center><img src="$img/$ship[0][0]" alt="$ship[0][4](HP$ship[0][2])"></td>
<td height=40 width=40 align=center valign=center><img src="$img/$ship[1][0]" alt="$ship[1][4](HP$ship[1][2])"></td>
<td height=40 width=40 align=center valign=center><img src="$img/$ship[5][0]" alt="$ship[5][4](HP$ship[5][2])"></td>
</tr>
<tr>
<td height=40 width=40 align=center valign=center><br></td>
<td height=40 width=40 align=center valign=center><img src="$img/$ship[10][0]" alt="$ship[10][4](HP$ship[10][2])"></td>
<td height=40 width=40 align=center valign=center><img src="$img/$ship[4][0]" alt="$ship[4][4](HP$ship[4][2])"></td>
<td height=40 width=40 align=center valign=center><img src="$img/$ship[8][0]" alt="$ship[8][4](HP$ship[8][2])"></td>
<td height=40 width=40 align=center valign=center><img src="$img/$ship[14][0]" alt="$ship[14][4](HP$ship[14][2])"></td>
</tr>
<tr>
<td height=40 width=40 align=center valign=center><br></td>
<td height=40 width=40 align=center valign=center><br></td>
<td height=40 width=40 align=center valign=center><img src="$img/$ship[12][0]" alt="$ship[12][4](HP$ship[12][2])"></td>
<td height=40 width=40 align=center valign=center><img src="$img/$ship[16][0]" alt="$ship[16][4](HP$ship[16][2])"></td>
<td height=40 width=40 align=center valign=center><br></td>
</tr>
</table>
SHIP_TABLE
}

# Sub Status #
sub status {
	&fleet;
	&load_data;
	$rest = $total - $total_load - $food - $sailor;
	($load_detail =$load) =~ s/△/　/g;
	($item_detail =$item_line) =~ s/,/　/g;
	$load_detail .= '<br>';
	$item_detail .= '<br>';
	my $now_price = sprintf "%3.2f" , $p_price*100;
	my $avoid = int($cmd / 3);
	$message .= $record;
	$record = '';
	$message = '<br>' if !$message;
	my $i_up = 1 + $t_item*0.01;
	my $alv = &level($aexp*$i_up);
	my $plv = &level($pexp*$i_up);
	my $tlv = &level($texp*$i_up);
	$on_clickf = qq|onClick="return opWin('$listcgi?mode=player_list','win6')"|;
	$on_clickh = qq|onClick="return opWin('$listcgi?mode=history&id=$id&ps=$F{'ps'}','win6')"|;
	$on_clicke = qq|onClick="return opWin('$listcgi?mode=event_look','win6')"|;
	$on_clickm = qq|onClick="return opWin('$listcgi?mode=mail_form&id=$id&ps=$F{'ps'}','win6')"|;
	$on_clicki = qq|onClick="return opWin('$listcgi?mode=introduce&id=$id&ps=$F{'ps'}','win6')"|;
print <<STATUS_TABLE;
<table border=1 width="100%" bgcolor=$t_bgcol bordercolor=$bdcol cellspacing=0>
<tr>
<td colspan=2 align=center>狀態</td>
</tr><tr>
<td width=80 align=center>艦隊</td><td>$name艦隊</td>
</tr><tr>
<td width=80 align=center>貨倉容量</td><td>全部：$total　現有：$total_load　剩餘：$rest</td>
</tr><tr>
<td width=80 align=center>貨物詳細</td><td>$load_detail</td>
</tr><tr>
<td width=80 align=center>食物</td><td>$food</td>
</tr><tr>
<td width=80 align=center>資金</td><td>$money G</td>
</tr><tr>
<td width=80 align=center>水手</td><td>$sailor人</td>
</tr><tr>
<td width=80 align=center>Lv</td><td>冒險Lv：$alv　海賊Lv：$plv　商人Lv：$tlv</td>
</tr><tr>
<td width=80 align=center>戰鬥力</td><td>$atk</td>
</tr><tr>
<td width=80 align=center>回避率</td><td>$avoid ％ (指揮力：$cmd)</td>
</tr><tr>
<td width=80 align=center>速度</td><td>$vector 節 (航海力：$nav)</td>
</tr><tr>
<td width=80 align=center>現在地</td><td>$p_name(物價：$now_price％)</td>
</tr><tr>
<td width=80 align=center>財寶</td><td>$item_detail</td>
</tr><tr>
<td width=80 align=center>名聲</td><td>冒險：$adven<br>海賊：$piracy<br>商人：$trade</td>
</tr><tr>
<td colspan=2 align=center>$message</td>
</tr><tr>
<td colspan=2 align=center>
STATUS_TABLE
	print qq|<a href="$listcgi?mode=player_list" $on_clickf target=_blank>[艦隊]</a>　\n|;
	print qq|<a href="$listcgi?mode=history&id=$id&ps=$F{'ps'}" $on_clickh target=_blank>[履歴]</a>　\n|;
	print qq|<a href="$listcgi?mode=event_look" $on_clicke target=_blank>[事件]</a>　\n|;
	print qq|<a href="$listcgi?mode=mail_form&id=$id&ps=$F{'ps'}" $on_clickm target=_blank>[信件]</a>　\n|;
	print qq|<a href="$listcgi?mode=introduce&id=$id&ps=$F{'ps'}" $on_clicki target=_blank>[Profile]</a>\n|;
	print qq|</td></tr></table>\n|;
}

# Sub Play #
sub play {
	&get_me($F{'id'});
	&set_cookie if $F{'mode'} eq 'play';
	&get_host;
	&get_port($area,$port) if $port;
	&get_port($area,$area) if !$port;
	&ship_data;
	$last = time;
	&t_check;
	&sink;
	&header;
	&quest;
	my ($y,$x) = split(/,/,$p_locate);
	$x = int($x * $map_x + $x_rev + 0.5); #0.5は四捨五入
	$y = int($y_rev - $y * $map_y + 0.5);
	print qq|<center><H2><font color=#4169e1>$title</font></H2>\n|;
	print qq|<table width="90%"><tr align=center valign=top><td>\n|;
	print qq|<table width=$map_width><tr><td height=$map_height background="$img/worldmap.gif" align=left valign=top>\n|;
	print qq|<div><span style="position:relative; top:$y; left:$x;">\n|;
	print qq|<img src="$img/pointer.gif"></span></div></td></tr><tr><td>\n|;
	&ships;
	&dis_tactics if $tactics != 4 || $moved < $last;
	print qq|</td></tr></table><td width="40%">\n|;
	&status;
	&move_point if $last > $moved; # $port &&  $portがあれば（港にいれば）、港内移動表示
	print qq|</td><td width="30%">\n|;
	if($_[0]) {print qq|$_[0]\n<form method=$method action=$seacgi><input type=hidden name="mode" value="play">|; &id_ps; &submit_button; print qq|</form>|;}
	elsif ($point==1 && $last >= $moved )	{ require 'move.cgi'; &move_list }
	elsif ($point==2) { require 'trade.cgi'; &trade_dis('購入',$trade_line); &trade_dis('賣出',$load) if $load; }
	elsif ($point==3) { require 'yard.cgi'; &shipyard }
	elsif ($point==4) { require 'bar.cgi'; &bar_meet }
	elsif ($point==5) { require 'city.cgi'; &city_top }
	elsif ($point==6) { require 'battle.cgi'; &enemy }
	elsif ($last < $moved) { &moving }
	print qq|</td></tr></table></center>\n|;
	&home_button;
	&footer;
	&set_me;exit;
}

# Sub Start View #
sub start_view {
	print qq|Set-Cookie: T$cookname=check;\n|;
	&header;
	print qq|<center><H2><font color=#4169e1>$title</font></H2><br>\n|;
	&get_cookie;
	&form_table('up','40',0);
	print qq|<a href="$newcgi">創立帳戶</a><br><a href="manual.htm" target=_blank>玩法說明</a></td></tr><tr><td align=center>|;
	$on_click = qq|onClick="return opWin('$listcgi?mode=id_list','win4')"|;
	print qq|ID 【<a href=$listcgi?mode=id_list $on_click target=_blank>ID LIST</a>】<br>\n|;
	print qq|<input type=text name=id class=text size=$stx_wth value="$c_id">\n|;
	print qq|</td></tr><tr><td align=center>\n|;
	print qq|密碼<br>\n|;
	print qq|<input type=password name=ps class=text size=$stx_wth value="$c_ps">\n|;
	print qq|</td></tr><tr><td align=right>\n|;
	&submit_button;
	print qq|<input type=hidden name=mode value="play"></center>\n|;
	&form_table('down');
	&ranking;
	&home_button;
	&footer;
}

# Sub Get Port #第一引数＝$area、第二引数＝$port(or $area)、要変更
sub get_port {
	if ($_[0] =~ /\W/) { &error('不正です') }
	my $AreaFile = new Nfile("$datadir/$_[0]\.dat",'read');
	@arealine = $AreaFile->read;
	($port_line) = grep {($num) = split(/<>/,$_); $num == $_[1];} @arealine;
	if (!$port_line) { &error("港口資料取得錯誤"); exit }
	($p_num,$p_name,$p_locate,$trade_line,$p_price) = split(/<>/,$port_line);
}

# Sub Trade Check #
sub trade_check {
	&ship_data;
	&fleet;
	&load_data;
	$rest = $total - $total_load - $food - $sailor;
	if ($F{'quan'} =~ /[^0-9]/) { &play("數量輸入錯誤");exit }
	if (!$F{'quan'}) { &play("未輸入數量");exit }
	if ($money < ($price * $F{'quan'}) ) { &play("所持金不足");exit }
	if ($rest < $F{'quan'} ) { &play("剩餘的容量不足");exit }
}

# Sub Sell Check #
sub sell_check {
	if ($F{'quan'} =~ /[^0-9]/) { &play("數量輸入錯誤");exit }
	if (!$F{'quan'}) { &play("未輸入數量");exit }
}


# Sub Quest #
sub quest {
	if (!$quest_flag) { return }
	my ($qarea,$qport,$qpoint,$guide,$prog,$get) = split(/,/,$quest_line);
	if ( $port == $qport && $area == $qarea && $point == $qpoint ) {
		&msg("$guide");
		&add_record("$guide");
		$prog++;
		my $ConFile = new Nfile("$datadir/$quest_flag",'read');
		@content = $ConFile->read;
		$quest_line = $content[$prog];
		chomp($quest_line);
		undef @content;
		if (!$quest_line) {
			if ($end_quest !~ /$quest_flag/) {
				$adven += $prog * 5000;
				$aexp += $prog * 5000;
				$end_quest .= "$quest_flag,";
				if ($get) {
					my @item_check = split(/,/,$item_line);
					foreach (@item_check) { if ($_ eq $get) { $find = 1; last } }
					if (!$find) {
						$item_line = join(',' , @item_check , $get);
						&add_record("獲得 $get");
						&msg("得到了$get")
					}
				}
			}
			$quest_flag = '';
			return
		}
		my @item_check = split(/,/,$quest_line);
		if ( $#item_check >= 4 ) {
			splice(@item_check , 4 , 0 , $prog);
			$quest_line = join(',' , @item_check);
			return
		}			
		$quest_line .= ",$prog"
	}
}

# Sub Add Record #
sub add_record {
	&get_date(time) if !$date;
	if ($_[1] && $_[0]) {
		$words =  "[$date] $_[0]\n";
		pop (@ulines) if @ulines >= $def_om;
		unshift (@ulines,$words);
	}
	elsif ($_[0]) {
		$words =  "[$date] $_[0]\n";
		pop (@ilines) if @ilines >= $def_om;
		unshift (@ilines,$words);
	}
}

# Sub Message #
sub msg {
	return if !$_[0];
	$message = "" if $message eq '<br>';
	$message .= "<br>" if $message;
	$message .= "$_[0]\n";
}

# Sub Get Date #
sub get_date {
	($sec,$min,$hour,$day,$month,$year) = localtime($_[0]);
	$year += 1900;
	$month++;
	$date   = sprintf("%04d\/%02d\/%02d",$year,$month,$day);
}

# Sub Get Ship Data # $ship[$_][0]=画像名、[1]=積載量、[2]=HP、[3]=速度、[4]=名前
sub ship_data {
	undef @ship;
	for (0 .. $#ship_ind) {
		@{$ship[$_]} = split(/,/,$ship_ind[$_])
	}
}

# Sub Fleet Status #
sub fleet {
	$total = $vector = 0;
	for(0 .. $#ship){
	  $total += $ship[$_][1];
	  $vector += $ship[$_][3]
	}
	$vector = @ship_ind > 0 ? int( ($vector + ($nav * 0.1)) / @ship_ind ) : 0;
	$vector = ($vector * int((100 + &level($aexp*(1 + $t_item*0.01)))/10))/10;
}

# Sub Total Load #
sub load_data {
	$total_load = 0;
	my @load_ind = split(/△/,$load);
	foreach (@load_ind) {
		($load_name,$load_quan) = split(/,/,$_);
		$total_load += $load_quan;
	}
}

# Sub Moving #
sub moving {
	$take = $moved - time;
	$take = 0 if $take < 0;
	$amount = $take == 0 ? $move_width : 1;
	$delay = ($take * 1000) / $move_width ;
print qq|<center><table width="100%"><tr><td align=center><form method=$method action=$seacgi>★到達|;
print qq|<input type=hidden name=mode value="play">\n|;
&id_ps;
&submit_button;
print <<SHIP_MOVE;
</form></td></tr><tr>
<td background="$img/$seaimg">
<marquee behavior=slide loop="1" height=$move_width direction=up scrollamount=$amount scrolldelay=$delay truespeed>
<center><img src="$img/$move_ship"></center>
</marquee>
</td></tr></table>
<FORM action="./" method="post" name="count">
	剩餘時間<INPUT NAME="down" SIZE="10">
<SCRIPT LANGUAGE="JavaScript">
<!---
xx = $take;
function down() {
if (xx < 0)xx = 0;
sec = xx % 60;
min = ((xx - sec) / 60) % 60;
hor = (xx - min * 60 - sec) / 3600;
if (hor < 10)hor = "0" + hor;
if (min < 10)min = "0" + min;
if (sec < 10)sec = "0" + sec;
xx--;
document.count.down.value = hor+":"+min+":"+sec;
setTimeout('down()', 1000);
}
down();
//end --->
</SCRIPT>
</FORM>
</center>
SHIP_MOVE
}

# Sub Sink #
sub sink {
	if (!$port && $#ship_ind < 0) {
		&set_cookie('del');
		&header;
		print qq|<center><font size=5 color=#4169e1>$title</font><br><br><br>\n|;
		print qq|<font size=6 color=#FF0000>\n|;
		print qq|遊戲結束！<br>$name艦隊於海上全滅！<br>成為海裡的碎藻‧‧‧\n|;
		print qq|</font></center>\n|;
		&home_button;
		&footer;
		unlink("$usrdir/$id\.dat");
		exit
	}
}

# Sub Submit Button #
sub submit_button {
	print qq|<input type=submit value="$sub_lbl" class=button>\n|;
}

# Sub Display Tactics #
sub dis_tactics {
	my(@t_type)=('好戰','適度','回避');
	&form_table('up','100%',1);
	print qq|戰術　　|;
	&id_ps;
	&submit_button;
	&reload;
	print qq|</td></tr><tr><td align=center valign=center>\n|;
	for($i=0;$i<3;$i++) {
		$checked = $i == $tactics  ? ' checked' : '';
		print qq|<input type=radio name=tactics value="$i"$checked>$t_type[$i] \n|;
	}
	if ($#ship_ind <= 1) {
		$checked = $tactics == 3  ? ' checked' : '';
		print qq|<br><input type=radio name=tactics value="3"$checked>投降(全名聲歸０)\n|;
	}
	if ($port && $moved < $last) {
		$checked = $tactics == 4  ? ' checked' : '';
		print qq|<br><input type=radio name=tactics value="4"$checked>停靠港口($stop小時)\n|;
	}
	print qq|<input type=hidden name=mode value="ch_tac">\n|;
	&form_table('down');
}

# Sub Change Tactics #
sub ch_tac {
	&get_me($F{'id'});
	if ($action ne $F{'reload'}) { &play; exit }
	$tactics = $F{'tactics'};
	if ($tactics == 4) { $moved = time + ($stop * 3600); $point = 1 }
	$action = '';
	&play;
}

# Sub Tactics Check #
sub t_check {
	if (($tactics == 3 && $#ship_ind > 1) || ($tactics == 4 && $moved < $last)) { $tactics = 1 }
	if ($tactics == 3) {
		$piracy = 0 if $piracy > 0;
		$adven = 0 if $adven > 0;
		$trade = 0 if $trade > 0;
	}
}

# Sub Move Point #
sub move_point {
	my(@in_port)=('港口','交易','造船','酒場','城鎮','襲撃'); # $point 海上＝0、港＝1、交易＝2、造船＝3、酒場＝4、町＝5、襲撃＝6
	print qq|<br>\n|;
	&form_table('up','100%',1);
	print qq|港內移動　　| if $port;
	print qq|行動　　| if !$port;
	&submit_button;
	print qq|</td></tr><tr><td align=center>\n|;
	for($i=1;$i<7;$i++) {
		$checked = $i == $point  ? ' checked' : '';
		print qq|<input type=radio name=point value="$i"$checked>$in_port[$i-1] \n|;
		$i += 4 if !$port;
	}
	&id_ps;
	print qq|<input type=hidden name=mode value="ch_point">\n|;
		&form_table('down');
#插入聊天室
require 'chat.cgi';
&chat;
}

# Sub Change Point #
sub ch_point {
	&get_me($F{'id'});
	if (time < $moved) { &play; return }
	#Ver2.73
	if ($F{'point'} < 0 || 6 < $F{'point'}) { &play; return; }
	if (!$port && $F{'point'} != 1 && $F{'point'} != 6) { &play; return; }
	##
	$point = $F{'point'};
	&msg("$ms[$F{'point'}]");
	&play;
}

# Sub Restart #
sub restart {
	require 'rank.cgi';
	&get_me($F{'id'},'read');
	unlink("$usrdir\/$id\.dat");
	&set_cookie('del');
	&start_view;
	exit;
}

# Sub Table #第一＝上or下、第二＝幅、第三＝境界
sub form_table {
if($_[0] eq 'up') {
print <<TAB;
	<center><form method=$method action=$seacgi>
	<table width="$_[1]" border="$_[2]" bgcolor=$t_bgcol bordercolor=$bdcol cellspacing=0>
	<tr><td align=center>
TAB
}
if($_[0] eq 'down') {
print <<TAB;
	</td></tr>
	</table></form>
	</center>
TAB
}
}

# Sub Return Button #
sub return_button {
	print qq|<center><form method=$method action=$seacgi><input type="button" value="返回" onClick="history.back()"></form></center>\n|;
}

# Sub Home Button #
sub home_button {
	if (!$def_ho) { return }
	print qq|<center><a href=$hom_url target=$hom_tgt>$hom_lbl</a><br></center>\n|;
}

# Sub ID & Password #
sub id_ps {
	print qq|<input type=hidden name=id value="$F{'id'}">\n|;
	print qq|<input type=hidden name=ps value="$F{'ps'}">\n|;
}

# Sub Reload #
sub reload {
	$action = rand(1000) if !$reloadflag;
	print qq|<input type=hidden name=reload value="$action">\n|;
	$reloadflag = 1;
}

# Sub Level #
sub level {
	return int(5.9 * log($_[0] + 4792) - 50)
}

# Sub Error #
sub error {
	&unlock if $locked;
	if (!$headflag) { &header }
print <<ERR;
<center>
<hr width=80%>
<B><font color=#FF0000>$_[0]</font></B>
<hr width=80%>
</center>
ERR
	&return_button if !$def_rb;
	&footer('no');
	exit;
}

# Sub Get Cookie #
sub get_cookie { 
	@pairs = split(/\;/,$ENV{'HTTP_COOKIE'});
	foreach $pair (@pairs) {
		my($name, $value) = split(/\=/, $pair);
		$name =~ s/ //g;
		$DUMMY{$name} = $value;
	}
	@pairs = split(/\,/,$DUMMY{$cookname});
	foreach $pair (@pairs) {
		my($name, $value) = split(/\:/, $pair);
		$COOKIE{$name} = $value;
	}
	$c_id = $COOKIE{'id'};
	$c_ps = $COOKIE{'ps'}
}

# Sub Set Cookie #
sub set_cookie {
	# クッキーは未更新削除期間有効
	($secg,$ming,$hourg,$mdayg,$mong,$yearg,$wdayg,$ydayg,$isdstg) = gmtime(time + $def_dead*24*60*60);
	($secg,$ming,$hourg,$mdayg,$mong,$yearg,$wdayg,$ydayg,$isdstg) = gmtime(time + $retry*60*60) if $_[0] eq 'del';
	$yearg += 1900;
	if ($secg  < 10) { $secg  = "0$secg";  }
	if ($ming  < 10) { $ming  = "0$ming";  }
	if ($hourg < 10) { $hourg = "0$hourg"; }
	if ($mdayg < 10) { $mdayg = "0$mdayg"; }
	$month = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')[$mong];
	$youbi = ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday')[$wdayg];
	$date_gmt = "$youbi, $mdayg\-$month\-$yearg $hourg:$ming:$secg GMT";
	$cook = "id\:$F{'id'}\,ps\:$F{'ps'}";
	print "Set-Cookie: $cookname=$cook; expires=$date_gmt\n";
}

# Sub Decode #
sub decode {
	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
		@pairs = split(/&/, $buffer);
	} else {
		@pairs = split(/&/, $ENV{'QUERY_STRING'});
		if($#pairs >= 0 && $method eq 'POST') { &error("不正なエラーです"); }
	}

	foreach $pair (@pairs) {
		($name, $value) = split(/=/, $pair);
		$name =~ tr/+/ /;
		$name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

#		&jcode'convert(*name,'sjis');
#		&jcode'convert(*value,'sjis');

		$value =~ s/</&lt;/g;
		$value =~ s/>/&gt;/g;
		$value =~ s/\,/，/g;
		$value =~ s/\r\n/<br>/g;
		$value =~ s/\r/<br>/g;
		$value =~ s/\n/<br>/g;

		$F{$name} = $value;
	}
}

# Sub Get Host #
sub get_host {
	$host = $ENV{'REMOTE_HOST'};
	$ad = $ENV{'REMOTE_ADDR'};
	if ($get_remotehost) {
		if ($host eq "" || $host eq "$ad") {
			$host = gethostbyaddr(pack("C4",split(/\./,$ad)),2);
		}
	}
	if ($host eq "") { $host = $ad }
}
