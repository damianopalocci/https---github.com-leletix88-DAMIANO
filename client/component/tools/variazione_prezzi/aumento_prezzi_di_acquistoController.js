myapp.controller("aumento_prezzi_di_acquistoController", [
    "$scope", "$rootScope", "$http", "$routeParams", "$location", "$timeout",

    function($scope, $rootScope, $http, $routeParams, $location, $timeout) {


        $scope.$ = $;
        // create a message 
        console.log("aumento_prezzi_di_acquistoController")

        $http
            .get("/login_service")
            .then(function(response) {
                $scope.infologin = response.data;

            });



        $scope.view_message = false;
        $scope.newcol = 12;
        $scope.list_rimossi = [];
        $scope.lostrig = [];
        $scope.finaldb = [];
        let myroud = function(number, precision = 2, rounding = 0.05) {
            let multiply = 1 / rounding;
            return parseFloat(Math.round(number * multiply) / multiply).toFixed(
                precision
            );
        };





        function calcolofinale(data) {
            $scope.new_prezzi = []
            angular.forEach(data, function(value) {
                let nprezzo = parseFloat(value.prezzo) + parseFloat($scope.aumento)
                nprezzo = myroud(nprezzo)
                value['newprice'] = parseFloat(nprezzo)
                this.push(value);
            }, $scope.new_prezzi);


            $scope.unique_list = [...new Set($scope.new_prezzi.map(item => item.descr_listino))];

        }




        function calcolofinale_no_roud(data) {
            $scope.new_prezzi = []
            angular.forEach(data, function(value) {
                let nprezzo = parseFloat(value.prezzo) + parseFloat($scope.aumento)
                nprezzo = nprezzo
                value['newprice'] = parseFloat(nprezzo)
                this.push(value);
            }, $scope.new_prezzi);


            $scope.unique_list = [...new Set($scope.new_prezzi.map(item => item.descr_listino))];

        }




        $scope.listinic = function(articolo) {
            $http.get('/tools/aumenti/info/listini/' + articolo).then(function(resp) {
                $scope.allist = resp.data
                $scope.clear_listes = $scope.allist
                calcolofinale($scope.allist);
            });
        }


        $scope.listinic_noround = function(articolo) {
            $http.get('/tools/aumenti/info/listini/' + articolo).then(function(resp) {
                $scope.allist = resp.data
                $scope.clear_listes = $scope.allist
                calcolofinale_no_roud($scope.allist);
            });
        }


        $scope.cerca = function(articolo) {
            $http.get('/tools/aumenti/info/' + articolo).then(function(resp) {
                $scope.info_art = resp.data
                if ($scope.info_art.codice) {
                    $scope.msg = false;
                    $scope.newcol = 6;
                } else {
                    $scope.msg = true;
                    $scope.newcol = 12;
                    $scope.articolo = '';
                }
            });

        }

        $scope.resetsearch = function() {
            $scope.info_art = {}
            $scope.newcol = 12
        }




        $scope.calcolo = function(price) {
            $scope.aumento = parseFloat(price) * parseFloat($scope.info_art.ricarico);
            $scope.aumento = $scope.aumento + price;
            $scope.aumento = $scope.aumento - $scope.info_art.prezzo
            $scope.aumento = myroud($scope.aumento)
            $scope.listinic($scope.info_art.codice);
        }


        $scope.calcolo_percentuale = function(percentuale) {
            $scope.perccosto = parseFloat($scope.info_art.costo) * parseFloat(percentuale);
            $scope.perccosto = parseFloat($scope.perccosto) / 100
            $scope.perccosto = parseFloat($scope.perccosto) + parseFloat($scope.info_art.costo)
            $scope.aumento = parseFloat($scope.perccosto) * parseFloat($scope.info_art.ricarico);
            $scope.aumento = $scope.aumento + $scope.perccosto;
            $scope.aumento = $scope.aumento - $scope.info_art.prezzo
            $scope.aumento = myroud($scope.aumento)
            $scope.listinic($scope.info_art.codice);
        }




        $scope.calcolo_assoluto = function(price) {
            $scope.aumento = myroud(price);
            $scope.listinic($scope.info_art.codice);


        }

        $scope.calcolo_noroud = function(price) {
            $scope.aumento = price;
            $scope.listinic_noround($scope.info_art.codice);

        }


        $scope.remove = function(descr_listino) {
            for (var i = $scope.allist.length - 1; i >= 0; i--) {
                if ($scope.allist[i].descr_listino == descr_listino) {
                    $scope.lostrig.push($scope.allist[i])
                    $scope.allist.splice(i, 1);
                }
            }
            for (var i = $scope.unique_list.length - 1; i >= 0; i--) {
                if ($scope.unique_list[i] == descr_listino) {
                    $scope.list_rimossi.push($scope.unique_list[i])
                    $scope.unique_list.splice(i, 1);
                }
            }
        }


        $scope.readd = function(descr_listino) {
            for (var i = $scope.lostrig.length - 1; i >= 0; i--) {
                if ($scope.lostrig[i].descr_listino == descr_listino) {
                    $scope.allist.push($scope.lostrig[i])
                    $scope.lostrig.splice(i, 1);
                }
            }
            for (var i = $scope.list_rimossi.length - 1; i >= 0; i--) {
                if ($scope.list_rimossi[i] == descr_listino) {
                    $scope.unique_list.push($scope.list_rimossi[i]);
                    $scope.finaldb.push($scope.unique_list[i]);
                    $scope.list_rimossi.splice(i, 1);
                }
            }
        }

        $scope.send_agent_email = function() {
            var date = document.getElementById("mdate").value;
            q = {
                'date': date,
                'codice': $scope.info_art.codice,
                'aumento': $scope.aumento,
                'descrizione': $scope.info_art.descrizione,
                'ulr_image': $scope.info_art.ulr_image,
                'cod_originale': $scope.info_art.cod_originale,
                'marca': $scope.info_art.marca
            }
            $http.post('/tools/aumenti/send_agent_email/', q).then(function(resp) {

                if (resp.data.msg == 'success') {
                    window.location.reload();
                }



            });


        }


        $scope.programmate_aumento = function() {
            $http.post('/tools/aumenti/elaboratelist/', $scope.definitive).then(function(resp) {

                $scope.view_message = true;
                $("#modelId").modal("toggle");
                $('html,body').scrollTop(0);
                if (resp.data.msg == 'success') {
                    $scope.send_agent_email($scope.definitive.codice);

                }
            });

        }


        $scope.schedulate = function(seldata) {
            var seldata = document.getElementById("mdate").value;
            $scope.definitive = []
            angular.forEach($scope.allist, function(value) {
                value.descr_listino = value.descr_listino.trim();
                value['date'] = seldata;
                value.codice = $scope.info_art.codice
                value['elaborato'] = false;
                value['operatore'] = $scope.infologin.username;
                $scope.definitive.push(value)
            });
            $scope.programmate_aumento()
        }


    }
]);