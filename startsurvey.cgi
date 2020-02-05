#!/usr/bin/perl

use CGI qw(:standard); print "Content-type: text/html\n\n";

use strict;
use CGI;
use CGI::Carp 'fatalsToBrowser', 'croak';

my ($query,$inputdata,@params,$num,$newnum,$itemID,%item,@randitems,$seed,@stims,@lines,@targets,@fillers,@randtargets,@randfillers,$writedir);


$writedir = "."; #for eecoppock.info
#$writedir = "/shared/hc/pc/data";  #for semlab.bu.edu

$query=CGI->new;

print start_html(-title=>'Survey',
                 -style => { -src => '/styles/survey.css',
                             -type => 'text/css',
                             -media => 'screen' },
                 );
print "<div id=\"shade\">";
print "<p>&nbsp;</p>";
print "<p>&nbsp;</p>";
print "<div id=\"content\">";
print "<div id=\"pub\">";

@params = $query->param;


#read old usernum
open (USERNUMFILE, "usernum.txt");
while (<USERNUMFILE>) {
    chomp;
    if (/([0-9]+)/) {
	$num = $1;
      } else {
	$num = 0;
      }
}
$newnum = $num + 1;
close (USERNUMFILE);

#update it
open (USERNUMFILE, ">usernum.txt");
print USERNUMFILE $newnum;
close (USERNUMFILE);

#print user data

open (USERDATAFILE, ">$writedir/userdata/userdata-$num.txt") or print "WARNING: Cannot open userdata file";

foreach my $paramKey (@params) {
    $inputdata = $query->param($paramKey);
    print USERDATAFILE "$num\t$paramKey\t$inputdata\n";
  }

foreach my $key ("REMOTE_ADDR","REMOTE_PORT","UNIQUE_ID","HTTP_USER_AGENT") {
   print USERDATAFILE "$num\t$key\t$ENV{$key}\n";
}

close (USERDATAFILE);



print "<p>&nbsp;</p>";

print "<h1>Welcome!</h1>";

print "<p>Thanks for participating!</p>
<p>Let's get started. As a reminder:</p>";

print "<p>You will see a series of scenes. Each scene contains five image pairs. There will be a black bar connecting each pair - this represents two objects that are \"with\" each other. The text at the top contains instructions about which image to pick.</p>";

print "<p>In some cases, part of the instructions will be covered up by by \"[**]\", so you won't be able to see one of the words. This is not an error; it is intended. In that case, just do your best and trust your intuition.</p>";

print "<p><b>Note</b>: There is sometimes a tendency for the server to drop the connection. If this happens, just <i>press the 'Back' button on your browser to go to the previous question</i>, and try again. It should work. Apologies for this inconvenience if it happens.</p>";

print "<p>We'll do three practice trials before we begin.</p>";

print "<form method=post action=\"practice-trial.cgi\">
<input type=hidden name=usernum value=$num>
<input type=hidden name=qnum value=0>
<input type=submit value=\"Begin practice trials\">
</form>";

close (USERDATAFILE);

open (STIMFILE,"items.csv") or print "Can't find items.csv";

@lines = <STIMFILE>;


foreach my $line (@lines) {
    chomp;
    my ($itemnum,@rest) = split(/,/,$line);
    if ($itemnum =~ m/[0-9]/) {
      push(@targets,"target-$itemnum");
    }
  }

close (STIMFILE);

open (FILLERFILE,"fillers.csv") or print "Can't find fillers.csv";

@lines = <FILLERFILE>;

foreach my $line (@lines) {
    chomp;
    my ($itemnum,@rest) = split(/,/,$line);
    if ($itemnum =~ m/[0-9]/) { #valid filler id
      $itemnum =~ s/^[^0-9]+//; #make sure there's no freaky crap at the beginning
      push(@fillers,"filler-$itemnum");
    }
  }

close (FILLERFILE);

@randfillers = randarray(@fillers);

@randtargets = randarray(@targets);

@randitems = merge_lists();

#@randitems = randarray(@stims);

open (ORDERFILE,">>order.txt");

print ORDERFILE "$num @randitems\n";

close(ORDERFILE);


print "</div>";
print "</div>";
print "</div>";

print "</body></html>";

sub merge_lists {
  my $thing;
  my $i = 0;
  while (@randtargets) {
    if ($i % 3 < 2) {
      $thing  = shift(@randfillers);
    } else {
      $thing = shift(@randtargets);
    }
    push(@randitems,$thing);
    $i++;
  }
  return(@randitems);
}


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
