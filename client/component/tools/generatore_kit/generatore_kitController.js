myapp.controller("generatore_kitController", [
    "$scope", "$rootScope", "$http", "$routeParams", "$location", "$timeout",

    function($scope, $rootScope, $http, $routeParams, $location, $timeout) {


        // create a message 
        console.log('generatore_kitController');



        $scope.title = 'Generatore Kit'
        $scope.baseurl = "/tools/kit/";

        $scope.mych = [];


        $http.get("/tools/kit/getkit").then(function(response) {
            $scope.kit = response.data;

        });




        $scope.addtolist = function() {
            let q = {
                'kit': $scope.selected,
                'qta': parseInt($scope.qta)
            }
            $scope.mych.push(q);
            $scope.selected = '';
            $scope.qta = '';

            if ($scope.mych.length > 0) {
                $scope.calculate();
            }

        }




        function getNum(val) {
            if (isNaN(val)) {
                return 0;
            }
            return val;
        }



        $scope.removeItem = function(index) {
            $scope.mych.splice(index, 1);
            $scope.calculate();
        }

        $scope.calculate = function() {
            $scope.res = ""
            $http.post("/tools/kit/calculatekit", $scope.mych).then(function(response) {
                $scope.res = response.data
                if ($scope.res == '400') {
                    $scope.res = "";

                }

                $scope.mytotvprice = 0
                $scope.tot_peso = 0
                angular.forEach($scope.res, function(value) {
                    vprice = parseFloat(value.vprice) * parseFloat(value.qta)

                    if (isNaN(vprice)) {
                        $scope.mytotvprice += 0
                        $scope.unonan = true
                    } else {
                        $scope.mytotvprice += vprice
                    }

                    vpeso = parseFloat(value.peso) * parseFloat(value.qta)

                    if (isNaN(vpeso)) {
                        $scope.tot_peso += 0
                        $scope.unonan = true
                    } else {
                        $scope.tot_peso += vpeso
                    }


                });


            });


        }

        $scope.sumone = function(index) {
            $scope.mych[index].qta = $scope.mych[index].qta + 1
            $scope.calculate();
        }
        $scope.remone = function(index) {
            $scope.mych[index].qta = $scope.mych[index].qta - 1
            $scope.calculate();
        }

        $scope.print_element = function(elem, elem1) {
            var style = "<style>";


            style = style + "table {width: 100%; font: 17px Calibri;}";
            style = style + "table, th, td {border: solid 1px #DDD; border-collapse: collapse;";
            style = style + "padding: 2px 3px; text-align: center;}";
            style = style + "img {width: 50px;}";
            style = style + "</style>";
            var mywindow = window.open('', 'PRINT', 'height=800,width=1000');

            mywindow.document.write('<html style="margin: 0 auto;"><head><title>' + document.title + '</title>');
            mywindow.document.write(style);
            mywindow.document.write('</head><body >');
            mywindow.document.write('<h1>' + "Articoli Disponibili" + '</h1>');
            mywindow.document.write(document.getElementById(elem).innerHTML);
            mywindow.document.write('<h1 style="margin-top: 50px;">' + "Articoli Mancanti" + '</h1>');
            mywindow.document.write(document.getElementById(elem1).innerHTML);
            mywindow.document.write('</body></html>');

            mywindow.document.close();
            mywindow.focus();

            mywindow.print();
            mywindow.close();

            return true;

        }


    }
]);