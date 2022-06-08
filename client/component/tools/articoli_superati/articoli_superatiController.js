myapp.controller("articoli_superatiController", [
    "$scope", "$rootScope", "$http", "$routeParams", "$location", "$timeout",

    function($scope, $rootScope, $http, $routeParams, $location, $timeout) {
        // create a message 
        console.log('articoli_superatiController');



        $scope.cerca = function(articolo) {


            $http.get('/tools/articolo_superato/find_articolo/' + articolo).then(function(resp) {


                $scope.info_art = resp.data

            });

        }


        function resetmsg() {

            location.reload()
        }


        $scope.invia = function() {


            x = confirm("Sei sicuro di voler inviare l'Email ?")

            if (x == true) {

                $scope.tsend = 1;



                q = { 'data': $scope.info_art[0], 'note': $scope.note, 'codice': $scope.codice }

                $http.post('/tools/articolo_superato/send_email', q).then(function(resp) {


                    $scope.respo = resp.data

                    $scope.msg = resp.data.msg

                    $scope.tsend = 0;

                    $timeout(resetmsg, 3000);

                });


            }


        }




    }
]);