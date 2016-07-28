#!/usr/bin/perl -w
use strict;
use warnings;

use CGI;
use CGI::Carp qw(fatalsToBrowser);
use DBI;
use JSON qw(encode_json decode_json);
use File::Path qw(make_path remove_tree);

print qq(Content-type : text/html\n\n);

my $query   = CGI->new();
my $rename  = $query->param("rename");
my $delete  = $query->param("delete");
my $create  = $query->param("create");

#Make the database connection
my ($db_user,$db_name,$db_pass) = ("root","CameronetDokVer","xebative123");
my $dbh = DBI->connect("DBI:mysql:database=$db_name",$db_user,$db_pass) or die "Fehler bei Datenbankverbindung: $!\n\n";

if ($rename){
	rename_in_DB();	
}elsif($delete){
	my $decodeDelete = decode_json($delete);
	delete_in_DB($decodeDelete);
}

sub rename_in_DB(){
	my $bid = -1;
	my $locID = -1;
	my $decodeRename = decode_json($rename);

	$bid = $decodeRename->{BID};
	$locID = $decodeRename->{FolderID};
	my $parentID = $decodeRename->{ParentID};
	my $newName = $decodeRename->{NewName};
	my $originalName = $decodeRename->{OriginalName};

#	Only for Folders we will select from DB to verify if they exist already 
#	In the case that they will not exist we will make an insert

	my $selectFromDB = $dbh->prepare("SELECT * FROM CameronetDokVer.Locations WHERE LocationName='$originalName' AND Locations.ParentLocationID=$parentID");
	$selectFromDB->execute() or die $selectFromDB->err_str;
	
	if ($selectFromDB->fetchrow_array()<=0){ 
		
		my $insertInDB = $dbh->prepare("INSERT INTO CameronetDokVer.Locations (LocationName,ParentLocationID) VALUES ('$newName',$parentID);");
		$insertInDB->execute() or die $insertInDB->err_str;

		create_dir($newName);		
	}else{	
#	print $bid;
		print $newName."\t <-> this is the new name\n";
		print $locID."\t <-> this would be the new location\n";

		if($bid and ($bid >= 0)){
			my $renameFile = $dbh->prepare("UPDATE CameronetDokVer.DokumentBeschreibung SET Name='$newName' WHERE DokumentBeschreibung.BID=$bid;");
			$renameFile->execute();

			print "\t I am inside BID\n";
	
		}elsif($locID and $locID >= 0){
			my $renameFolder = $dbh->prepare("UPDATE CameronetDokVer.Locations SET LocationName='$newName' WHERE Locations.LocationID=$locID;");
			$renameFolder->execute(); 
			print "edited the name of the folder";
		}
	}	
}

sub delete_in_DB(){
	print "I am in the delete function\n";	
	my $deleteArray = shift(@_);
	
	my $did 	 = -1;
	my $FolderID 	 = -1;

	$did 		 = $deleteArray->{DID};
	$FolderID 	 = $deleteArray->{FolderID};
	
	print "This is the FolderID"." -> "."$FolderID\n";	
	print "This is the DID"." -> "."$did\n";	
	
	if($did and $did >= 0){
		my $deleteInDB = $dbh->prepare("DELETE FROM CameronetDokVer.Dokumente WHERE Dokumente.DID=$did;");
		$deleteInDB->execute() or die $deleteInDB->err_str;
	}elsif($FolderID and $FolderID >= 0){
		delete_recursive_fromDB($FolderID);	
#		$deleteInDB = $dbh->prepare("DELETE FROM ");
		print "This is a Folder";
	}

	
}

sub delete_recursive_fromDB(){
	my $id = shift(@_);
#	$id = $id->{FolderID};
	print "$id"." -> delete recursive from DB";
#	my $deleteInDB	= $dbh->prepare("DELETE Locations,DokumentBeschreibung FROM 
#					Locations INNER JOIN DokumentBeschreibung WHERE 
#					Locations.LocationID=$id and Locations.ParentLocationID=$id and DokumentBeschreibung.LocationID=$id;");

	my $deleteInDB = $dbh->prepare("DELETE FROM CameronetDokVer.Locations WHERE Locations.LocationID=$id;");

	$deleteInDB->execute() or die $deleteInDB->err_str;
#	delete_recursive_fromDB($id);
}

sub create_dir(){
	my $folder = shift(@_);
	
	print $folder." This is the name of the Folder\n";
	
	my $root_dir = "/var/www/html/folders/$folder";

	unless(mkdir $root_dir,0755){
		die "Unable to create $root_dir  ..... $!\n";
	}
}
#sub create_in_DB(){
#	my $nodeArray = shift(@_);
#	my $locationName = $nodeArray->{LocationName};
#	my $parentID = $nodeArray->{ParentID};
#	
#	print "$parentID\n"."parent ID";
#
#	$insertInDB->execute();
#
#	print "DB executed with the ParentID -> $parentID and Location Name -> $locationName;\n";
#}

$dbh->disconnect();
