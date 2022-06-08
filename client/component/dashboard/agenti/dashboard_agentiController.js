myapp.controller("dashboard_agentiController", [
    "$scope", "$rootScope", "$http", "$routeParams", "$location",

    function($scope, $rootScope, $http, $routeParams, $location) {
        // create a message 
        console.log('dashboard_agentiController');

        // SET ANNI
        var y = new Date().getFullYear()
        var mm = new Date().getMonth() + 1
        $scope.cmese = mm
        $scope.cy = String(y)
        $scope.c1 = String(y - 1)
        $scope.c2 = String(y - 2)


        $scope.getTotal = function(type) {
            var total = 0;
            angular.forEach($scope.mydb, function(el) {
                total += el[type];
            });
            return total;
        };



        function summese() {
            let q = { "IDAGENTE": parseInt($scope.id_agente), "MESE": mm }
            $http
                .post("/dashboard/agenti/sumquery", q)
                .then(function(response) {
                    $scope.db_sum_mese = response.data
                    angular.forEach($scope.db_sum_mese, function(value) {
                        if (value._id == $scope.cy) { $scope.tot_mese = value.sum }
                        if (value._id == $scope.c1) { $scope.tot_mesep = value.sum }
                        if (value._id == $scope.c2) { $scope.tot_mesepp = value.sum }
                    });

                });

        }

        function summanni() {
            let q = { "IDAGENTE": parseInt($scope.id_agente) }

            $http
                .post("/dashboard/agenti/sumquery", q)
                .then(function(response) {
                    $scope.db_sum_anni = response.data

                    angular.forEach($scope.db_sum_anni, function(value) {
                        if (value._id == $scope.cy) { $scope.tot_anno = value.sum }
                        if (value._id == $scope.c1) { $scope.tot_annop = value.sum }
                        if (value._id == $scope.c2) { $scope.tot_annopp = value.sum }
                    });

                });

        }


        function summanni_vending() {
            let q = { "IDAGENTE": parseInt($scope.id_agente), "isVending": -1 }

            $http
                .post("/dashboard/agenti/sumquery", q)
                .then(function(response) {
                    $scope.db_sum_anni_vending = response.data

                    angular.forEach($scope.db_sum_anni_vending, function(value) {
                        if (value._id == $scope.cy) { $scope.tot_anno_vending = value.sum }
                        if (value._id == $scope.c1) { $scope.tot_annop_vending = value.sum }
                        if (value._id == $scope.c2) { $scope.tot_annopp_vending = value.sum }
                    });

                });

        }

        function summanni_tradizionale() {
            let q = { "IDAGENTE": parseInt($scope.id_agente), "isVending": 0 }

            $http
                .post("/dashboard/agenti/sumquery", q)
                .then(function(response) {
                    $scope.db_sum_anni_tradizionale = response.data

                    angular.forEach($scope.db_sum_anni_tradizionale, function(value) {
                        if (value._id == $scope.cy) { $scope.tot_anno_trad = value.sum }
                        if (value._id == $scope.c1) { $scope.tot_annop_trad = value.sum }
                        if (value._id == $scope.c2) { $scope.tot_annopp_trad = value.sum }
                    });

                });

        }


        function summesi_vending() {
            let q = { "IDAGENTE": parseInt($scope.id_agente), "isVending": -1, "MESE": mm }

            $http
                .post("/dashboard/agenti/sumquery", q)
                .then(function(response) {
                    $scope.db_sum_mesi_vending = response.data

                    angular.forEach($scope.db_sum_mesi_vending, function(value) {
                        if (value._id == $scope.cy) { $scope.tot_mesi_vending = value.sum }
                        if (value._id == $scope.c1) { $scope.tot_mesip_vending = value.sum }
                        if (value._id == $scope.c2) { $scope.tot_mesipp_vending = value.sum }
                    });

                });

        }

        function summesi_tradizionale() {
            let q = { "IDAGENTE": parseInt($scope.id_agente), "isVending": 0, "MESE": mm }

            $http
                .post("/dashboard/agenti/sumquery", q)
                .then(function(response) {
                    $scope.db_sum_mesi_tradizionale = response.data

                    angular.forEach($scope.db_sum_mesi_tradizionale, function(value) {
                        if (value._id == $scope.cy) { $scope.tot_mesi_tradizionale = value.sum }
                        if (value._id == $scope.c1) { $scope.tot_mesip_tradizionale = value.sum }
                        if (value._id == $scope.c2) { $scope.tot_mesipp_tradizionale = value.sum }
                    });

                });

        }





        $http
            .get("/login_service")
            .then(function(response) {
                $scope.infologin = response.data;
                $scope.id_agente = $scope.infologin.id_agente
                summese();
                summanni();
                summanni_vending();
                summanni_tradizionale();
                summesi_vending();
                summesi_tradizionale();
                $scope.getdataanno('CLIENTE', 'IMPNETTO', 'CLIENTE')
            });




        $scope.getdataanno = function(tipo, valore, vw) {
            $scope.selCampo = vw
            $http
                .get("/dashboard/agenti/anno/" + $scope.id_agente + "/" + tipo + "/" + valore)
                .then(function(response) {
                    $scope.mydb = response.data

                    $scope.current_page = $location.path()
                    let look_path = $scope.current_page.split('/')
                    console.log(look_path)
                    $scope.current_page = look_path[1]
                });
        }


        $scope.getdatamese = function(tipo, valore, vw) {
            $scope.selCampo = vw
            $http
                .get("/dashboard/agenti/mese/" + $scope.id_agente + "/" + tipo + "/" + valore)
                .then(function(response) {
                    $scope.mydb = response.data

                });
        }




        $scope.ExportToExcel = function(type, fn, dl) {
            var elt = document.getElementById('tbl_exporttable_to_xls');
            var wb = XLSX.utils.table_to_book(elt, { sheet: "sheet1" });
            return dl ?
                XLSX.write(wb, { bookType: type, bookSST: true, type: 'base64' }) :
                XLSX.writeFile(wb, fn || ($scope.selCampo + '.' + (type || 'xlsx')));
        }


    }
]);