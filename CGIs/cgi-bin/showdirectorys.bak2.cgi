#!/usr/bin/perl -wT

use strict;
use warnings;
use English;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use DBI;
use JSON;

print qq(Content-type: text/html\n\n);

my $cgi = CGI->new();

my ($db_user,$db_name,$db_pass) = ("root","CameronetDokVer","xebative123");

#Make the database connection
my $dbh = DBI->connect("DBI:mysql:database=$db_name",$db_user,$db_pass) or die "Fehler bei Datenbankverbindung: $!\n\n";

#verbindung zur DB herstellen
#alternativ (wenn DB nicht lokal):
#my $dbh = DBI->connect("DBI:mysql:database=$db_name;host=$db_host;port=$db_port","$db_user","$db_pass")
#man kann auch noch Fein-Tuning betreiben, z.B mit dem RaiseError- oder dem AutoCommit-Switch

#Vorbereitung der SQL-Anweisung 

my $query_locations = $dbh->prepare("SELECT *  FROM  Locations");
my $query_documents_etiquet = $dbh->prepare("SELECT * FROM DokumentBeschreibung");

$query_locations->execute() or die $query_locations->err_str;
$query_documents_etiquet->execute() or die $query_documents_etiquet->err_str;

#Auflistung aller Eintraege
my $json = "[";
my $lastID;
my %children;

while(my ($col_1, $col_2 , $col_3) = $query_locations->fetchrow_array()){
#	HERE ARE THE CHILDREN
#	we will take the childrens from "DokumentBeschreibung" for this Folder ($col_1)
	my $queryChildren = $dbh->prepare("SELECT * FROM DokumentBeschreibung WHERE LocationID=$col_1");
	$queryChildren->execute();

	while(	my($attr_1,$attr_2,$attr_3,$attr_4,$attr_5,$attr_6) = $queryChildren->fetchrow_array()	){
		%children = (
				"bid" 	  => $attr_1,
				"descr"	  => $attr_2,
				"locID"	  => $attr_3,
				"blocked" => $attr_4,
				"cName"   => $attr_5,
				"type"	  => $attr_6					
				)	
	}
	my $encodedJSONChilds = encode_json \%children;
#	HERE ARE THE PARENTS

	my %Daten = (
			"id" 		=> $col_1,
			"FolderID" 	=> $col_1,
			"parent" 	=> $col_3,
			"text" 		=> $col_2,
			"children"	=> "[".$encodedJSONChilds."]"
			);

	#we save all the time the ID so we can add it to the documents
	$lastID = $Daten{"id"};

	my $encodedJSON = encode_json \%Daten;
	
	if($json eq "["){
		$json .= $encodedJSON;

	}else{
		$json = $json.",".$encodedJSON;	
	}

}

#while(my ($d1,$d2,$d3,$d4,$d5,$d6) = $query_documents_etiquet->fetchrow_array()){
#	my %Daten = (	"id" => $lastID += 1,
#			"bid" => $d1,
#			"beschreibung" => $d2,
#			"parent" => $d3,
#			"gesperrt" => $d4,
#			"text" => $d5,
#			"type" => $d6);
#
#	my $encodedJSON = encode_json \%Daten;
#
#	if($json eq "["){
#		$json .= $encodedJSON;
#
#	}else{
#		$json = $json.",".$encodedJSON;	
#	}
#}

$json = $json."]";
print "$json\n";


$dbh->disconnect();
