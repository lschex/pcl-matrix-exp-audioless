#!/usr/bin/perl

use CGI qw(:standard); print "Content-type: text/html\n\n";
use strict;
use CGI;
use CGI::Carp 'fatalsToBrowser', 'croak';

my (
    $query,       # CGI query object
    $rand,        # random number for banners
    @params,      # array of all fields sent
    $usernum, $qnum, $itemID, $total, @order, $question, @answerIDs, $answerID, $answer, $seed, @answers, $comment,$pic,$cond,%nouns,%prep,%fillerimages,%fillerphrase,$type,$stimnum,$phrase,@images,@nouns, $image1,$image2,$image3,$image4,$image5,$image6,$image7,$image8,$image9,$image10,$subject,%subj,$size,$time,$image,$i,$num
    );
$query=CGI->new;           # get CGI object

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
$time = localtime;

open (STIMFILE,"practice-items.csv") or die "Can't find practice-items.csv";

#number,item reference,type,phrase,image1,image2,image3,image4,image5,$image6,$image7,$image8,$image9,$image10

while (<STIMFILE>) {
    chomp;
    my ($itemnum,$itemref,$type,$phrase, @images) = split(/,/);
    if ($itemnum =~ m/^[0-9]/) {
      $fillerimages{$itemnum} = [@images];
      $fillerphrase{$itemnum} = $phrase;
    }
  }

close (STIMFILE);


$qnum = $qnum+1;

$total = 3;

if ($qnum>$total) {


  print "<form method=post action=\"display-question.cgi\">
<input type=hidden name=usernum value=$usernum>
<input type=hidden name=qnum value=0>
<input type=submit value=\"Let's begin!\"  id=begin>
</form> </p>";

} else {

  print "<p id=\"progress-indicator-position\">$qnum/$total</p>";
  foreach my $i (1..5) {
      my $lineposition = $i;
      print "<svg id=\"line-position-$lineposition\">";
      print "<line  x1=\"0\" y1=\"0\" x2=\"0\" y2=\"100\">";
      print "</svg>\n";
  }

  $stimnum = $qnum;

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

  my $i = 1;

  my @positionorder = position_pairs(randarray(1,2,3,4,5));

 foreach my $image ($image1, $image2, $image3, $image4, $image5,$image6,$image7,$image8,$image9,$image10) {


   #   print "[$image] ";

   $size = 160;

   my $position = $positionorder[$i-1];



   print "<form method=post action=practice-trial.cgi name=form$i>\n";

   print "<input type=hidden name=usernum value=$usernum>\n";
   print "<input type=hidden name=cond value=$cond>\n";
   print "<input type=hidden name=qnum value=$qnum>\n";
   print "<input type=hidden name=itemID value=$itemID>\n";
   print "<input type=hidden name=time id=time value=\"\">\n";

   print "<label>\n";

   print  "<input type=button name=answer value=$i required> <img src=\"images/$image.png\" width=$size id=\"object-position-$position\", alt=\"$image.png\"  onclick=\"checkform$i();\">\n";

   print "</label>";



   print "</form>";


   $i++;
 }

  #old working version
#   print "<audio controls id=\"audio-button\">
#   <source src=\"audio/practice-$qnum.mp3\" type=\"audio/mpeg\" alt=\"Click on the $phrase.\">
# Your browser does not support the audio element.
# </audio>\n";


 # print"    <script>
 #  function play(){
 #       var audio = document.getElementById(\"audio-button\");
 #       audio.play();
 #                 }
 #   </script>";


print "<p class=\"myInstructions\">$phrase.</p>";


}





  #    print "<br>Comments (optional):<br> <input type=text name=comments size=90>";



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
    window.alert(\"Are you sure?  Remember that an object is with another object if they are connected by a black line.\");
  }
 </script>\n\n";

 print "
 <script>
 function checkform3() {
    window.alert(\"Oops! That does not seem to be the correct answer.\");
  }
 </script>\n\n";

 print "
 <script>
 function checkform4() {
    window.alert(\"Oops! That does not seem to be the correct answer.\");
  }
 </script>\n\n";

 print "
 <script>
 function checkform5() {
    window.alert(\"Oops! That does not seem to be the correct answer.\");
  }
 </script>\n\n";

 print "
 <script>
 function checkform6() {
    window.alert(\"Oops! That does not seem to be the correct answer.\");
  }
 </script>\n\n";

 print "
 <script>
 function checkform7() {
    window.alert(\"Oops! That does not seem to be the correct answer.\");
  }
 </script>\n\n";

 print "
 <script>
 function checkform8() {
    window.alert(\"Oops! That does not seem to be the correct answer.\");
  }
 </script>\n\n";

 print "
 <script>
 function checkform9 {
    window.alert(\"Oops! That does not seem to be the correct answer.\");
  }
 </script>\n\n";

 print "
 <script>
 function checkform10() {
    window.alert(\"Oops! That does not seem to be the correct answer.\");
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
  if ($usernum % 4 < 1) {
    if ($itemnum % 4 < 1) {
      return "rel-a";
    } elsif ($itemnum %4 < 2) {
      return "abs-a";
    } elsif ($itemnum %4 < 3) {
      return "rel-b";
    }  else {
      return "abs-b";
    }
  } elsif ($usernum % 4 < 2) {
    if ($itemnum % 4 < 1) {
      return "abs-a";
    } elsif ($itemnum %4 < 2) {
      return "rel-b";
    } elsif ($itemnum %4 < 3) {
      return "abs-b";
    }  else {
      return "rel-a";
    }
  }
   elsif ($usernum % 4 < 3) {
    if ($itemnum % 4 < 1) {
      return "rel-b";
    } elsif ($itemnum %4 < 2) {
      return "abs-b";
    } elsif ($itemnum %4 < 3) {
      return "rel-a";
    }  else {
      return "abs-a";
    }
  } else {
    if ($itemnum % 4 < 1) {
      return "abs-b";
    } elsif ($itemnum %4 < 2) {
      return "rel-a";
    } elsif ($itemnum %4 < 3) {
      return "abs-a";
    }  else {
      return "rel-b";
    }
  }
}
