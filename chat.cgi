sub chat{
print <<chat
<script>function check(key_msg){document.form.edc.value=key_msg}</script>
<br><table width="100%" align=center bgcolor="#e9e2ce" border="1" bordercolor=$bdcol cellspacing=0><tr><td align=center>Chat Room</td></tr><tr><td>
<FORM NAME="form" METHOD="POST" ACTION="bbs/say.cgi" TARGET="i" onsubmit="check(keymsg.value);keymsg.value=''">
<iframe src="bbs/say.cgi" width="100%" height="150" name="i" frameborder="0"></iframe><BR>
<INPUT TYPE="hidden" NAME="edn"  SIZE="8" CLASS="input" VALUE=$name>
<INPUT TYPE="hidden" NAME="edid"  SIZE="8" CLASS="input" VALUE=$id><BR>
<INPUT NAME="keymsg" TYPE="text" SIZE="33" CLASS="input">
<INPUT type="submit" value="送出" class=button>
<INPUT type="button" value="更新" onclick="edc.value='';submit()" class=button>
<INPUT NAME="edc" TYPE="hidden" SIZE="33" CLASS="input">
</FORM></td></tr></table>
chat
}

1;