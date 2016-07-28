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

my $query_locations = $dbh->prepare("SELECT *  FROM Locations");
my $query_documents_etiquet = $dbh->prepare("SELECT * FROM Dokumente");

$query_locations->execute() or die $query_locations->err_str;
$query_documents_etiquet->execute() or die $query_documents_etiquet->err_str;

#Auflistung aller Eintraege
my $json = "[";
my $lastID;

while(my ($col_1, $col_2 , $col_3) = $query_locations->fetchrow_array()){
	my %Daten = (
			"id" 		=> $col_1,
			"FolderID" 	=> $col_1,
			"parent" 	=> $col_3,
			"text" 		=> $col_2
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

while(	my ($d1,$d2,$d3,$d4,$d5,$d6,$d7,$d8,$d9,$d10,$d11) = $query_documents_etiquet->fetchrow_array() ){
	my %Daten = (	
			"id"	 		=> $lastID += 1,
			"doc_did" 		=> $d1,
			"parent"	 	=> $d2,
			"doc_bid" 		=> $d3,
			"doc_version" 		=> $d4,
			"doc_autor" 		=> $d5,
			"type" 			=> $d6,
			"doc_description"	=> $d7,
			"doc_created" 		=> $d8,
			"doc_updated" 		=> $d9,
			"doc_address" 		=> $d10,
			"text"	 		=> $d11
			);

	my $encodedJSON = encode_json \%Daten;
	if($json eq "["){
		$json .= $encodedJSON;

	}else{
		$json = $json.",".$encodedJSON;	
	}
}

$json = $json."]";
print "$json\n";


$dbh->disconnect();
