package output;
#output:出力パッケージ

# 外部から呼び出されるサブルーチン

# ヘッダ
sub topheader{
	print <<END;
Content-type: text/html; charset=UTF-8

<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8" />
<meta http-equiv="content-type" content="text/html;" />
<meta http-equiv="content-style-type" content="text/css;" />
<meta http-equiv="content-script-type" content="text/javascript;" />
<title>$ini::bbsName</title>
<link rel="stylesheet" type="text/css" href="style.css" />
<script type="text/javascript" src="script.js"></script>
</head>
<body>
<header id="header">
<hgroup>
<h1>$ini::bbsName</h1>
<h2>$ini::bbsDescription</h2>
</hgroup>
END
	navi();
	print <<END;
</header>
END
}

# スレッド一覧のヘッダ
sub threads_header{
	my($page,$threads_number)=@_;


	print <<END;
<article id="threads">
<h2>スレッド一覧</h2>
END
	if($page>=0){
		threads_navi($page,$threads_number,'up');
	}
	print <<END;
<table>
<tr>
<th>No</th><th>題名</th><th>レス数</th><th>作成</th><th>最終更新</th>
</tr>

END
}
# スレッド一覧のページ
sub threads_navi{
	my($page,$threads_number,$mode)=@_;
	print <<END;
<nav class="pager $mode">
END
	my($i);
	for($i=0;$i<$threads_number/$ini::page_threads;$i++){

		print "<a";
		if($i*$ini::page_threads==$page){
			print " class='current'";
		}
		print " href='index.cgi?page=".($i*$ini::page_threads)."'>$i</a>\n";
	}
	print <<END;
</nav>
END
}
# 1つのスレッド
sub threads_thread{
	my($data)=@_;
	my($number)=$data->{'number'};
	my($res)=$data->{'resnum'}-1;#レス数は投稿の数より1少ない
	my($href);
	if($::Global_admin_mode==1){
		$href="admin.cgi?mode=administer&number=$number&password=$ini::password";
	}else{
		$href="index.cgi?mode=view&number=$number";
	}
	print <<END;
<tr>
<td class="number">$number</td><td><a href="$href">$data->{'title'}</a></td>
<td class="number">$res</td><td>$data->{'maker'}<br><time>$data->{'mdate'}</time></td>
<td>$data->{'lastreply'}<br><time>$data->{'date'}</time></td>
</tr>
END
}
# スレッド一覧のフッタ
sub threads_footer{
	my($page,$threads_number)=@_;
	print <<END;
</table>
END
	if($page>=0){
		threads_navi($page,$threads_number,'down');
	}
	print <<END;
</article>
END
}

#フッタ
sub footer{
	# 広告は削除しないようにして下さい。
	my($admin)="admin.cgi";
	if($::Global_admin_mode==1){
		$admin.="?password=$ini::password&mode=login";
	}
	print <<END;
<footer id="footer">
<p><a href="http://github.com/noty2008">noty2008</a>作のらくちん掲示板 1.0</p>
<p style="text-align:right">[<a href="$admin">管理者ページ</a>]</p>
</footer>
</body>
</html>
END
}
#============================================================

