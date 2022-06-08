myapp.controller("articolo_Controller", [
    "$scope", "$rootScope", "$http", "$routeParams", "$location", "$window",

    function($scope, $rootScope, $http, $routeParams, $location, $window) {
        // create a message 
        console.log('articolo_Controller');

        $scope.insert = true
        $scope.modify = false
        $scope.insert_prev = true
        $scope.modify_prev = false
        $scope.insert_nota = true
        $scope.modify_nota = false
        $scope.preventivo = false
        $scope.db_note_preventivo = []
        $scope.articoid = $routeParams.id;


        $http.get('/tools/campioni/getcampioni/articolo/' + $scope.articoid).then(function(resp) {
            $scope.db_articolo = resp.data[0]
        });


        $http.get('/tools/campioni/getcampioni/articolo/change_stato/' + $scope.articoid).then(function(resp) {
            $scope.db_action = resp.data
        });


        $http.get('/tools/campioni/getcampioni/articolo/note/' + $scope.articoid).then(function(resp) {
            $scope.db_note_articolo = resp.data
        });

        $http.get('/tools/campioni/getcampioni/articolo/indagine/' + $scope.articoid).then(function(resp) {
            $scope.db_indagine_tab = resp.data

            $scope.tot_qta_indagini = 0

            angular.forEach($scope.db_indagine_tab, function(value) {

                $scope.tot_qta_indagini += parseFloat(value.qta_annua)


            });





        });

        $http.get('/tools/campioni/getcampioni/articolo/preventivo/' + $scope.articoid).then(function(resp) {
            $scope.db_note_preventivo = resp.data

            $scope.preventivi_to_print = []

            angular.forEach($scope.db_note_preventivo, function(value) {

                if (value.stato == 1) {

                    $scope.preventivi_to_print.push(value)

                }

            });


        });


        $scope.updatestatus = function() {
            delete $scope.db_articolo._id
            q = { 'stato': $scope.mynewstato }
            $http.post('/tools/campioni/updatestatus/' + $scope.articoid, q).then(function(resp) {
                $scope.addresponse = resp.data.msg
            });

            $scope.data_change = moment($scope.data_change).format('DD/MM/YYYY - h:mm:ss');
            stato_change = { 'id_articolo': $scope.articoid, 'codice': $scope.db_articolo.cod_interno, 'data_cambio_stato': $scope.data_change, 'user_action': $rootScope.login_info.username, 'vecchio_stato': $scope.db_articolo.stato, 'nuovo_stato': $scope.mynewstato }
            $http.post('/tools/campioni/add_action_stato', stato_change).then(function(resp) {
                $scope.db_indagine_tot = resp.data.msg
                location.reload()
            });

        }


        $scope.update_indagine = function() {


            $http.post('/tools/campioni/update_indagine/' + $scope.db_indagine._id, $scope.db_indagine).then(function(resp) {
                $scope.update_respons = resp.data.msg
                location.reload()
            });
        }


        $scope.update_preventivo = function() {


            $http.post('/tools/campioni/update_preventivo/' + $scope.db_preventivo._id, $scope.db_preventivo).then(function(resp) {
                $scope.update_respons_prev = resp.data.msg;
                location.reload()
            });
        }

        $scope.update_preventivo_bad = function() {

            $scope.db_preventivo.stato = 0
            $http.post('/tools/campioni/update_preventivo/' + $scope.db_preventivo._id, $scope.db_preventivo).then(function(resp) {
                $scope.update_respons_prev = resp.data.msg;
                location.reload()
            });
        }

        $scope.update_preventivo_good = function() {

            $scope.db_preventivo.stato = 1
            $http.post('/tools/campioni/update_preventivo/' + $scope.db_preventivo._id, $scope.db_preventivo).then(function(resp) {
                $scope.update_respons_prev = resp.data.msg;
                location.reload()
            });
        }

        $scope.update_preventivo_black = function() {

            $scope.db_preventivo.stato = null
            $http.post('/tools/campioni/update_preventivo/' + $scope.db_preventivo._id, $scope.db_preventivo).then(function(resp) {
                $scope.update_respons_prev = resp.data.msg;
                location.reload()
            });
        }


        $scope.update_nota = function() {


            $http.post('/tools/campioni/update_note/' + $scope.db_note._id, $scope.db_note).then(function(resp) {
                $scope.update_respons_note = resp.data.msg
                location.reload()
            });
        }


        $scope.deletecomment = function(id) {

            x = confirm("Vuoi eliminare questa nota ?")
            if (x == true) {
                $http.get('/tools/campioni/deletecomment/' + id).then(function(resp) {
                    $scope.deletemsg = resp.data.msg
                    location.reload()
                });

            }

        }

        $scope.deletepreventivo = function(id) {

            x = confirm("Vuoi eliminare questa nota ?")
            if (x == true) {
                $http.get('/tools/campioni/deletepreventivo/' + id).then(function(resp) {
                    $scope.deletemsg = resp.data.msg
                    location.reload()
                });


            }

        }



        $scope.delete_nota_tech = function(id) {

            x = confirm("Vuoi eliminare questa nota ?")
            if (x == true) {
                $http.get('/tools/campioni/delete_note_tech/' + id).then(function(resp) {
                    $scope.deletemsg = resp.data.msg
                    location.reload()
                });


            }

        }

        $scope.delete_nota_tot = function(id) {

            x = confirm("Vuoi eliminare questa nota ?")
            if (x == true) {
                $http.get('/tools/campioni/delete_tot_nota/' + id).then(function(resp) {
                    $scope.deletemsg = resp.data.msg
                    location.reload()
                });


            }

        }


        $scope.deleteindagine = function(id) {

            x = confirm("Vuoi eliminare questa nota ?")
            if (x == true) {
                $http.get('/tools/campioni/deleteindagine/' + id).then(function(resp) {
                    $scope.deletemsg = resp.data.msg
                    location.reload()
                });


            }

        }



        $scope.addnewgenericnote = function() {
            var m = new Date();
            m = m.toLocaleString()
            q = { 'relid': $scope.articoid, 'tipo': $scope.db_note.tipo, 'insert_date': m, 'note': $scope.db_note.note, 'login_user_acttion': $rootScope.login_info.username }

            $http.post('/tools/campioni/addnewnotagenerica', q).then(function(resp) {
                $scope.addnotares = resp.data.msg
                location.reload()
            });



        }


        $scope.add_indagine = function(data) {

            data.relid = $scope.db_articolo._id
            data.user_login = $rootScope.login_info.username

            $http.post('/tools/campioni/add_indagine', data).then(function(resp) {
                $scope.db_indagine_tot = resp.data.msg
                location.reload()
            });



        }


        $scope.add_preventivo = function() {

            $scope.db_preventivo.relid = $scope.db_articolo._id
            $scope.db_preventivo.user_login_prev = $rootScope.login_info.username

            $http.post('/tools/campioni/add_preventivo', $scope.db_preventivo).then(function(resp) {
                $scope.db_preventivo = resp.data.msg
                location.reload()
            });



        }


        $scope.button_indagine = function() {

            $scope.insert = true
            $scope.modify = false
            $scope.db_indagine = {}
        }
        $scope.button_preventivo = function() {

            $scope.insert_prev = true
            $scope.modify_prev = false
            $scope.preventivo = false
            $scope.db_preventivo = {}
        }
        $scope.button_nota = function() {

            $scope.insert_nota = true
            $scope.modify_nota = false
            $scope.db_note = {}
        }


        $scope.get_one_indagine = function(data) {

            $scope.insert = false
            $scope.modify = true
            $scope.db_indagine = data

        }
        $scope.get_one_preventivo = function(data) {

            $scope.insert_prev = false
            $scope.modify_prev = true
            $scope.preventivo = true
            $scope.db_preventivo = data

        }
        $scope.get_one_note = function(data) {

            $scope.db_note = data
            $scope.insert_nota = false
            $scope.modify_nota = true
        }

        $scope.get_one_total_nota = function(data) {

            $scope.db_note = data
            $scope.insert_nota = false
            $scope.modify_nota = true
        }

        $scope.get_one_nota_tech = function(data) {

            $scope.db_note = data
            $scope.insert_nota_tech = false
            $scope.modify_nota_tech = true
        }



        $scope.exportToExcelpreventivo = function() {

            debugger;
            var uri = 'data:application/vnd.ms-excel;base64,',
                template = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>{CouponDetails}</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--></head><body><table>{table}</table></body></html>',
                base64 = function(s) { return window.btoa(unescape(encodeURIComponent(s))) },
                format = function(s, c) { return s.replace(/{(\w+)}/g, function(m, p) { return c[p]; }) }

            var table = document.getElementById("mytable");
            var ctx = { worksheet: name || 'Worksheet', table: table.innerHTML };
            var url = uri + base64(format(template, ctx));
            var a = document.createElement('a');
            a.href = url;
            a.download = 'Preventivo.xls';
            a.click();
        };

        $scope.exportToExcelindagine = function() {

            debugger;
            var uri = 'data:application/vnd.ms-excel;base64,',
                template = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>{CouponDetails}</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--></head><body><table>{table}</table></body></html>',
                base64 = function(s) { return window.btoa(unescape(encodeURIComponent(s))) },
                format = function(s, c) { return s.replace(/{(\w+)}/g, function(m, p) { return c[p]; }) }

            var table = document.getElementById("mytable2");
            var ctx = { worksheet: name || 'Worksheet', table: table.innerHTML };
            var url = uri + base64(format(template, ctx));
            var a = document.createElement('a');
            a.href = url;
            a.download = 'Indagine.xls';
            a.click();
        };



        $scope.print_element = function() {



            var style = "<style>";
            style = style + "table {width: 100%; font: 12px Calibri; margin-top: 20px;margin-bottom: 20px; padding: 10px;box-shadow: 2px 2px 4px 4px rgba(128, 128, 128, 0.377); border-radius: 5px 5px 5px 5px ;}";
            style = style + "table, th, td {border: solid 1px #DDD; border-collapse: collapse;";
            style = style + "padding: 2px 3px; text-align: center;}";
            style = style + "div {margin: 15px;}";
            style = style + ".art {margin-bottom: 25px; border: 1px solid rgba(128, 128, 128, 0.345); box-shadow: 2px 2px 4px 4px rgba(128, 128, 128, 0.377); border-radius: 5px 5px 5px 5px ;}";
            style = style + ".infotop { border: 1px solid rgba(128, 128, 128, 0.345);box-shadow: 2px 2px 4px 4px rgba(128, 128, 128, 0.377); border-radius: 5px 5px 5px 5px ; height: 50px;}";
            style = style + ".text_banner {float: right; text-align: center; justify-content: center;}";
            /*             style = style + ".text_banner1 {padding-top: 50px !important;}"; */
            style = style + "img {width: 250px; float: right;}";
            style = style + ".no-print {display: none;}";
            style = style + ".text {font-size: 9px;}";
            style = style + "</style>";

            var mywindow = window.open('', 'PRINT', 'height=800,width=1000');
            mywindow.document.write('<html style="margin: 0 auto;"><head><title>' + document.title + '</title>');
            mywindow.document.write(style);
            mywindow.document.write('</head><body >');
            mywindow.document.write('<h1 style="margin-top: 10px; font-weight: bold; border-radius: 5px 5px 5px 5px ;text-align: center; padding-top: 5px; padding-bottom: 5px;">' + "ACCETTAZIONE PREVENTIVO" + '</h1>');
            mywindow.document.write(document.getElementById('printbox').innerHTML)
            mywindow.document.write(document.getElementById('elem1').innerHTML);
            mywindow.document.write(document.getElementById('elem').innerHTML);
            mywindow.document.write('<h2 style="margin-top: 35px; font-weight: bold;background-color: #fc7b03; color: whitesmoke;  border-radius: 5px 5px 5px 5px ; padding: 10px;">' + "PREVENTIVO" + '</h2>');
            mywindow.document.write(document.getElementById('elem2').innerHTML);
            mywindow.document.write('<h2 style="margin-top: 40px; font-weight: bold;background-color: #2c7da0; color: whitesmoke;  border-radius: 5px 5px 5px 5px ; padding: 10px;">' + "INDAGINI" + '</h2>');
            mywindow.document.write(document.getElementById('elem3').innerHTML);
            mywindow.document.write(document.getElementById('printOnly').innerHTML);
            mywindow.document.close();
            mywindow.focus();

            mywindow.print();
            mywindow.close();

        }


        $scope.print_element_P_I_tab = function() {



            var style = "<style>";
            style = style + "table {width: 100%; font: 12px Calibri; margin-top: 20px;margin-bottom: 20px; padding: 10px;box-shadow: 2px 2px 4px 4px rgba(128, 128, 128, 0.377); border-radius: 5px 5px 5px 5px ;}";
            style = style + "table, th, td {border: solid 1px #DDD; border-collapse: collapse;";
            style = style + "padding: 2px 3px; text-align: center;}";
            style = style + "div {margin: 15px;}";
            style = style + ".art {margin-bottom: 25px; border: 1px solid rgba(128, 128, 128, 0.345); box-shadow: 2px 2px 4px 4px rgba(128, 128, 128, 0.377); border-radius: 5px 5px 5px 5px ;}";
            style = style + ".infotop { border: 1px solid rgba(128, 128, 128, 0.345);box-shadow: 2px 2px 4px 4px rgba(128, 128, 128, 0.377); border-radius: 5px 5px 5px 5px ; height: 50px;}";
            style = style + ".text_banner {float: right; text-align: center; justify-content: center;}";
            /*             style = style + ".text_banner1 {padding-top: 50px !important;}"; */
            style = style + "img {width: 250px; float: right;}";
            style = style + ".no-print {display: none;}";
            style = style + ".text {font-size: 9px;}";
            style = style + "</style>";

            var mywindow = window.open('', 'PRINT', 'height=800,width=1000');
            mywindow.document.write('<html style="margin: 0 auto;"><head><title>' + document.title + '</title>');
            mywindow.document.write(style);
            mywindow.document.write('</head><body >');
            mywindow.document.write('<h1 style="margin-top: 10px; font-weight: bold; border-radius: 5px 5px 5px 5px ;text-align: center; padding-top: 5px; padding-bottom: 5px;">' + "ACCETTAZIONE PREVENTIVO" + '</h1>');
            mywindow.document.write(document.getElementById('printbox').innerHTML)
            mywindow.document.write(document.getElementById('elem1').innerHTML);
            mywindow.document.write(document.getElementById('elem').innerHTML);
            mywindow.document.write('<h2 style="margin-top: 35px; font-weight: bold;background-color: #fc7b03; color: whitesmoke;  border-radius: 5px 5px 5px 5px ; padding: 10px;">' + "PREVENTIVO" + '</h2>');
            mywindow.document.write(document.getElementById('elem4').innerHTML);
            mywindow.document.write('<h2 style="margin-top: 40px; font-weight: bold;background-color: #2c7da0; color: whitesmoke;  border-radius: 5px 5px 5px 5px ; padding: 10px;">' + "INDAGINI" + '</h2>');
            mywindow.document.write(document.getElementById('elem3').innerHTML);
            mywindow.document.write(document.getElementById('printOnly').innerHTML);
            mywindow.document.close();
            mywindow.focus();

            mywindow.print();
            mywindow.close();

        }



    }


]);