$(document).ready(function() {
//Disabling autodiscover, otherwise Dropzone will try to attach twice
    Dropzone.autoDiscover = false;
    connectDB.init();
    upload.defineDropzone();

    $(".search").keyup(function () {
        var searchTerm = $(".search").val();
        var listItem = $('.results tbody').children('tr');
        var searchSplit = searchTerm.replace(/ /g, "'):containsi('");

        $.extend($.expr[':'], {'containsi': function(elem, i, match, array){
            return (elem.textContent || elem.innerText || '').toLowerCase().indexOf((match[3] || "").toLowerCase()) >= 0;
        }
        });

        $(".results tbody tr").not(":containsi('" + searchSplit + "')").each(function(e){
            $(this).attr('visible','false');
        });

        $(".results tbody tr:containsi('" + searchSplit + "')").each(function(e){
            $(this).attr('visible','true');
        });

        var jobCount = $('.results tbody tr[visible="true"]').length;
        $('.counter').text(jobCount + ' item');

        if(jobCount == '0') {$('.no-result').show();}
        else {$('.no-result').hide();}
    });

});

var connectDB = {
    init: function(){
        //console.log(typeof connectDB.init);
        $.get("/cgi-bin/showdirectorys.cgi",function(res){

            if(res === null || res === "undefined"){
                alert("We have no Data to show");
                return;
            }

            res = JSON.parse(res);
            showDataInTree.show(res);
        })
        .fail(function(err){
            console.log(err);
            console.log("In the ERROR function");
        });
    }
};
var showDataInTree = {
    show : function(data){
        var $jsTree = $(".jstree_folders");

//  we need " # " to define the root of the folders in jsTree Framework
        if(data[0].parent === null) data[0].parent = '#';

        $jsTree.jstree({
            "plugins" : [
                "search",
                "contextmenu",
                "types"
            ],
            "types" : {
                "file" : {
                    "icon" : "../../img/file.png"
                },
                "default" : {
                    "icon" : "../../img/folder.png"
                }
            },
            "core":{
                "themes":{
                    "variant":"large"
                },
                "data": data,
                "check_callback" : function(operation,node,nodeParent,nodePosition){

        //  In @node.original we will find all the time the original data sended from CGI
        //  from there (@node.original) we can take the BID and the name of the original document
                    var json;

                    switch(operation){
                        case "rename_node" :
//  @todo -> renaming for files also ---------------------------> not only for folders
                            json = "rename="+JSON.stringify(
                                {
                                    "BID":node.original.bid,
                                    "OriginalName":node.text,
                                    "ParentID":node.parent,
                                    "NewName":nodePosition,
                                    "FolderID":node.original.FolderID
                                }
                            );

                            processEvents.processNode(json);
                            break;

                        case "delete_node" :

                            if(node.original.doc_did){
                                json = "delete="+JSON.stringify(
                                    {
                                        "DID":node.original.doc_did,
                                        "FolderID":node.original.parent
                                    }
                                )
                                console.log(json + "  In THIS PLACE");
                            }else if(node.original.FolderID){
                                json = "delete="+JSON.stringify(
                                        {
                                            "FolderID":node.original.FolderID,
                                            "parentID":node.original.parent
                                        }
                                    );
                            }else{
                                console.log("SOMETHING WENT WRONG: No BIDs or FolderIDs");
                            }

                            processEvents.processNode(json);
                            break;

                        default : console.log("default");break;
                    }

                    //create, rename, delete, move or copy
                    /*console.log(operation);
                    console.log(node.original.bid);
                    console.log(node.text);
                    console.log(node.parent);
                    console.log(nodeParent);
                    console.log(nodePosition); // the name of the edited node*/
                }
            },
            'contextmenu' : {
                'items' : function(node) {
                    var tmp = $.jstree.defaults.contextmenu.items();
                    delete tmp.ccp.submenu;

                    tmp.ccp.label = "Mehr";
                    tmp.ccp.icon = "../../img/more.png";
                    tmp.ccp.submenu = {
                        "upload_file" : {
                            "separator_after"	: true,
                            "label"				: "Hochladen",
                            "icon"              : "../../img/upload.png",
                            "action"			: function (data) {

                                console.log("BEGIN - DATA:");
                                console.log(data);
                                console.log("FINISHED - DATA:");

                                var inst = $.jstree.reference(data.reference);
                                var obj = inst.get_node(data.reference);
                                var currentdate = new Date();

                                currentdate = currentdate.today() + " " + currentdate.timeNow();
    //we write the time and date in the Field
                                $("#doc_date").val(currentdate);
                                console.log(obj);
                                    /*
                                    inst.create_node(obj,
                                        { type : "file" },
                                        "last",
                                        function (new_node) {
                                            console.log(new_node);
                                    });
                                    */
                                /*
                                *   Here we have to show the Fields
                                * */

                                upload.folderID = obj.id;
                                upload.folderName = obj.text;

                                console.log("das modal soll angezeigt werden");

                                $('#upload_modal').modal("show");
                                /*$("#cameronet_drop").trigger("click",
                                    [obj.text,obj.id]
                                );*/
                            }
                        },
                        "download_file" : {
                            "label"				: "Herunterladen",
                            "icon"              : "../../img/download.png",
                            "action"			: function (data) {
                                var inst = $.jstree.reference(data.reference),
                                    obj = inst.get_node(data.reference);

                                    $.ajax({
                                        url : "/cgi-bin/download.cgi?",
                                        type: "POST",
                                        data: "name="+obj.text,
                                        success : function(res){
                                            console.log(res);
                                            window.location.href = res;
                                        },
                                        error : function(err){
                                            console.log(err);
                                        }
                                    });

                                    console.log("This is the Object : " + obj);
                                    console.log("This is the Instance : " + inst);
                            }
                        }
                    };

                    if(this.get_type(node) === "file") {
                        delete tmp.create;
                        delete tmp.ccp.submenu.upload_file;
                    }

                    if(this.get_type(node) === "default") {
                        delete tmp.ccp.submenu.download_file;
                    }
                    return tmp;
                }
            }
        });

        /**
         *  We will open all the nodes from the tree when the data is there
         */

        $jsTree.on("loaded.jstree",function(){
            $(this).jstree("open_all");
        });

        /**
         *  Here will happen the magic in the table at the right side when will be clicked
         */

        $jsTree.on("changed.jstree",function(e,data){
            console.log(e);
            console.log(data);
            console.log(data.node.type);
            console.log(data.node.id);

            if(data.node.type === "default"){
                $("table.for_files").attr("hidden",true);
                $("table.for_test").attr("hidden",false);
                //forFolders.writeDetails(data);
            }

            if(data.node.type === "file"){
                $("table.for_test").attr("hidden",true);
                forFiles.writeDetails(data);
                $("table.for_files").attr("hidden",false);
            }
        });

        console.log(data);

        showDataInTree.searchForItems();
    },
    searchForItems : function(){
        $("#jstree4_q").off("keyup");
        $("#jstree4_q").on("keyup",function(){
            var v = $(this).val();
            console.log(v);
            $(".jstree_folders").jstree(true).search(v);
        });
    }
};

