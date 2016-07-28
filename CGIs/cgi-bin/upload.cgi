#!/usr/bin/perl -w
use strict;
use warnings;

#use DVS;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use DBI;
use File::Basename;

$CGI::POST_MAX = 1024*5000;

print qq(Content-type: text/html\n\n);

my $query 	= CGI->new();
my $upload_dir 	= "/var/www/html/folders";
my $filename 	= $query->param(	"file"		);
my $folderName 	= $query->param(	"folderName"	);
my $folderId 	= $query->param(	"folderId"	);
my $autorId 	= $query->param(	"autorId"	);
my $docVersion 	= $query->param(	"docVersion"	);
my $docDate 	= $query->param(	"docDate"	);
my $docCategory = $query->param(	"docCategory"	);
my $docComments	= $query->param(	"docComments"	);

#my $dbh = dbConnect();

#	----------Make the database connection and Prepares------------
my ($db_user,$db_name,$db_pass) = ("root","CameronetDokVer","xebative123");
my $dbh 			= DBI->connect("DBI:mysql:database=$db_name",$db_user,$db_pass) or die "Fehler bei Datenbankverbindung: $!\n\n";
my $newInsert 			= $dbh->prepare("INSERT INTO CameronetDokVer.Dokumente (LocationID,BID,Version,AutorID,type,Beschreibung,Created_at,Pfad,Name) VALUES (?,?,?,?,?,?,?,?);");
#	--------------------------- FINISH ----------------------------

#	$newDescription will help ud to control the state of DokumentBeschreibung (if is empty or not)
my $newDescription 		= $dbh->prepare("SELECT * FROM DokumentBeschreibung;");
my $insertIntoDescription 	= $dbh->prepare("INSERT INTO CameronetDokVer.DokumentBeschreibung (LocationID,Gesperrt,Name,type) VALUES (?,?,?,?);");
	
	if(!$filename){
		print $query->header();
		print "Deine Datei k&ouml;nnte zu gross sein (versuch bitte ein kleineres hochzuladen)";
		print $filename;
		exit;
	}

	if($filename and $folderName and $folderId and $autorId and $docVersion and $docDate and $docCategory and $docComments){
		write_file_in_db($filename,$folderName,$folderId,$autorId,$docVersion,$docDate,$docCategory,$docComments);
		open(UPLOADFILE,">$upload_dir/$filename") or die "$!";

		my $nBytes = 0;
		my $totBytes = 0;
		my $buffer = "";

		binmode UPLOADFILE;
		binmode $filename;

		while($nBytes = read($filename, $buffer, 1024)){
			print UPLOADFILE $buffer;
		}
		close UPLOADFILE;
	}

#	we call this function when we have all the data we need to update or add into DB
#	------------------------------- START ------------------------------------------------
#	IN THIS FUNCTION WE CAN MAKE THE "UPLOAD" MAGIG IN DATABASE

	sub write_file_in_db(){
#	we save the parameters in an array so will be easier for us to manipulate later the values
		my (@data) = @_;

		my $fileName_ 		= $data[0];
		my $folderName_		= $data[1];
		my $locationId_ 	= $data[2];
		my $autorId_ 		= $data[3];
		my $docVersion_ 	= $data[4];
		my $docDate_ 		= $data[5];
		my $docCategory_	= $data[6];
		my $docComments_ 	= $data[7];

		print "$fileName_\n";
		print "$folderName_\n";
		print "$locationId_\n";
		print "$autorId_\n";
		print "$docVersion_\n";
		print "$docDate_\n";
		print "$docCategory_\n";
		print "$docComments_\n";

		$newDescription->execute() or die $newDescription->err_str;
		if($newDescription->rows == 0){
			$insertIntoDescription->execute("$data[2]",0,"$data[0]","file");	
		}else{

#	my $queryDB = $dbh->prepare("SELECT * FROM Dokumente");
#	$queryDB->execute() or die $queryDB->err_str;
#	if($queryDB->rows == 0){
#	print "We have nothing there";
#	we save our uploaded file in the DB 
#			dbh->prepare("INSERT INTO CameronetDokVer.Dokumente (LocationID,BID,Version,AutorID,type,Created_at,Pfad,Name) VALUES (?,?,?,?,?,?,?,?);");
						
			$newInsert->execute($locationId_,4,$docVersion_,$autorId_,"file",$docComments,$docDate_,"/folders/$fileName_",$fileName_) or die $newInsert->err_str;
#	}else{
#	while( my($DID,$LocationID,$BID,$Version,$AutorID,$type,$Beschreibung,$Created_at,$Updated_at) = $queryDB->fetchrow_array() ){
#	print "Seems that we have some rows in the DB";
#	}
#	}

		}
	}
#	------------------------------ FINISH ------------------------------------------------

print $query->header();
print "<!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.01 Transitional//EN'>\n";
print "<html>\n";
print "<head>\n";
print "<meta http-equiv='Content-Type' content='text/html; charset='utf-8' />\n";
print "</head>\n";
print "<body> Everything went fine!! </body>\n";
print "</html>";

$dbh->disconnect();