# 記事のヘッダ
sub view_header{
	my($title)=(shift)->{'title'};
	print <<END;
Content-type: text/html; charset=UTF-8

<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8" />
<title>$ini::bbsName - $title</title>
<link rel="stylesheet" type="text/css" href="style.css" />
<script type="text/javascript" src="script.js"></script>
</head>
<body>
<header id="header">
<hgroup>
<h1>$ini::bbsName</h1>
<h2>$ini::bbsDescription</h2>
</hgroup>
END
	navi();
	print <<END;
</header>
END
	if($::Global_admin_mode==1){
		print <<END;
<p><a href="admin.cgi?mode=administer&password=$ini::password">戻る</a></p>
END
	}
	print <<END;
<article id="view">
<h2>$title</h2>
END
}
# 記事のフッタ
sub view_footer{
	print <<END;
</article>
END
}
# レス1つ
sub res{
	my($data,$words)=@_;
	my($cl) = $data->{'num'}==1 ? "res top" : "res";

	my($title,$name,$message,$date)=($data->{'title'},$data->{'name'},$data->{'message'},$data->{'date'});
	if($words){
		foreach(@$words){
			my($p)=data::saferegexp($_);

			$title =~ s/((?:$p)+)/<mark>$1<\/mark>/g;
			$name =~ s/((?:$p)+)/<mark>$1<\/mark>/g;
			$message =~ s/((?:$p)+)/<mark>$1<\/mark>/g;

		}
	}
	my($ddd)="";
	if($::Global_admin_mode==1){
		$date=~ s/;.*//;
		$ddd=" IPアドレス:<b>$data->{'ip'}</b>";
	}
	my($date2)=$date;
	$date2 =~ s/^\(編集\d*\)//;

	if(($data->{'flag'}==1)||($data->{'flag'}==2)){
		$cl .= " deleted";
	}
	print <<END;
<article class="$cl">
<header>
<h3>$title</h3>
<p>$data->{'num'}. <b class="name">$name</b> <time datetime="$date2" pubdate>$date</time>$ddd</p>
</header>
$message
</article>
END
}
# 返信フォーム
sub view_reply{
	my($number,$data,$cgi)=@_;
	my($name,$password)=($cgi->cookie("bbs_name"), $cgi->cookie("bbs_password"));
	replydata_form({
		'name' => $name,
		'password' => $password,
		'title' => $data->{'title'},
		'message' => ""
	},"返信フォーム","reply",<<END);
<input type="hidden" name="number" value="$number" />
<input type="hidden" name="mode" value="reply" />
END
}
sub replydata_form{
	my($initdata,$formtitle,$formid,$option)=@_;
	my($name,$password,$title,$message);
	if($initdata){
		($name,$password,$title,$message) =
		($initdata->{'name'},$initdata->{'password'},$initdata->{'title'},$initdata->{'message'});
	}
	print <<END;
<article id="$formid" class="form">
<h2>$formtitle</h2>
<form action="index.cgi" method="post" id="replyform">
<p>$option<b>名前:</b>
<input type="text" size="30" name="name" value="$name" />
</p>
<p>
<b>題名:</b>
<input type="text" size="50" name="title" value="$title" />
</p>
<p>
<b>内容:</b>
<textarea cols="50" rows="6" name="message">
$message</textarea>
</p>
<p>
<b>パスワード:</b>
<input type="password" name="password" size="15" value="$password" />
<input type="submit" value="送信" /></p>
<p id="error_message"></p>
</form>
</article>
<script type="text/javascript">
var noPassword = $ini::noPassword;
var noName = "$ini::noName";

var form = document.getElementById('replyform');
if(form){
	if(form.addEventListener){
		form.addEventListener('submit',check_input,false);
	}else if(form.attachEvent){
		form.attachEvent('onsubmit',check_input);
	}
}
</script>
END
}
# ページャー
sub view_navi{
	my($number,$page,$res_number,$mode)=@_;
	print <<END;
<nav class="pager $mode">
END
	my($i);
	for($i=0;$i<$res_number/$ini::page_res;$i++){

		print "<a";
		if($i*$ini::page_res==$page){
			print " class='current'";
		}
		print " href='index.cgi?mode=view&number=$number&page=".($i*$ini::page_res)."'>$i</a>\n";
	}
	print <<END;
</nav>
END
}
# 削除フォーム
sub view_delete{
	my($number)=shift;
	my($adminstr)="";
	if($::Global_admin_mode==1){
		$adminstr = <<END;
<input type="hidden" name="adminmode" value="adminmode" />
END
	}
	print <<END;
<article id="delete" class="form">
<h2>記事の編集・削除</h2>
<form action="index.cgi" method="post">
<p><input type="hidden" name="number" value="$number" />$adminstr
<b>レス番号:</b>
<input type="text" size="20" name="res_number" />
</p>
<p>
<b>パスワード:</b>
<input type="password" size="20" name="password" />
</p>
<p>
<b>
<select name="mode">
<option value="delete" selected>削除</option>
<option value="edit">編集</option>
</select>
</b>
<input type="submit" value="送信" /></p>
</form>
</article>
END
}
# スレ削除フォーム
sub view_thdelete{
	my($number)=shift;
	print <<END;
<article id="delete" class="form">
<h2>スレッドの削除</h2>
<form action="admin.cgi" method="post">
<p><input type="hidden" name="number" value="$number" />
<input type="hidden" name="mode" value="thdelete" />
<input type="hidden" name="password" value="$ini::password" />
<input type="submit" value="削除" /></p>
</form>
</article>
END
}
# スレ復活フォーム
sub view_threstore{
	my($number)=shift;
	print <<END;
<article id="delete" class="form">
<h2>スレッドの復活</h2>
<form action="admin.cgi" method="post">
<p><input type="hidden" name="number" value="$number" />
<input type="hidden" name="mode" value="threstore" />
<input type="hidden" name="password" value="$ini::password" />
<input type="submit" value="復活" /></p>
</form>
</article>
END
}
# レス編集ページ
sub editres{
	my($number,$res_number,$thread,$res,$old_password)=@_;
	view_header($thread);
	res($res);
	view_footer();

	$res->{'message'} =~ s/\<.+\>//g;

	my($formstr) = <<END;
<input type="hidden" name="mode" value="edit_do" />
<input type="hidden" name="number" value="$number" />
<input type="hidden" name="res_number" value="$res_number" />
<input type="hidden" name="old_password" value="$old_password" />
END
	if($::Global_admin_mode==1){
		$formstr .= <<END;
<input type="hidden" name="adminmode" value="adminmode" />
<input type="hidden" name="masterpassword" value="$ini::password" />
END
	}
	replydata_form($res,"レス編集フォーム","resedit",$formstr);
}

