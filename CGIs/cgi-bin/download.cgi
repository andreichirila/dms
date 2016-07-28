#!/usr/bin/perl -w
use strict;
use warnings;

use CGI;
use CGI::Carp qw(fatalsToBrowser);
use DBI;
use File::Basename;
use Net::Address::IP::Local;

my $address_ipv4 = Net::Address::IP::Local->public_ipv4;
my $browser 		= CGI->new();
#	get the file name from URL ex. "http://<server_IP>/cgi-bin/download.cgi?name=$filename"
my $browserParam 	= $browser->param("name");
my $directory		= "/var/www/html/folders";
my $filesLocation 	= "$directory/$browserParam";

print	"Content-Type:		application/x-download\n";
print	"Content-Disposition:	attachment;filename=$browserParam\n\n";

#	we have to prepare the file for sen|| Error("open","file");ding back to the user
open (FILE,"<$filesLocation") or die "can't open the file : $filesLocation <-------> $!\n";

my @fileholder;
binmode FILE;
@fileholder = <FILE>;

while(<FILE>){
	print $_;
}
#	this address will be sended back to AJAX
print("http://$address_ipv4/folders/$browserParam");
#	close the File
close (FILE) || Error("close","file");

#	we write in the LOG 
open(LOG,">>/var/www/html/folders/dl.log") or die $!;
print LOG "$browserParam\n";
close(LOG);


