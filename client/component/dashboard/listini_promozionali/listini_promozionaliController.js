myapp.controller("listini_promozionaliController", [
    "$scope", "$rootScope", "$http", "$routeParams", "$location",

    function($scope, $rootScope, $http, $routeParams, $location) {
        // create a message 
        console.log('listini_promozionaliController');

        $scope.vw = 0;
        $scope.msg = 0;
        $scope.cerca = 1;

        $scope.arrow_up = 0
        $scope.arrow_down = 0

        $http.get('/listini_promozionali/find_list_promo').then(function(resp) {
            $scope.db_listini = resp.data



        });



        $scope.cerca_listino = function(idlistino) {

            $scope.cerca = 0;
            $scope.msg = 0;

            $scope.data_listino = []
            idlistino = $scope.myid_listino

            $http.get('/listini_promozionali/find_list_promo/' + idlistino).then(function(resp) {
                $scope.data_listino = resp.data
                console.log($scope.data_listino)

                if ($scope.data_listino.msg == 'errore') {
                    $scope.msg = 1;
                    $scope.vw = 0;
                    $scope.cerca = 1
                } else {
                    $scope.msg = 0;
                    $scope.cerca = 1
                }




            });

        }


        $scope.exportReportToExcel = function() {
            let table = document.getElementsByTagName("table");
            TableToExcel.convert(table[0], {
                name: `report_listino.xlsx`,
                sheet: {
                    name: 'Sheet 1'
                }
            });
        }
        $scope.exportReportToExcel2 = function() {
            let table = document.getElementsByTagName("table");
            TableToExcel.convert(table[1], {
                name: `andamento_fatturato.xlsx`,
                sheet: {
                    name: 'Sheet 1'
                }
            });
        }




    }
]);