var processEvents = {
    processNode : function(json){
        console.log("ajax function");
        console.log(json);

        $.ajax({
            url : "/cgi-bin/events.cgi?",
            type : "POST",
            data : json,
            success : function(res){
                console.log(res);
                //setTimeout(function(){connectDB.init();},50);
            },
            error : function(err){
                console.log("something went wrong " + err);
            },
            complete : function(){
                //setTimeout(function(){connectDB.init();},50);
                setTimeout(function(){window.location.reload();},50);
            }
        });
    }
};

var upload = {
    folderID        : null,
    folderName      : null,
    autorID         : null,
    docVersion      : null,
    docDate         : null,
    docCategory     : null,
    docComments     : null,
    counter         : 0,
    $cameronetDrop  : $("#cameronet_drop"),

    defineDropzone : function(){

        upload.$cameronetDrop.off("click");
        upload.$cameronetDrop.dropzone({
            url             : "/cgi-bin/upload.cgi",
            clickable       : true,
            addRemoveLinks  : false,
            maxFiles        : 1,
            _this           : this,
            init: function() {

                var $autorID            = $("#autor_id").attr("id");
                var $docVersion         = $("#doc_version").attr("id");
                var $docDate            = $("#doc_date").attr("id");
                var $keywords           = $("#doc_category").attr("id");
                var $doc_description    = $("#doc_description").attr("id");
                var elemsArray          = [];

                elemsArray.push($autorID,$docVersion,$docDate,$keywords,$doc_description);
                var elemsArrayLength = elemsArray.length;

                this.on("addedfile", function(file){
                    upload.counter = 0;

                    if( (upload.folderID == null) || (upload.folderName == null) ){
                        console.error("Folder ID or Folder Name is not present");
                        return;
                    }else{
                        for(var i=0; i < elemsArrayLength; i++){
                            var el = elemsArray[i], elVal = $("#"+el).val();

                            if(elVal == ""){
                                $("#"+el).css({"background-color": "tomato"});
                                upload.counter++;
                            }else{
                                $("#"+el).css({"background-color": "#fff"});
                            }
                        }
                    }

                    if(upload.counter == 0){
                        this.on("sending", function(file, xhr, formData){

                            upload.autorID          = $("#autor_id").val();
                            upload.docVersion       = $("#doc_version").val();
                            upload.docDate          = $("#doc_date").val();
                            upload.docCategory      = $("#doc_category").val();
                            upload.docComments      = $("#doc_description").val();

                            formData.append("folderName",upload.folderName);
                            formData.append("folderId",upload.folderID);
                            formData.append("autorId",upload.autorID);
                            formData.append("docVersion",upload.docVersion);
                            formData.append("docDate",upload.docDate);
                            formData.append("docCategory",upload.docCategory);
                            formData.append("docComments",upload.docComments);

                            console.log("We have sended what we have prepared");
                            console.log(upload.autorID);

                            upload.folderID = upload.folderName = null;
                        });
                        this.on("complete",function(){
                            //setTimeout(function(){window.location.reload();},850);
                        });
                    }else{
                        this.removeAllFiles();
                    }
                    //console.log(upload.counter);
                });

                this.on("maxfilesexceeded",function(file){
                    this.removeAllFiles();
                    this.addFile(file);
                });
            }
        });
    }
};

// For todays date;
Date.prototype.today = function () {
    return this.getFullYear() +"-"+ (((this.getMonth()+1) < 10)?"0":"") + (this.getMonth()+1) +"-"+ ((this.getDate() < 10)?"0":"") + this.getDate();
}

// For the time now
Date.prototype.timeNow = function () {
    return ((this.getHours() < 10)?"0":"") + this.getHours() +":"+ ((this.getMinutes() < 10)?"0":"") + this.getMinutes() +":"+ ((this.getSeconds() < 10)?"0":"") + this.getSeconds();
}