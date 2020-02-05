#!/usr/bin/perl

use CGI qw(:standard); print "Content-type: text/html\n\n";
use strict;
use CGI;
use CGI::Carp 'fatalsToBrowser', 'croak';

my (
    $query,       # CGI query object
    $rand,        # random number for banners
    @params,      # array of all fields sent
    $usernum, $qnum, $itemID, $total, @order, $question, @answerIDs, $answerID, $answer, $seed, @answers, $comment,$pic,$cond,%nouns,%prep,%fillerimages,%fillerphrase,$type,$stimnum,$phrase,@images,@nouns, $image1,$image2,$image3,$image4,$image5,$image6,$image7,$image8,$image9,$image10,$subject,%subj,$size,$time,$audiofile,%words,$anim1,$anim2,$prep,$inan1,$inan2,$inan3,%word,$adj,$adjtype,$audiofile,$displaytype,$version,$writedir,
    );
$query=CGI->new;           # get CGI object


$writedir = ""; #for eecoppock.info
#$writedir = "/shared/hc/pc/data/";  #for semlab.bu.edu

print start_html(-title=>'Survey',
                 -style => { -src => 'survey.css',
                             -type => 'text/css',
                             -media => 'screen' },
                 );
print "<div id=\"shade\">";
print "<p>&nbsp;</p>";
print "<p>&nbsp;</p>";
print "<div id=\"content\">";
#print "<div id=\"pub\">";


#first print data from previous question

$usernum = $query->param("usernum");
$qnum = $query->param("qnum");
$cond = $query->param("cond");
$adjtype = $query->param("adjtype");
$audiofile = $query->param("audiofile");
$answer = $query->param("answer");
$time = localtime;

open (STIMFILE,"items.csv") or die "Can't find items.csv";

while (<STIMFILE>) {
    chomp;
    my ($itemnum,$anim1,$anim2,$prep,$inan1,$inan2,$inan3) = split(/,/);
    $itemnum =~ s/^[^0-9]+//; #no idea how freaky characters get on there
    $word{$itemnum}{"anim1"} = $anim1;
    $word{$itemnum}{"anim2"} = $anim2;
    $word{$itemnum}{"prep"} = $prep;
    $word{$itemnum}{"inan1"} = $inan1;
    $word{$itemnum}{"inan2"} = $inan2;
    $word{$itemnum}{"inan3"} = $inan3;
  }

close (STIMFILE);


open (STIMFILE,"fillers.csv") or die "Can't find fillers.csv";

#number,item reference,type,phrase,image1,image2,image3,image4,image5

while (<STIMFILE>) {
  chomp;
  $_ =~ s/[^a-z]$//;
  my ($itemnum,
      $anim1,$inan1,$anim2,$inan2,$anim3,$inan3,$anim4,$inan4,$anim5,$inan5,$phrase,$expected) = split(/,/);
  if ($itemnum =~ m/^[0-9]/) {
    #      $itemnum =~ s/^[^0-9]+//; #no idea how freaky characters get on there
    my @images =  ($anim1,$inan1,$anim2,$inan2,$anim3,$inan3,$anim4,$inan4,$anim5,$inan5,);
    $fillerimages{$itemnum} = \@images;
    $fillerphrase{$itemnum} = $phrase;
  }
}

close (STIMFILE);


open (ORDERFILE, "order.txt");

while (<ORDERFILE>) {
    chomp;
    my ($subject,@stims) = split(/ /);
    if ($subject eq $usernum) {
	@order = @stims;
    }
}
close (ORDERFILE);

$total = scalar(@order);

