myapp.controller("info_articoloController", [
    "$scope", "$rootScope", "$http", "$routeParams", "$location",

    function($scope, $rootScope, $http, $routeParams, $location) {
        // create a message 
        console.log('info_articoloController');



        var y = new Date().getFullYear()
        var mm = new Date().getMonth() + 1
        $scope.cmese = mm
        $scope.cy = String(y)
        $scope.c1 = String(y - 1)
        $scope.c2 = String(y - 2)
        $scope.col_cerca = 7


        $scope.cerca = function(codice) {

            $scope.info_codice = []
            $scope.info_magazz = []
            $scope.info_prezzo_base = []
            $scope.anno_corrente = 0
            $scope.anno_precedente = 0
            $scope.anno_mdue = 0



            $http.get('/tools/info_articolo/find_codice/' + codice).then(function(resp) {


                $scope.current_page = $location.path()
                let look_path = $scope.current_page.split('/')
                console.log(look_path)
                $scope.current_page = look_path[1]

                $scope.info_codice = resp.data[0]

                if ($scope.info_codice) {
                    $scope.col_cerca = 10
                }
                if ($scope.info_codice == undefined) {
                    $scope.message = true
                } else {
                    $scope.message = false
                }


            });

            $http.get('/tools/info_articolo/find_data_magaz/' + codice).then(function(resp) {

                $scope.info_magazz = resp.data

            });

            $http.get('/tools/info_articolo/find_prezzo_base/' + codice).then(function(resp) {

                $scope.info_prezzo_base = resp.data

            });


            $http.get('/tools/info_articolo/find_padre_figlio/' + codice).then(function(resp) {

                $scope.info_pad_fig = resp.data
                if ($scope.info_pad_fig.length > 0) {
                    $scope.col = 7
                } else {
                    $scope.col = 12
                }

            });

            $http.get('/tools/info_articolo/find_static_art/' + codice).then(function(resp) {

                $scope.info_static_art = resp.data

                $scope.anno_corrente = 0
                $scope.anno_precedente = 0
                $scope.anno_mdue = 0

                angular.forEach($scope.info_static_art, function(value) {


                    if (value.ANNO == $scope.cy) {

                        $scope.anno_corrente += value.IMPNETTO
                    }
                    if (value.ANNO == $scope.c1) {

                        $scope.anno_precedente += value.IMPNETTO

                    }
                    if (value.ANNO == $scope.c2) {

                        $scope.anno_mdue += value.IMPNETTO
                    }

                })

            });



        }



        $scope.exportToExcel = function() {

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
            a.download = 'Indagine.xls';
            a.click();
        };












    }
]);