#=====================================================
#新スレのページ
sub newpage{
	my($cgi)=shift;
	my($name,$password)=($cgi->cookie("bbs_name"), $cgi->cookie("bbs_password"));
	topheader();
	replydata_form({
		'name' => $name,
		'password' => $password,
		'title' => "",
		'message' => ""
	},"新規スレッド作成","new",<<END);
<input type="hidden" name="mode" value="newdo" />
END
	footer();
	return;
}
#=====================================================
sub searchpage{
	topheader();
	print <<END;
<article class="form">
<h2>検索</h2>
<form action="index.cgi" method="post">
<p><input type="hidden" name="mode" value="find" />
<b>モード:</b>
<label><input type="radio" name="searchmode" value="or" checked="checked" />OR検索</label>　
<label><input type="radio" name="searchmode" value="and" />AND検索</label>
</p>
<p><input type="hidden" name="mode" value="find" />
<b>検索対象:</b>
<label><input type="checkbox" name="in" value="name" />名前</label>　
<label><input type="checkbox" name="in" value="title" />タイトル</label>　
<label><input type="checkbox" name="in" value="message" checked="checked" />本文</label>　
</p>
<p>
<b>検索語句:</b>
<input type="text" size="40" name="search" />
</p>
<p>
<b></b>
<input type="submit" value="検索" /></p>
</form>
</article>
END
	footer();
}
sub find_header{
	topheader();
	print <<END;
<article id="find">
<h2>検索結果</h2>
END
}
#スレッドごと
sub find_label{
	my($number,$title)=@_;
	print <<END;
<h3><a href="index.cgi?mode=view&number=$number">$title</a></h3>
END
}
sub find_footer{
	print <<END;
</article>
END
	footer();
}

#=====================================================
#cookieのHTTPヘッダ
sub cookie_header{
	my($cgi)=shift;
	my(@list)=('name','title','password');
	foreach(@list){
		my($cookie) = $cgi->cookie(-name => "bbs_$_",
			-value => $cgi->param($_),
			-expires => "+1M");
		$cookie =~ s/path\s*=\s*[^;]*;//i;
		print "Set-Cookie: $cookie\n";
	}
}



#=====================================================

# エラー（全部出力）
sub error1{
	topheader();
	error2($_[0]);
	footer();
}
# エラー（エラー部分だけ出力）
sub error2{
	print <<END;
<article class="error">
<p><strong>エラー</strong>：$_[0]</p>
</article>
END
}
#-----------------
# 内部で使うサブルーチン
sub navi{
	print <<END;
<nav>
  <ul>
    <li><a href="$ini::site">サイトに戻る</a></li>
    <li><a href="index.cgi">掲示板ホーム</a></li>
    <li><a href="index.cgi?mode=new">新規スレッド作成</a></li>
    <li><a href="index.cgi?mode=search">検索</a></li>
  </ul>
</nav>
END
}








return 1;