if ($qnum > 0) {

  open (DATAFILE, ">>$writedir data/data-$usernum.txt");
  $itemID = $order[$qnum-1];
  #($type,$stimnum) = split(/-/,$itemID);
  ($adjtype,$displaytype,$version) = split(/:/,$cond);
  print DATAFILE "$usernum\t$itemID\t$cond\t" . $adjtype . "\t" . $displaytype . "\t" . $version;
  print DATAFILE "\t$audiofile";
  print DATAFILE "\t" . $query->param("answer") . "\t" . $time;
  print DATAFILE "\t" . $query->param("posarray") . "\t" . $query->param("chosenpos") . "\t" . $query->param("images");
  print DATAFILE "\t" . $query->param("phrase") . "\n";
  #$comment = $query->param("comments");
  #print DATAFILE "$usernum $itemID comment $comment\n";
  close (DATAFILE);

} else {
  open (USERDATAFILE, ">>$writedir userdata/userdata-$usernum.txt");
  print USERDATAFILE "$usernum\tstarttime\t$time\n";
  close (USERDATAFILE);
}



#then print next question

$qnum = $qnum+1;

if ($qnum>$total) {

 # open (USERDATAFILE, ">>userdata/userdata-$usernum.txt");
  #note below changed after run from spaces to tabs
 # print USERDATAFILE "$usernum\tendtime\t$time\n";
 # close (USERDATAFILE);

  print "<br><br><br><br><br><br><h1>All done!</h1>  <p>Thanks for participating!</p>";

  #add comments here

  print "<p>If you have any questions or comments, <br> please send an email to ecoppock" . '@' . "bu.edu.</p>";

  print "<p>Completion URL: <a href=\"https://app.prolific.co/submissions/complete?cc=1B5D01FC\">https://app.prolific.co/submissions/complete?cc=1B5D01FC</a></p>";

} else {

 print "<p id=\"progress-indicator-position\">$qnum/$total</p>";

  $itemID = $order[$qnum-1];

  ($type,$stimnum) = split(/-/,$itemID);

 $stimnum =~ s/^[^0-9]+//; #no idea how freaky characters get on there

  if ($type eq "filler") {
    @images = @{$fillerimages{$stimnum}};
    $phrase = $fillerphrase{$stimnum};

    $image1 = $images[0];
    $image2 = $images[1];
    $image3 = $images[2];
    $image4 = $images[3];
    $image5 = $images[4];
    $image6 = $images[5];
    $image7 = $images[6];
    $image8 = $images[7];
    $image9 = $images[8];
    $image10 = $images[9];

#    print "$phrase" . " " . join(" ",@images);

    $audiofile = "filler-$stimnum";

    $cond = "NA:NA:NA";

  } elsif ($type eq "target") {

    $anim1 = $word{$stimnum}{"anim1"};
    $anim2 = $word{$stimnum}{"anim2"};
    $prep = $word{$stimnum}{"prep"};
    $inan1 = $word{$stimnum}{"inan1"};
    $inan2 = $word{$stimnum}{"inan2"};
    $inan3 = $word{$stimnum}{"inan3"};


    $cond = get_cond($usernum,$stimnum);


#    print "cond: $cond<br>\n";

    #    print "stimnum: $stimnum<br>\n";

    if ($cond =~ m/^cmp/) {
      $adj = "bigger";
      $adjtype = "cmp";
    } elsif ($cond =~ m/pos/) {
      $adj = "big";
      $adjtype = "pos";
    } else {
      print "ERROR: Unknown cond $cond";
    }

   if ($cond  =~ m/a$/) {
    $phrase = $anim1 . " " . $prep . " the " . $adj . " " . "[**]"; #underlyingly $inan1
    $audiofile = "target-$stimnum-a-$adjtype";
    if ($cond  =~ m/rel-abs/) {
      $image1 = $anim2 ;
      $image2 = $inan1 . "_big" ;
      $image3 = $anim1 ;
      $image4 = $inan1 . "_med" ;
      $image5 = $anim1 ;
      $image6 = $inan1 . "_small" ;
      $image7 = $anim1 ;
      $image8 = $inan2 . "_med" ;
      $image9 = $anim2 ;
      $image10 = $inan2 . "_small" ;
    } elsif ($cond =~ m/rel-both/) {
      $image1 = $anim2 ;
      $image2 = $inan1 . "_big" ;
      $image3 = $anim1 ;
      $image4 = $inan1 . "_med" ;
      $image5 = $anim1 ;
      $image6 = $inan1 . "_small" ;
      $image7 = $anim1 ;
      $image8 = $inan2 . "_med" ;
      $image9 = $anim1 ;
      $image10 = $inan2 . "_small" ;
    } elsif ($cond =~ m/abs-both/) {
      $image1 = $anim2 ;
      $image2 = $inan3 . "_big" ;
      $image3 = $anim1 ;
      $image4 = $inan1 . "_med" ;
      $image5 = $anim2 ;
      $image6 = $inan1 . "_small" ;
      $image7 = $anim1 ;
      $image8 = $inan2 . "_med" ;
      $image9 = $anim1 ;
      $image10 = $inan2 . "_small" ;
    } else {
      print "ERROR: Unknown cond $cond";
    }
  } elsif ($cond =~ m/b$/) {
    $phrase = $anim1 . " " . $prep . " the " . $adj . " " . "[**]"; #underlyingly $inan2
    $audiofile = "target-$stimnum-b-$adjtype-with";
    #and we just switch inan1 and inan2
    if ($cond  =~ m/rel-abs/) {
      $image1 = $anim2 ;
      $image2 = $inan2 . "_big" ;
      $image3 = $anim1 ;
      $image4 = $inan2 . "_med" ;
      $image5 = $anim1 ;
      $image6 = $inan2 . "_small" ;
      $image7 = $anim1 ;
      $image8 = $inan1 . "_med" ;
      $image9 = $anim2 ;
      $image10 = $inan1 . "_small" ;
    } elsif ($cond =~ m/rel-both/) {
      $image1 = $anim2 ;
      $image2 = $inan2 . "_big" ;
      $image3 = $anim1 ;
      $image4 = $inan2 . "_med"  ;
      $image5 = $anim1 ;
      $image6 = $inan2 . "_small" ;
      $image7 = $anim1 ;
      $image8 = $inan1 . "_med" ;
      $image9 = $anim1 ;
      $image10 = $inan1 . "_small" ;
    } elsif ($cond =~ m/abs-both/) {
      $image1 = $anim2 ;
      $image2 = $inan3 . "_big" ;
      $image3 = $anim1 ;
      $image4 = $inan2 . "_med" ;
      $image5 = $anim2 ;
      $image6 = $inan2 . "_small" ;
      $image7 = $anim1 ;
      $image8 = $inan1 . "_med" ;
      $image9 = $anim1 ;
      $image10 = $inan1 . "_small" ;
    } else {
   print "ERROR: Unknown cond $cond";
    }
    if ($cond  =~ m/a$/) {
      $phrase = $anim1 . " " . $prep . " the " . $adj . " " . "[**]"; #underlyingly $inan1
      $audiofile = "target-$stimnum-a-$adjtype";
    } elsif ($cond =~ m/b$/) {
      $phrase = $anim1 . " " . $prep . " the " . $adj . " " . "[**]"; #underlyingly $inan2
      $audiofile = "target-$stimnum-b-$adjtype";
    }


  } else {

    print "ERROR: UNKNOWN TYPE $type with itemID $itemID\n";

  }
  }


foreach my $i (1..5) {
    my $lineposition = $i;
    print "<svg id=\"line-position-$lineposition\">";
    print "<line  x1=\"0\" y1=\"0\" x2=\"0\" y2=\"100\">";
    print "</svg>\n";
}

  my $i = 1;

  my @positionorder = position_pairs(randarray(1,2,3,4,5));

 foreach my $image ($image1, $image2, $image3, $image4, $image5, $image6, $image7, $image8, $image9, $image10) {

   $image =~ s/[^a-z-_]//g;

#   print "[$image] ";

   $size = 160;

    my $position = $positionorder[$i-1];


    print "<form method=post action=display-question.cgi name=form$i>\n";

   print "<input type=hidden name=usernum value=\"$usernum\">\n";
   print "<input type=hidden name=cond value=\"$cond\">\n";
   print "<input type=hidden name=adjtype value=\"$adjtype\">\n";
   print "<input type=hidden name=audiofile value=\"$audiofile\">\n";
    print "<input type=hidden name=qnum value=\"$qnum\">\n";
    print "<input type=hidden name=itemID value=\"$itemID\">\n";
    # print "<input type=hidden name=posarray value=\"" . join(":", @positionorder) ."\">\n";
    print "<input type=hidden name=posarray value=\"1:2:3:4:5:6:7:8:9:10\">\n";
    print "<input type=hidden name=images value=\"$image1:$image2:$image3:$image4:$image5:$image6:$image7:$image8:$image9:$image10\">\n";
    print "<input type=hidden name=chosenpos value=\"$position\">\n";
    print "<input type=hidden name=phrase value=\"$phrase\">\n";
    print "<input type=hidden name=answer value=\"$i\">";
    print "<label>\n";

#     print  "<input type=submit> <img src=\"images/$image.png\" width=$size id=\"object-position-$position\", alt=\"$image.png\"\">\n";

    print  "<input type=button> <img src=\"images/$image.png\" width=$size id=\"object-position-$position\", alt=\"$image.png\"  onclick=\"checkform$i();\">\n";

    print "</label>";

    print "</form>";


    $i++;
  }

 # print "<p id=audio-button>Click on the $phrase.<br>cond $cond</p>";

 # print"    <script>
 #  function play(){
 #       var audio = document.getElementById(\"audio-button\");
 #       audio.play();
 #                 }
 #   </script>";


print "<p class=\"myInstructions\">Click on the $phrase.</p>";

 # older working version
#  print "<div id=\"audio-button\"><audio controls >
#   <source src=\"audio/$audiofile.mp3\" type=\"audio/mpeg\" alt=\"Click on the $phrase.\">
# Your browser does not support the audio element.
# </audio><br>Click on the $phrase.</div>\n";


}


