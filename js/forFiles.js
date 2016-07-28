var forFiles = {

    writeDetails : function(data){
        /**
         *  in the "data" we have saved all the Informations from the clicked File ( NOT Folder !!!)
         */
        var html = "";
        console.log(data);

        var $id     = data.node.original.id;
        var $text   = data.node.original.id;
        var $id     = data.node.original.id;
        var $id     = data.node.original.id;
        var $id     = data.node.original.id;


        html += '<thead>';
        html += '<tr>';
        html += '<th>#</th>';
        html += '<th>Dok. Nummer</th>';
        html += '<th>Dok. Name</th>';
        html += '<th>Kategorie</th>';
        html += '<th>Autor</th>';
        html += '<th>Rev.</th>';
        html += '<th>Dok. Datum</th>';
        html += '<th>Freigeben</th>';
        html += '</tr>';
        html += '</thead>';

        html += '<tr data-toggle="collapse" data-target="#fat" class="accordion-toggle">';
        html += '<th scope="row">1</th>';
        html += '<td>'+data.node.original.id+'</td>';
        html += '<td>'+data.node.original.text+'</td>';
        html += '<td>Anweisung</td>';
        html += '<td>'+data.node.original.doc_autor+'</td>';
        html += '<td>Rev. '+data.node.original.doc_version+'</td>';
        html += '<td>'+data.node.original.doc_created+'</td>';
        html += '<td class="status locked"></td>';
        html += '</tr>';
        html += '<tr>';
        html += '<td colspan="12" class="hiddenRow">';
        html += '<div id="fat" class="accordian-body collapse">';
        html += '<table class="table table-striped">';
        html += '<thead>';
        html += '<tr>';
        html += '<th>Dok. Nummer</th>';
        html += '<th>Dok. Name</th>';
        html += '<th>Kategorie</th>';
        html += '<th>Autor</th>';
        html += '<th>Rev.</th>';
        html += '<th>Beschreibung</th>';
        html += '<th>Dok. Datum</th>';
        html += '<th>Freigeben</th>';
        html += '<th>#</th>';
        html += '</tr>';
        html += '</thead>';
        html += '<tbody>';
        html += '<tr>';
        html += '<td>'+data.node.original.id+'</td>';
        html += '<td>'+data.node.original.text+'</td>';
        html += '<td>Anweisung</td>';
        html += '<td>'+data.node.original.doc_autor+'</td>';
        html += '<td>Rev. '+data.node.original.doc_version+'</td>';
        html += '<td>'+data.node.original.doc_description+'</td>';
        html += '<td>'+data.node.original.doc_created+'</td>';
        html += '<td class="status unlocked" id=""></td>';
        html += '<td>';
        html += '<button type="button" class="btn btn-default btn-sm download" id="download_'+data.node.original.id+'">';
        html += '<i class="glyphicon glyphicon-download"> <b>Herunterladen</b></i>';
        html += '</button>';
        html += '</td>';
        html += '</tr>';
        html += '</tbody>';
        html += '</table>';
        html += '</div>';
        html += '</td>';
        html += '</tr>';
        html += '</tbody>';
        html += '</table>';

        $("table.for_files").html(html);
        forFiles.clickOnStatus();
    },
    clickOnStatus : function(){
        var $status = $("td.status");

        $status.off("click");
        $status.on("click",function(e){
            e.preventDefault();
            e.stopPropagation();

            var $this   = $(this);

            if($this.hasClass("locked")){

                json = "status="+JSON.stringify(
                        {
                            "BID":node.original.bid,
                            "OriginalName":node.text,
                            "ParentID":node.parent,
                            "NewName":nodePosition,
                            "FolderID":node.original.FolderID
                        }
                    );
                console.log("we send a lock message to the server");
                //processEvents.processNode(json);

                $this.addClass("unlocked");
                $this.removeClass("locked");
            }else{

                console.log("we send an unlock message to the server");
                //processEvents.processNode(json);

                $this.addClass("locked");
                $this.removeClass("unlocked");
            }
        });
    },
    sendStatus : function(){
        /**
         *  we will send the status of the document (locked or unlocked) plus the ID for this Document
         */

        $.ajax({
            url : "/cgi-bin/change_status.cgi?",
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