#print "</div>";
print "</div>";
print "</div>";

 print "
 <script>
 function checkform1() {
    document.form1.submit();
  }
 </script>";

 print "
 <script>
 function checkform2() {
    document.form2.submit();
  }
 </script>\n\n";

 print "
 <script>
 function checkform3() {
    document.form3.submit();
  }
 </script>\n\n";

 print "
 <script>
 function checkform4() {
    document.form4.submit();
  }
 </script>\n\n";

 print "
 <script>
 function checkform5() {
    document.form5.submit();
  }
 </script>\n\n";

 print "
 <script>
 function checkform6() {
    document.form6.submit();
  }
 </script>\n\n";

 print "
 <script>
 function checkform7() {
    document.form7.submit();
  }
 </script>\n\n";

 print "
 <script>
 function checkform8() {
    document.form8.submit();
 }
 </script>\n\n";

 print "
 <script>
 function checkform9() {
    document.form9.submit();
 }
 </script>\n\n";


 print "
 <script>
 function checkform10() {
    document.form10.submit();
 }
 </script>";


print "</body></html>";


sub randarray {
        my @array = @_;
        my @rand = undef;
        $seed = $#array + 1;
        my $randnum = int(rand($seed));
        $rand[$randnum] = shift(@array);
        while (1) {
                my $randnum = int(rand($seed));
                if ($rand[$randnum] eq undef) {
                        $rand[$randnum] = shift(@array);
                }
                last if ($#array == -1);
        }
        return @rand;
}

sub position_pairs {
  my @array = @_;
  my @paired = ();
  my $side = int(rand(2));
  for (@array){
    if ($side >= 1) {
      push @paired, 2*$_ -1;
      push @paired, 2*$_;
    }
    else {
      push @paired, 2*$_;
      push @paired, 2*$_-1;
    }
  }
  return @paired;
}


sub get_cond {
  my ($usernum,$itemnum) = @_;
  my @conds = ("cmp:rel-abs:a","cmp:rel-both:a","cmp:abs-both:a",
	       "cmp:rel-abs:b","cmp:rel-both:b","cmp:abs-both:b",
	       "pos:rel-abs:a","pos:rel-both:a","pos:abs-both:a",
	       "pos:rel-abs:b","pos:rel-both:b","pos:abs-both:b"
	      );
  my $i = ($usernum+$itemnum) % 12;
  my $cond = $conds[$i];
  return $cond;
}
